let currentSlide = 0;
const slidesContainer = document.querySelector('.slides-container');
const slideWidth = document.querySelector('.slide').offsetWidth;
const totalSlides = document.querySelectorAll('.slide').length;

function showSlide(index) {
  const newPosition = -index * slideWidth + 'px';
  slidesContainer.style.transform = 'translateX(' + newPosition + ')';
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % totalSlides;
  showSlide(currentSlide);
}

function prevSlide() {
  currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
  showSlide(currentSlide);
}

showSlide(currentSlide);
