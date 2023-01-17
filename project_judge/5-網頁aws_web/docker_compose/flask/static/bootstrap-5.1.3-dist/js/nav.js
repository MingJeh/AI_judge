const sidebar = document.querySelector(".sidebar");

if (sidebar) {
  const init = () => {
    attachEvents();
  };

  const hamburgerMenu = document.querySelector(".hamburger-menu");
  const hamburgerMenuContainer = document.querySelector(
    ".hamburger-menu__container"
  );
  const nav = document.querySelector(".nav");

  const attachEvents = () => {
    hamburgerMenuContainer.addEventListener("click", toggleMenu);
  };

  const toggleMenu = () => {
    hamburgerMenu.classList.toggle("hamburger-menu--open");
    nav.classList.toggle("nav--open");
  };

  init();
}
