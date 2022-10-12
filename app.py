from asyncio import format_helpers
from flask import Flask, redirect, render_template, flash, session, g
from sqlalchemy.exc import IntegrityError
from models import connect_db, db, User, Favorite
from forms import RegisterForm, LoginForm
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

CURR_USER_KEY = 'curr_user'

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "secrets"

@app.before_request

def add_user_to_g():
    """if the user is logged in, add the current user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """login user"""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """logout"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        flash("Logged Out.", 'danger')

@app.route('/')
def show_home():
    """shows the main page"""
    return render_template('home.html')


##########  USER ROUTES #########

@app.route('/register', methods=["GET", "POST"])
def show_register_form():
    """shows the register form"""

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data.lower(),
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()
        
        except IntegrityError:
            flash("Username or email already taken", 'danger')
            return render_template('register.html', form=form)
        
        do_login(user)
        return redirect('/')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def show_login_form():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data.lower(), form.password.data)
       
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        
        flash('Incorrect username or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    '''do a logout'''
    do_logout()
    return redirect('/')

@app.route('/users/<int:userId>')
def show_favorites(userId):
    '''show the user's favorites'''
    favorites = g.user.favorites
    favoritesList = []
    for favorite in favorites:
        response = requests.get(f'http://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={favorite.cocktail_id}').json()
        favDict = {
            'id': response["drinks"][0]["idDrink"], 
            'name': response["drinks"][0]["strDrink"], 
            'img': response["drinks"][0]["strDrinkThumb"],
        }
        favoritesList.append(favDict)
    return render_template('favorites.html', user = g.user, favorites=favoritesList)

##### SEARCH COCKTAIL ROUTES #####

@app.route('/drinks/<int:idDrink>')
def cocktail_detail(idDrink): 
    '''show details on a given cocktail by retrieving that cocktail by its ID from the API'''
    response = requests.get(f'http://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={idDrink}').json()
    cocktail = response['drinks'][0]
    ingredients = []
    star = "Add to Favorites ☆"
    favorite = Favorite.query.filter_by(cocktail_id = idDrink).first()
    if favorite is not None:
        star = "Remove from Favorites ★"
    for i in range(1, 15):
        ingredient = cocktail[f'strIngredient{i}']
        if ingredient is not None:
            ingredients.append(ingredient)
    measurements = []
    for i in range(1, 15):
        measurement = cocktail[f'strMeasure{i}']
        if measurement is not None:
            measurements.append(measurement)
    return render_template('drink.html', cocktail=cocktail, ingredients=ingredients, measurements=measurements, star=star)

@app.route('/random')
def show_random():
    '''show the details on a random drink.'''
    response = requests.get(f'http://www.thecocktaildb.com/api/json/v1/1/random.php').json()
    id = response['drinks'][0]['idDrink']
    return cocktail_detail(id)

@app.route('/all')
def letter_search():
    '''shows the page to retrieve all cocktails by letter'''
    return render_template('lettersearch.html')

@app.route('/name')
def name_search():
    """search for a cocktail by name. handles by search.js"""
    return render_template('namesearch.html')

@app.route('/ingredient')
def ingredient_search():
    """brings up the page to search for cocktails by ingredient"""
    return render_template('ingredientsearch.html')

@app.route('/favorite/<int:idDrink>', methods=["POST"])
def handle_favorite(idDrink):
    """adds the drink to the current user's favorites"""
    if g.user:
        drinkId = idDrink
        userId = g.user.id
        try: 
            favorite = Favorite.query.filter_by(user_id=userId, cocktail_id = drinkId).first()
            db.session.delete(favorite)
            db.session.commit()
            flash('Favorite removed.', 'danger')
            return redirect(f'/users/{userId}')
        except:
            favorite = Favorite(user_id = userId, cocktail_id = drinkId)
            db.session.add(favorite)
            db.session.commit()
            return redirect(f'/users/{userId}')
    else:
        flash('You must be logged in to favorite a drink.', 'success')
        return redirect(f'/drinks/{idDrink}')
