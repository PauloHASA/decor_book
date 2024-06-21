document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll(".lazy");

    const lazyLoad = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const lazyImage = entry.target;
                lazyImage.src = lazyImage.dataset.src;
                lazyImage.classList.remove("lazy");
                observer.unobserve(lazyImage);

                lazyImage.addEventListener('load', function() {
                    lazyImage.classList.add('loaded');
                });
            }
        });
    });

    lazyImages.forEach(function(lazyImage) {
        lazyLoad.observe(lazyImage);
    });
});