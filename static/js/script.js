  const toggleBtn = document.getElementById('menuToggle');
  const navbarCollapse = document.getElementById('navbarNav');

  toggleBtn.addEventListener('click', () => {
    toggleBtn.classList.toggle('menu-toggle-active');
  });

  // Optional: reset toggle icon when navbar closes
  navbarCollapse.addEventListener('hidden.bs.collapse', () => {
    toggleBtn.classList.remove('menu-toggle-active');
  });
