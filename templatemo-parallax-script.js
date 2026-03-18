/* ==========================================================================
 Parallax + EmailJS Submit Handler — FIXED
 ========================================================================== */
(function () {
  'use strict';
  var nav = document.getElementById('templatemo-nav');
  var navToggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');
  var navItems = document.querySelectorAll('.nav-links a');
  var sections = document.querySelectorAll('.parallax-section');
  var parallaxBgs = document.querySelectorAll('.parallax-bg');
  var revealElements = document.querySelectorAll('.section-content');
  var isMobile = /Android|iPhone|iPad|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth <= 768;
  var ticking = false;
  function updateParallax() {
    if (isMobile) return;
    var windowHeight = window.innerHeight;
    parallaxBgs.forEach(function (bg) {
      var section = bg.parentElement;
      var rect = section.getBoundingClientRect();
      if (rect.bottom < -300 || rect.top > windowHeight + 300) return;
      var speed = parseFloat(bg.getAttribute('data-speed')) || 0.5;
      var sectionCenterY = rect.top + rect.height / 2;
      var viewportCenterY = windowHeight / 2;
      var offset = sectionCenterY - viewportCenterY;
      var totalTravel = windowHeight + rect.height;
      var normalized = Math.max(-1, Math.min(1, offset / (totalTravel / 2)));
      var translateY = normalized * (windowHeight * speed);
      bg.style.transform = 'translate3d(0,' + translateY.toFixed(1) + 'px,0)';
    });
    ticking = false;
  }
  function onScroll() { if (!ticking) { window.requestAnimationFrame(updateParallax); ticking = true; } }
  if (!isMobile) { window.addEventListener('scroll', onScroll, { passive: true }); updateParallax(); }
  window.addEventListener('resize', function () {
    isMobile = window.innerWidth <= 768;
    if (!isMobile) updateParallax(); else parallaxBgs.forEach(function (bg) { bg.style.transform = 'translate3d(0,0,0)'; });
  });
  function handleNavScroll() { if (window.scrollY > 80) nav.classList.add('scrolled'); else nav.classList.remove('scrolled'); }
  window.addEventListener('scroll', handleNavScroll, { passive: true });
  handleNavScroll();
  if (navToggle) { navToggle.addEventListener('click', function () { navToggle.classList.toggle('active'); navLinks.classList.toggle('open'); }); }
  navItems.forEach(function (link) { link.addEventListener('click', function () { navToggle.classList.remove('active'); navLinks.classList.remove('open'); }); });
  function updateActiveLink() {
    var scrollPos = window.scrollY + window.innerHeight / 3;
    sections.forEach(function (section) {
      var top = section.offsetTop, height = section.offsetHeight, id = section.getAttribute('id');
      if (scrollPos >= top && scrollPos < top + height) {
        navItems.forEach(function (link) {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) link.classList.add('active');
        });
      }
    });
  }
  window.addEventListener('scroll', updateActiveLink, { passive: true });
  updateActiveLink();
  revealElements.forEach(function (el) { el.classList.add('reveal'); });
  function checkReveal() {
    var windowHeight = window.innerHeight, revealPoint = 120;
    revealElements.forEach(function (el) { var elementTop = el.getBoundingClientRect().top; if (elementTop < windowHeight - revealPoint) el.classList.add('visible'); });
  }
  window.addEventListener('scroll', checkReveal, { passive: true });
  checkReveal();
  function showToast(msg) {
    var el = document.getElementById('toast'); if (!el) { alert(msg); return; }
    el.textContent = msg; el.classList.add('show');
    setTimeout(function(){ el.classList.remove('show'); }, 2800);
  }
  var contactForm = document.getElementById('contactForm');
  function emailjsReady() {
    return typeof window.emailjs !== 'undefined' && typeof window.emailjs.send === 'function';
  }
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = contactForm.querySelector("input[name='name']").value.trim();
      var email = contactForm.querySelector("input[name='email']").value.trim();
      var message = contactForm.querySelector("textarea[name='message']").value.trim();
      if (!name || !email || !message) { showToast('Please fill out all fields.'); return; }
      if (!emailjsReady()) { console.error('EmailJS SDK not loaded or not initialized'); showToast('Unable to send right now. Please try again later.'); return; }
      var SERVICE_ID = 'service_3kflnuh';
      var TEMPLATE_ID = 'template_un57291';
      var PUBLIC_KEY  = 'pEt0L5IFostMcoXno';
      var params = { name: name, email: email, message: message, to_email: 'info@octos.at' };
      console.log('Sending with PUBLIC_KEY:', PUBLIC_KEY);
      emailjs.send(SERVICE_ID, TEMPLATE_ID, params, PUBLIC_KEY)
        .then(function () { showToast('Thank you! Your message has been sent.'); contactForm.reset(); })
        .catch(function (err) { console.error('EmailJS error:', err); var msg = (err && (err.text || err.message)) ? String(err.text || err.message) : 'Sorry, something went wrong. Please try again later.'; showToast(msg); });
    });
  }
})();
