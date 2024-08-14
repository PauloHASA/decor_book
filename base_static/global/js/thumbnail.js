        
var mainImage = document.getElementById("main-image");
var thumbnails = document.querySelectorAll('.thumbnail');


thumbnails.forEach(function(thumbnail) {
    thumbnail.addEventListener('click', function(event) {
        event.preventDefault(); 
        var newImageUrl = this.getAttribute('data-image'); 
        mainImage.src = newImageUrl; 
    });
});
