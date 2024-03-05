document.addEventListener('DOMContentLoaded', function() {
    var dropBox = document.getElementById('dropBox');
    var fileInput = document.getElementById('images');
    var imagePreviews = document.getElementById('imagePreviews');

    dropBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropBox.classList.add('dragover');
    });

    dropBox.addEventListener('dragleave', function() {
        dropBox.classList.remove('dragover');
    });

    dropBox.addEventListener('drop', function(e) {
        e.preventDefault();
        dropBox.classList.remove('dragover');
        var files = e.dataTransfer.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        var files = this.files;
        handleFiles(files);
    });

    function handleFiles(files) {
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            if (file.type.startsWith('image/')) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var img = document.createElement('img');
                    img.src = e.target.result;
                    var preview = document.createElement('div');
                    preview.classList.add('image-preview');
                    preview.appendChild(img);
                    var cancelBtn = document.createElement('button');
                    cancelBtn.textContent = 'X';
                    cancelBtn.addEventListener('click', function() {
                        imagePreviews.removeChild(preview);
                    });
                    preview.appendChild(cancelBtn);
                    imagePreviews.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        }
    }
});
