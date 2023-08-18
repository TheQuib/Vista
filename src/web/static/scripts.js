document.getElementById("clearDisplay-button").addEventListener("click", function() {
    fetch('/clear-display', {
      method: 'POST',
    })
    .then(response => response.text())
    .then(data => {
      console.log(data); // Log the response from the server
      // You can update the UI here if needed
    });
  });