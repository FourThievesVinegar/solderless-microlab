import { MicrolabStatusResponse, MicrolabRecipe } from './microlabTypes'

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

export const getStatus = (callback: (data: MicrolabStatusResponse) => void, handleGetStatusError: () => void) => {
  fetch(apiUrl + 'status')
    .then(response => response.json())
    .then(data => callback(data))
    .catch(rejected => {
      console.error('Error fetching status', rejected)
      handleGetStatusError()
      window.setTimeout(() => {
        // Try again in a few seconds
        getStatus(callback, handleGetStatusError)
      }, 5000)
    })
}

export const getRecipe = (recipeName: string): Promise<MicrolabRecipe> => {
  return fetch(apiUrl + 'recipe/' + recipeName).then(response => response.json())
}

export const listRecipes = (callback: (data: string[]) => void) => {
  fetch(apiUrl + 'list') //this route returns an array with all the names ex: ['recipe1',recipe2']
    .then(response => response.json())
    .then(data => callback(data))
}

export const deleteRecipe = (recipeName: string): Promise<MicrolabRecipe> => {
  return fetch(apiUrl + 'deleteRecipe/' + recipeName, {
    method: 'DELETE',
  }).then(response => response.json())
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
  return fetch(apiUrl + 'start/' + name, {
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

export const getControllerHardware = (): Promise<{ controllerHardware: string }> => {
  return fetch(apiUrl + 'controllerHardware').then(response => response.json())
}

export const listControllerHardware = (): Promise<string[]> => {
  return fetch(apiUrl + 'controllerHardware/list').then(response => response.json())
}

export const setControllerHardware = (name: string): Promise<{ response: 'ok' | 'error'; message?: string }> => {
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

export const getLabHardware = (): Promise<{ labHardware: string }> => {
  return fetch(apiUrl + 'labHardware').then(response => response.json())
}

export const listLabHardware = (): Promise<string[]> => {
  return fetch(apiUrl + 'labHardware/list').then(response => response.json())
}

export const setLabHardware = (name: string): Promise<{ response: 'ok' | 'error'; message?: string }> => {
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

export const reloadHardware = (): Promise<{ response: 'ok' | 'error'; message?: string }> => {
  return fetch(apiUrl + 'reloadHardware', {
    method: 'POST',
  }).then(response => response.json())
}

export const getLogs = (callback: (data: { logs: string }) => void) => {
  return fetch(apiUrl + 'log')
    .then(response => response.json())
    .then(data => callback(data))
}

/*
 *   STRING MANIPULATION
 */

export const capitalize = (string: string) => {
  return string.charAt(0).toUpperCase() + string.slice(1)
}
