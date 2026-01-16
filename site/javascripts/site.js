// Add page scope classes based on URL path
(function () {
  const p = window.location.pathname;

  // GitHub Pages often has /<repo>/ prefix, so just check contains "/projects/"
  if (p.includes("/projects/")) {
    document.body.classList.add("is-projects");
  }
})();
