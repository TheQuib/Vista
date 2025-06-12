document.getElementById("refreshDisplay-button").addEventListener("click", function() {
    fetch('/refresh-display', {
        method: 'POST',
    })
    .then(response => response.text())
    .then(data => {
        alert('Display refreshed');
    });
});

