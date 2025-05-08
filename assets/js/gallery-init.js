import PhotoSwipeLightbox from './photoswipe-lightbox.esm.js';
const lightbox = new PhotoSwipeLightbox({
  gallery: '#portfolio-gallery',
  children: 'a',
  pswpModule: () => import('./photoswipe.esm.js')
});
lightbox.init();
