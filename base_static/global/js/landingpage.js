
document.addEventListener("DOMContentLoaded", function() {
    const seeMoreBtn = document.getElementById("see-more");
    const backToUpBtn = document.getElementById("back-to-up");
    const section1 = document.getElementById("section-1");
    const section2 = document.getElementById("section-2");
    const body = document.body;

    seeMoreBtn.addEventListener("click", function(event) {
        event.preventDefault(); 
        section1.style.display = "none";
        section2.style.display = "block"; 
        body.classList.add("overflow-y"); 
    });

    backToUpBtn.addEventListener("click", function(event) {
        event.preventDefault(); 
        section2.style.display = "none";
        section1.style.display = "flex"; 
        body.classList.remove("overflow-y"); 
    });
});