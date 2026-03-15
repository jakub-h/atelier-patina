document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.photo-slot input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function () {
            var slot = input.closest('.photo-slot');
            var nameEl = slot.querySelector('.photo-slot-name');
            if (input.files.length > 0) {
                slot.classList.add('has-file');
                nameEl.textContent = input.files[0].name;
                nameEl.title = input.files[0].name;
            } else {
                slot.classList.remove('has-file');
                nameEl.textContent = 'Foto ' + input.name.replace('foto_', '');
                nameEl.title = '';
            }
        });
    });
});
