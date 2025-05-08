document.addEventListener("DOMContentLoaded", function() {
    fetch('menu.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('navbar').innerHTML = data;
        // Remove is-preload as soon as menu is ready
        document.body.classList.remove('is-preload');
        // Now that the menu is loaded, load your main JS
        var script = document.createElement('script');
        script.src = 'assets/js/main.js';
        document.body.appendChild(script);
    });
});
