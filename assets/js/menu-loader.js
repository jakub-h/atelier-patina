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
        // Check if this is the index page (has banner)
        const isIndexPage = document.getElementById('banner') !== null;

        // If it's the index page, add the 'alt' class to preserve animation
        if (isIndexPage) {
            data = data.replace('<header id="header">', '<header id="header" class="alt">');
        }

        // Fix logo path for gallery pages (they're in gallery_pages/ subdirectory)
        const currentPath = window.location.pathname;
        if (currentPath.includes('/gallery_pages/')) {
            // Gallery pages need to go up one directory level for images
            data = data.replace('src="images/logo.svg"', 'src="../images/logo.svg"');
        }

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
