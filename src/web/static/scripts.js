document.getElementById("clearDisplay-button").addEventListener("click", function() {
    fetch('/clear-display', {
      method: 'POST',
    })
    .then(response => response.text())
    .then(data => {
      console.log(data); // Log the response from the server
    });
  });

document.getElementById("refreshDisplay-button").addEventListener("click", function() {
  fetch('/refresh-display', {
    method: 'POST',
  })
  .then(response => response.text())
  .then(data => {
    console.log(data); // Log the response from the server
  });
});