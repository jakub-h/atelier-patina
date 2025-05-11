document.addEventListener("DOMContentLoaded", function() {
  // Get the base URL for the site
  const baseUrl = window.location.href.substring(0, window.location.href.lastIndexOf('/'));
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

  fetch(`${siteBase}/templates/footer.html`)
    .then(response => response.text())
    .then(data => {
      document.getElementById('footer').outerHTML = data;
    })
    .catch(error => {
      console.error('Error loading footer:', error);
    });
});
