document.addEventListener("DOMContentLoaded", function() {
  fetch('/templates/footer.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('footer').outerHTML = data;
    });
});
