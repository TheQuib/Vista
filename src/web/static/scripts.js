document.getElementById("clearDisplay-button").addEventListener("click", function() {
    fetch('/clear-display', {
        method: 'POST',
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
    });
});

document.getElementById("refreshDisplay-button").addEventListener("click", function() {
    fetch('/refresh-display', {
        method: 'POST',
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
    });
});

document.getElementById("settings-button").addEventListener("click", function() {
    window.location.href = '/settings';
});

