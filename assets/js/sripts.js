// window.addEventListener('DOMContentLoaded', function() {
//     function setViewportScale() {
//       const screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
  
//       let viewportTag = document.querySelector('meta[name="viewport"]');
//       let viewportContent = 'width=device-width, initial-scale=1.0';
  
//       if (screenWidth < 370) {
//         viewportContent = 'width=device-width, initial-scale=0.8'; // Измените значение 1.2 на желаемый масштаб
//       }
  
//       if (!viewportTag) {
//         viewportTag = document.createElement('meta');
//         viewportTag.setAttribute('name', 'viewport');
//         document.head.appendChild(viewportTag);
//       }
  
//       viewportTag.setAttribute('content', viewportContent);
//     }
  
//     setViewportScale();
  
//     window.addEventListener('resize', setViewportScale);
//   });
var lastScrollPosition = 0;
var scrollThreshold = 90;

window.addEventListener('scroll', function() {
  var nav = document.querySelector('.navigation');
  var currentScrollPosition = window.pageYOffset;
  var scrollDifference = Math.abs(currentScrollPosition - lastScrollPosition);

  if (scrollDifference >= scrollThreshold) {
    if (currentScrollPosition < lastScrollPosition) {
      // Скролл вверх
      nav.classList.remove('swipe');
    } else {
      // Скролл вниз
      nav.classList.add('swipe');
    }

    // Обновление позиции скролла для следующего события
    lastScrollPosition = currentScrollPosition;
  }
});

const navBurger = document.querySelector('.nav-burgers');
const closeNavBurger = document.querySelector('.close-nav-burgers');
const modal = document.querySelector('.modal-catalog');
const closeModalCatalog = document.querySelector('.modal-close')

closeModalCatalog.addEventListener('ontouchstart', () => {
  modal.style.display = 'none'
})



navBurger.addEventListener('ontouchstart', function() {
  modal.style.display = 'flex'
  document.body.style.overflow = 'hidden';
});

closeNavBurger.addEventListener('ontouchstart', function() {
  modal.classList.remove('open-modal');
  document.body.classList.remove('modal-show');
  document.body.style.overflow = 'none';
});

