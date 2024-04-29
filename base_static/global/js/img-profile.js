$(document).ready(function(){
    $('#profile-picture-input').change(function(event){
        var input = event.target;
        var reader = new FileReader();
        reader.onload = function(){
            var dataURL = reader.result;
            $('#profile-image').attr('src', dataURL);
        };
        reader.readAsDataURL(input.files[0]);
    });
});
