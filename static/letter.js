const $cocktailsList = $('.cocktails-list');
const $searchForm = $('#search-form');
const $letterZone = $('#letters')

// search for cocktails that start with a given letter. returns array of drink objects. 
async function getCocktailsByLetter(letter) {
    const response = await axios.get(`https://www.thecocktaildb.com/api/json/v1/1/search.php?f=${letter}`);
    return response.data;
}

// create html for the list of drinks
function populateCocktails(cocktails){
    $cocktailsList.empty();
    for (let cocktail of cocktails.drinks) {
        const $cocktail = $(
        `<div class="drink">
        <a href="/drinks/${cocktail.idDrink}"> 
        <img src="${cocktail.strDrinkThumb}/preview"><br>
        <b>${cocktail.strDrink}</b>
        </a>
        </div>
        `
        );
        $cocktailsList.append($cocktail)
    }
}

async function searchForDrinkAndDisplay(letter){
    let cocktails = await getCocktailsByLetter(letter);
    populateCocktails(cocktails)
};

$letterZone.click(async function(evt) {
    evt.preventDefault();
    letter = evt.target.innerText;
    await searchForDrinkAndDisplay(letter);
});