export const apiUrl = 'http://' + window.location.hostname + ':5000/';

export const getStatus = (setter) => {
    fetch(apiUrl + "status")
      .then((response) => response.json())
      .then((data) => setter(data));
  };