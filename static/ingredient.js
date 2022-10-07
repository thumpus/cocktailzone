const $cocktailsList = $('.cocktails-list');
const $searchForm = $('#search-form');
const $button = $(".btn-secondary")

// search for cocktails that match the search query. returns array of drink objects. 
async function getCocktailsByIngredient(ingredient) {
    const response = await axios.get(`https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=${ingredient}`);
    return response.data;
}

// create html for the list of drinks
function populateCocktails(cocktails){
    $cocktailsList.empty();
    
    for (let cocktail of cocktails.drinks) {
        console.log(cocktail)
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

async function searchForDrinkAndDisplay(ingredient){
    let cocktails = await getCocktailsByIngredient(ingredient);
    if (cocktails.drinks == null){
        $cocktailsList.empty();
        $cocktailsList.append(`No cocktails found with ingredient: ${ingredient}.`)
    } else {
        populateCocktails(cocktails)}
};

$searchForm.on("submit", async function(evt) {
    evt.preventDefault();
    const ingredient = $("#search-query").val();
    await searchForDrinkAndDisplay(ingredient);
});

$button.click(async function(evt){
    const ingredient = evt.target.innerText;
    
    await searchForDrinkAndDisplay(ingredient);
})