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

  // Load contact settings (phone, vacation mode) from assets/js/site-config.js
  const configLoaded = new Promise(resolve => {
    const script = document.createElement('script');
    script.src = `${siteBase}/assets/js/site-config.js`;
    script.onload = resolve;
    script.onerror = () => {
      console.error('Error loading site config');
      resolve();
    };
    document.head.appendChild(script);
  });

  const footerLoaded = fetch(`${siteBase}/templates/footer.html`)
    .then(response => response.text())
    .then(data => {
      document.getElementById('footer').outerHTML = data;
    })
    .catch(error => {
      console.error('Error loading footer:', error);
    });

  Promise.all([configLoaded, footerLoaded]).then(applySiteConfig);
});

// Fill phone numbers and the vacation notice from window.SITE_CONFIG.
// Elements opt in via data attributes:
//   data-phone       – text is replaced with the current phone number
//   data-phone-link  – href becomes tel:<number>
//   data-whatsapp    – href becomes the WhatsApp link for the number
//   #vacation-notice – shown only while vacation mode is active
function applySiteConfig() {
  const config = window.SITE_CONFIG;
  if (!config) return;

  const vacation = config.vacation || {};
  const phone = vacation.active && vacation.phone ? vacation.phone : config.phone;
  const digits = phone.replace(/[^\d]/g, '');

  document.querySelectorAll('[data-phone]').forEach(el => {
    el.textContent = phone;
  });
  document.querySelectorAll('[data-phone-link]').forEach(el => {
    el.href = `tel:+${digits}`;
  });
  document.querySelectorAll('[data-whatsapp]').forEach(el => {
    el.href = `https://wa.me/${digits}`;
  });

  const notice = document.getElementById('vacation-notice');
  if (notice && vacation.active) {
    const until = vacation.until ? ` do <strong>${vacation.until}</strong>` : '';
    const call = vacation.phone
      ? `, případně volejte na číslo <a href="tel:+${digits}">${vacation.phone}</a>`
      : '';
    notice.innerHTML =
      `<h3>Jsme na dovolené${until}</h3>` +
      `<p>Pište nám prosím na <a href="mailto:patina.restaurovani@gmail.com">patina.restaurovani@gmail.com</a>${call}. Děkujeme za pochopení!</p>`;
    notice.hidden = false;
  }
}
