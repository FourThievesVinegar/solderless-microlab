export const apiUrl = 'http://' + window.location.hostname + ':8081/'

export const downloadFileFromURL = (fileName, url) => {
  const link = document.createElement('a')
  link.download = fileName
  link.href = url
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  link.remove()
}

export const getStatus = setter => {
  fetch(apiUrl + 'status')
    .then(response => response.json())
    .then(data => setter(data))
}

export const listRecipes = callback => {
  fetch(apiUrl + 'list') //this route returns an array with all the names ex: ['recipe1',recipe2']
    .then(response => response.json())
    .then(data => callback(data))
}

export const selectOption = option => {
  fetch(apiUrl + 'select/option/' + option, {
    method: 'POST',
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const stopRecipe = () => {
  fetch(apiUrl + 'stop', {
    method: 'POST',
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const startRecipe = name => {
  fetch(apiUrl + 'start/' + name, {
    method: 'POST',
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const uploadRecipe = file => {
  const formData = new FormData()
  formData.append('File', file)
  return fetch(apiUrl + 'uploadRecipe', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const getControllerHardware = () => {
  return fetch(apiUrl + 'controllerHardware').then(response => response.json())
}

export const listControllerHardware = () => {
  return fetch(apiUrl + 'controllerHardware/list').then(response => response.json())
}

export const setControllerHardware = name => {
  return fetch(apiUrl + 'controllerHardware/' + name, {
    method: 'POST',
  }).then(response => response.json())
}

export const downloadControllerConfig = name => {
  const url = apiUrl + 'downloadControllerConfig/' + name
  downloadFileFromURL(name, url)
}

export const uploadControllerConfig = file => {
  const formData = new FormData()
  formData.append('File', file)
  return fetch(apiUrl + 'uploadControllerConfig', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const getLabHardware = () => {
  return fetch(apiUrl + 'labHardware').then(response => response.json())
}

export const listLabHardware = () => {
  return fetch(apiUrl + 'labHardware/list').then(response => response.json())
}

export const setLabHardware = name => {
  return fetch(apiUrl + 'labHardware/' + name, {
    method: 'POST',
  }).then(response => response.json())
}

export const uploadLabConfig = file => {
  const formData = new FormData()
  formData.append('File', file)
  return fetch(apiUrl + 'uploadLabConfig', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const downloadLabConfig = name => {
  const url = apiUrl + 'downloadLabConfig/' + name
  downloadFileFromURL(name, url)
}

export const getLogs = callback => {
  return fetch(apiUrl + 'log')
    .then(response => response.json())
    .then(data => callback(data))
}
