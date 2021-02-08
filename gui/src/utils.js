export const apiUrl = 'http://' + window.location.hostname + ':5000/';

export const getStatus = (setter) => {
  fetch(apiUrl + "status")
    .then((response) => response.json())
    .then((data) => setter(data));
};

export const listRecipes = (callback) => {
  fetch(apiUrl + 'list')//this route returns an array with all the names ex: ['recipe1',recipe2']
    .then(response => response.json())
    .then(data => callback(data));
}

export const selectOption = (option) => {
  fetch(apiUrl + 'select/option/' + option)
    .then(response => response.json())
    .then(data => console.log(data))
}

export const stopRecipe = () => {
  fetch(apiUrl + 'stop')
  .then(response => response.json())
  .then(data => console.log(data))
}

export const startRecipe = name => {
  fetch(apiUrl + 'start/' + name)
    .then(response => response.json())
    .then(data => console.log(data))
}
