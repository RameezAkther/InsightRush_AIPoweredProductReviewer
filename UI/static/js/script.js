document.addEventListener('DOMContentLoaded', function() {
    const sliders = document.querySelectorAll('.slider');
    const prevButtons = document.querySelectorAll('.prev1');
    const nextButtons = document.querySelectorAll('.next1');

    sliders.forEach((slider, index) => {
        let currentSlideIndex = 0;
        const slides = slider.querySelectorAll('.slide');
        const totalSlides = slides.length;

        function showSlide(slideIndex) {
            slides.forEach((slide, i) => {
                if (i === slideIndex) {
                    slide.style.display = 'block';
                } else {
                    slide.style.display = 'none';
                }
            });
        }

        prevButtons[index].addEventListener('click', () => {
            currentSlideIndex = (currentSlideIndex - 1 + totalSlides) % totalSlides;
            showSlide(currentSlideIndex);
        });

        nextButtons[index].addEventListener('click', () => {
            currentSlideIndex = (currentSlideIndex + 1) % totalSlides;
            showSlide(currentSlideIndex);
        });

        // Show the initial slide
        showSlide(currentSlideIndex);
    });
});
