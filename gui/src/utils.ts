export const apiUrl = 'http://' + window.location.hostname + ':8081/'

export const downloadFileFromURL = (fileName: string, url: string) => {
  const link = document.createElement('a')
  link.download = fileName
  link.href = url
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  link.remove()
}

export const getStatus = (callback: (data: any) => void) => {
  fetch(apiUrl + 'status')
    .then(response => response.json())
    .then(data => callback(data))
}

export const listRecipes = (callback: (data: any) => void) => {
  fetch(apiUrl + 'list') //this route returns an array with all the names ex: ['recipe1',recipe2']
    .then(response => response.json())
    .then(data => callback(data))
}

export const selectOption = (option: string) => {
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

export const startRecipe = (name: string) => {
  fetch(apiUrl + 'start/' + name, {
    method: 'POST',
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const uploadRecipe = (file: string | Blob | File) => {
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

export const setControllerHardware = (name: string) => {
  return fetch(apiUrl + 'controllerHardware/' + name, {
    method: 'POST',
  }).then(response => response.json())
}

export const downloadControllerConfig = (name: string) => {
  const url = apiUrl + 'downloadControllerConfig/' + name
  downloadFileFromURL(name, url)
}

export const uploadControllerConfig = (file: string | Blob | File) => {
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

export const setLabHardware = (name: string) => {
  return fetch(apiUrl + 'labHardware/' + name, {
    method: 'POST',
  }).then(response => response.json())
}

export const uploadLabConfig = (file: string | Blob | File) => {
  const formData = new FormData()
  formData.append('File', file)
  return fetch(apiUrl + 'uploadLabConfig', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => console.log(data))
}

export const downloadLabConfig = (name: string) => {
  const url = apiUrl + 'downloadLabConfig/' + name
  downloadFileFromURL(name, url)
}

export const reloadHardware = () => {
  return fetch(apiUrl + 'reloadHardware', {
    method: 'POST',
  }).then(response => response.json())
}

export const getLogs = (callback: (data: any) => void) => {
  return fetch(apiUrl + 'log')
    .then(response => response.json())
    .then(data => callback(data))
}
