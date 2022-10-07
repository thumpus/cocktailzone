const $cocktailsList = $('.cocktails-list');
const $searchForm = $('#search-form');

// search for cocktails that match the search query. returns array of drink objects. 
async function getCocktailsByTerm(term) {
    const response = await axios.get(`https://www.thecocktaildb.com/api/json/v1/1/search.php?s=${term}`);
    return response.data;
}

// create html for the list of drinks
function populateCocktails(cocktails){
    $cocktailsList.empty();
    console.log(cocktails)
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

//handle search form submission: get drinks from API and display em

async function searchForDrinkAndDisplay(){
    const term = $("#search-query").val();
    let cocktails = await getCocktailsByTerm(term);
    if (cocktails.drinks == null){
        $cocktailsList.empty();
        $cocktailsList.append(`No cocktails found with search term ${term}.`)
    } else {
        populateCocktails(cocktails)}
};

$searchForm.on("submit", async function(evt) {
    evt.preventDefault();
    await searchForDrinkAndDisplay();
});