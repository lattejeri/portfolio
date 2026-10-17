// Sidebar navigation: show one page at a time, driven by the URL hash (#font, #colour…).
(() => {
  const pages = [...document.querySelectorAll('.page')];
  const links = [...document.querySelectorAll('.sidebar ul a')];
  document.documentElement.classList.add('js');

  const show = () => {
    const id = location.hash.slice(1);
    const page = pages.find((p) => p.dataset.page === id) ?? pages[0];
    pages.forEach((p) => p.classList.toggle('is-active', p === page));
    links.forEach((a) => (a.hash === `#${page.dataset.page}` ? a.setAttribute('aria-current', 'page') : a.removeAttribute('aria-current')));
    document.title = `${page.querySelector('h1').textContent} · Research HQ global styling`;
    fit();
  };

  // Report mock-ups are drawn at 1160px wide; scale them down to fit narrower screens.
  const fit = () => {
    for (const box of document.querySelectorAll('.page.is-active .mock-fit')) {
      const report = box.firstElementChild;
      const scale = Math.min(1, box.clientWidth / 1160);
      report.style.setProperty('--fit', scale);
      box.style.height = `${report.offsetHeight * scale}px`;
    }
  };

  addEventListener('hashchange', () => { show(); scrollTo(0, 0); });
  addEventListener('resize', fit);
  show();
})();
