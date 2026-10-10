// forms: open the visitor's email app with all filled-in fields (no data passes through the site)
function mailForm(form, subject) {
  var lines = [];
  var label = function (el) {
    var l = el.id && document.querySelector('label[for="' + el.id + '"]');
    if (el.type === 'radio' || el.type === 'checkbox') { var c = el.closest('label'); var b = c && c.querySelector('b'); return b ? b.textContent : (c ? c.textContent : el.name); }
    return l ? l.textContent : el.name;
  };
  var legend = function (el) { var fs = el.closest('fieldset'); var lg = fs && fs.querySelector('legend'); return lg ? lg.textContent.replace(/^\d+\s*/, '').trim() : ''; };
  Array.prototype.forEach.call(form.elements, function (el) {
    if (!el.id && !el.name || el.disabled || el.type === 'submit' || el.tagName === 'BUTTON' || el.tagName === 'FIELDSET') return;
    if (el.type === 'radio') { if (el.checked) lines.push(legend(el) + ': ' + label(el)); return; }
    var de = document.documentElement.lang === 'de';
    if (el.type === 'checkbox') {
      if (!el.checked) return;
      var q = document.getElementById(el.id + '-q');
      lines.push(label(el) + ': ' + (q ? q.value + (de ? ' Stück' : ' pcs') : (de ? 'ja' : 'yes')));
      return;
    }
    if (/-q$/.test(el.id) && document.getElementById(el.id.slice(0, -2))) return;
    var v = (el.tagName === 'SELECT' ? el.options[el.selectedIndex].text : el.value || '').trim();
    if (v) lines.push(label(el).trim() + ': ' + (el.tagName === 'TEXTAREA' ? '\n' + v + '\n' : v));
  });
  location.href = 'mailto:info@octos.at?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
}

(function () {
  var de = document.documentElement.lang === 'de';

  // mobile menu
  var top = document.querySelector('.top');
  var mb = document.querySelector('.menu-btn');
  if (mb) mb.addEventListener('click', function () {
    var open = top.classList.toggle('open');
    mb.setAttribute('aria-expanded', open ? 'true' : 'false');
    mb.textContent = open ? (de ? 'Schließen' : 'Close') : 'Menu';
  });

  // copy buttons
  function select(el) { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  document.querySelectorAll('.copy').forEach(function (b) {
    var label = b.textContent;
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-copy');
      var done = function () { b.textContent = de ? 'Kopiert' : 'Copied'; setTimeout(function () { b.textContent = label; }, 1600); };
      try { navigator.clipboard.writeText(t).then(done, function () { select(b.previousElementSibling); }); }
      catch (e) { select(b.previousElementSibling); }
    });
  });

  // inquiry form: checks input, then opens the email app
  var f = document.getElementById('inq');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var n = document.getElementById('q-note');
    var idea = document.getElementById('q-idea').value.trim();
    var mail = document.getElementById('q-mail').value.trim();
    if (!idea || !/.+@.+\..+/.test(mail)) {
      n.className = 'note';
      n.textContent = de ? 'Bitte beschreiben Sie kurz Ihre Idee und geben Sie eine gültige E-Mail-Adresse an, damit wir antworten können.'
                         : 'Add a short description of your idea and a valid email so we can reply.';
      return;
    }
    n.className = 'note ok';
    var who = document.getElementById('q-co').value.trim() || document.getElementById('q-name').value.trim();
    mailForm(f, (de ? 'Projektanfrage' : 'Project inquiry') + (who ? ': ' + who : ''));
  });

  var v = document.querySelector('.stage video');
  if (v && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { v.removeAttribute('autoplay'); v.pause(); }
})();

// offer request form: checks input, then opens the email app
(function () {
  var de = document.documentElement.lang === 'de';
  var f = document.getElementById('offer');
  if (!f) return;
  [['o-ess', 'o-ess-q'], ['o-pow', 'o-pow-q']].forEach(function (p) {
    var c = document.getElementById(p[0]), q = document.getElementById(p[1]);
    var sync = function () { q.disabled = !c.checked; };
    c.addEventListener('change', sync); sync();
  });
  var docs = document.getElementById('o-docs-row');
  var showDocs = function () {
    var trade = document.getElementById('o-type-trade').checked;
    docs.hidden = !trade;
    if (!trade) document.getElementById('o-docs').checked = false;
  };
  document.querySelectorAll('input[name="o-type"]').forEach(function (r) { r.addEventListener('change', showDocs); });
  showDocs();
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (id) { return document.getElementById(id).value.trim(); };
    var n = document.getElementById('o-note');
    var any = document.getElementById('o-ess').checked || document.getElementById('o-pow').checked;
    var missing = [];
    if (!any) missing.push(de ? 'eine Version (Essential oder Power+)' : 'a version (Essential or Power+)');
    if (!v('o-co')) missing.push(de ? 'Firmenname' : 'company name');
    if (!v('o-name')) missing.push(de ? 'Ansprechperson' : 'contact name');
    if (!/.+@.+\..+/.test(v('o-mail'))) missing.push(de ? 'gültige E-Mail' : 'a valid email');
    if (!v('o-street') || !v('o-zip')) missing.push(de ? 'Adresse' : 'address');
    if (missing.length) {
      n.className = 'note err';
      n.textContent = (de ? 'Bitte ergänzen: ' : 'Please add: ') + missing.join(', ') + '.';
      return;
    }
    n.className = 'note ok';
    mailForm(f, (de ? 'Angebotsanfrage: OctoStool, ' : 'Offer request: OctoStool, ') + v('o-co'));
  });
})();

// contact form: preselect project size from ?slot= (links from the project slots tile)
(function () {
  var s = document.getElementById('q-slot');
  var m = /[?&]slot=([a-z]+)/.exec(location.search);
  if (s && m) s.value = m[1];
})();

// floating feel: grid drift, reveal on scroll, image parallax (skipped with reduced motion)
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var root = document.documentElement;

  // reveal: content floats up as it enters the viewport
  var sel = '.block-head, .card, .svc-group, .skills article, .facts > div, .kit li, .values article, .who-grid article, .case-grid > *, .two > *, .opts > *, .gallery figure, .buy > div, .map > *, .steps > *, .story > *, form.offer fieldset, .reel, .quote';
  var els = document.querySelectorAll(sel);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) {
      var i = 0, s = el.previousElementSibling;
      while (s && i < 4) { if (s.matches(sel)) i++; s = s.previousElementSibling; }
      el.style.setProperty('--rd', (i * 80) + 'ms');
      el.classList.add('rv'); io.observe(el);
    });
  }

  // parallax: large images drift slower than the page
  var px = Array.prototype.slice.call(document.querySelectorAll('.bleed > img, .case-hero img, .phead figure:not(.white):not(.founder-pic) img, .pic:not(.contain) img'));
  px.forEach(function (el) { el.classList.add('px'); });

  var ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY, vh = window.innerHeight;
    root.style.setProperty('--py', (-(y * 0.25) % 120) + 'px');
    px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var c = (r.top + r.height / 2 - vh / 2) / vh;  // -1..1 around viewport centre
      el.style.setProperty('--pxy', (c * -28).toFixed(1) + 'px');
    });
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  window.addEventListener('resize', frame);
  frame();
})();
