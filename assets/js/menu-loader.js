document.addEventListener("DOMContentLoaded", function() {
    // Get the base URL for the site
    const hostname = window.location.hostname;

    // Determine the base path based on the environment
    let siteBase = '';
    if (hostname.includes('github.io')) {
        siteBase = '/atelier-patina';
    } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
        siteBase = ''; // Local development
    } else {
        siteBase = ''; // Custom domain
    }

    fetch(`${siteBase}/templates/menu.html`)
    .then(response => response.text())
    .then(data => {
        document.getElementById('navbar').innerHTML = data;

        // Update all links with data-base-path attribute
        document.querySelectorAll('a[data-base-path]').forEach(link => {
            const currentHref = link.getAttribute('href');
            link.setAttribute('href', `${siteBase}/${currentHref}`);
        });

        // Remove is-preload as soon as menu is ready
        document.body.classList.remove('is-preload');
        // Now that the menu is loaded, load your main JS
        var script = document.createElement('script');
        script.src = `${siteBase}/assets/js/main.js`;
        document.body.appendChild(script);
    })
    .catch(error => {
        console.error('Error loading menu:', error);
    });
});
