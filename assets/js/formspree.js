document.addEventListener('DOMContentLoaded', function() {
    const actualBtn = document.getElementById('files');
    const fileChosen = document.getElementById('file-chosen');

    if (actualBtn && fileChosen) {
        actualBtn.addEventListener('change', function(){
            if(this.files.length > 0) {
                fileChosen.innerHTML = '';
                Array.from(this.files).forEach(file => {
                    const tag = document.createElement('span');
                    tag.className = 'file-tag';
                    tag.textContent = file.name;
                    fileChosen.appendChild(tag);
                });
            } else {
                fileChosen.textContent = 'Žádný soubor nevybrán';
            }
        });
    }
});
