// Add page scope classes based on URL path
(function () {
  const p = window.location.pathname;

  // GitHub Pages often has /<repo>/ prefix, so just check contains "/projects/"
  if (p.includes("/projects/")) {
    document.body.classList.add("is-projects");
  }
})();

// Global image lightbox for portfolio content.
(function () {
  let overlay;
  let preview;
  let caption;
  let counter;
  let previousButton;
  let nextButton;
  let closeButton;
  let pageImages = [];
  let currentIndex = 0;
  let returnFocus = null;

  function isEligibleImage(image) {
    return Boolean(
      image &&
      image.closest(".md-content") &&
      !image.closest(".site-lightbox") &&
      !image.matches(".twemoji, .emoji, [data-no-lightbox]")
    );
  }

  function getPageImages() {
    return Array.from(document.querySelectorAll(".md-content img")).filter(isEligibleImage);
  }

  function getCaption(image) {
    const figureCaption = image.closest("figure")?.querySelector("figcaption");
    return (figureCaption?.textContent || image.alt || "Image preview").trim();
  }

  function ensureLightbox() {
    if (overlay) return;

    overlay = document.createElement("div");
    overlay.className = "site-lightbox";
    overlay.hidden = true;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Expanded image viewer");
    overlay.innerHTML = `
      <div class="site-lightbox__toolbar">
        <span class="site-lightbox__counter" aria-live="polite"></span>
        <button class="site-lightbox__close" type="button" aria-label="Close expanded image">Close</button>
      </div>
      <figure class="site-lightbox__stage">
        <img class="site-lightbox__image" alt="">
        <figcaption class="site-lightbox__caption"></figcaption>
      </figure>
      <div class="site-lightbox__navigation">
        <button class="site-lightbox__previous" type="button">Previous</button>
        <button class="site-lightbox__next" type="button">Next</button>
      </div>
    `;

    document.body.appendChild(overlay);
    preview = overlay.querySelector(".site-lightbox__image");
    caption = overlay.querySelector(".site-lightbox__caption");
    counter = overlay.querySelector(".site-lightbox__counter");
    previousButton = overlay.querySelector(".site-lightbox__previous");
    nextButton = overlay.querySelector(".site-lightbox__next");
    closeButton = overlay.querySelector(".site-lightbox__close");

    closeButton.addEventListener("click", closeLightbox);
    preview.addEventListener("click", closeLightbox);
    previousButton.addEventListener("click", function () { move(-1); });
    nextButton.addEventListener("click", function () { move(1); });
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeLightbox();
    });
  }

  function renderCurrentImage() {
    const sourceImage = pageImages[currentIndex];
    if (!sourceImage) return;

    preview.src = sourceImage.currentSrc || sourceImage.src;
    preview.alt = sourceImage.alt || "Expanded image";
    caption.textContent = getCaption(sourceImage);
    counter.textContent = `${currentIndex + 1} / ${pageImages.length}`;

    const hasMultipleImages = pageImages.length > 1;
    previousButton.hidden = !hasMultipleImages;
    nextButton.hidden = !hasMultipleImages;
  }

  function openLightbox(image) {
    ensureLightbox();
    pageImages = getPageImages();
    currentIndex = Math.max(0, pageImages.indexOf(image));
    returnFocus = document.activeElement;
    renderCurrentImage();
    overlay.hidden = false;
    document.body.classList.add("site-lightbox-open");
    closeButton.focus();
  }

  function closeLightbox() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    preview.removeAttribute("src");
    document.body.classList.remove("site-lightbox-open");
    if (returnFocus && typeof returnFocus.focus === "function") returnFocus.focus();
  }

  function move(direction) {
    if (pageImages.length < 2) return;
    currentIndex = (currentIndex + direction + pageImages.length) % pageImages.length;
    renderCurrentImage();
  }

  document.addEventListener("click", function (event) {
    const image = event.target.closest("img");
    if (!isEligibleImage(image)) return;
    event.preventDefault();
    openLightbox(image);
  });

  document.addEventListener("keydown", function (event) {
    if (!overlay || overlay.hidden) return;
    if (event.key === "Escape") closeLightbox();
    if (event.key === "ArrowLeft") move(-1);
    if (event.key === "ArrowRight") move(1);
  });
})();
