/* Zgoda na pliki cookies – baner, zapis wyboru i ładowanie treści zewnętrznych
   (mapa Google, widget ZnanyLekarz) dopiero po akceptacji. */
(function () {
  'use strict';

  var KEY = 'oc_cookie_consent';
  var POLICY = 'assets/downloads/Polityka cookies serwisu OrthoCare.pdf';
  var MAPS_FALLBACK = 'https://maps.google.com/?q=ul.+D\u0119bowa+2,+26-600+Radom';

  function read() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function write(value) {
    try { localStorage.setItem(KEY, value); } catch (e) { /* tryb prywatny / brak storage */ }
  }

  var api = {
    get: read,
    accepted: function () { return read() === 'accepted'; },
    rejected: function () { return read() === 'rejected'; },
    open: showBanner,
    accept: accept,
    reject: reject
  };
  window.OCConsent = api;

  /* ---------- baner ---------- */
  var banner = null;
  var lastFocus = null;

  function buildBanner() {
    if (banner) return banner;
    banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.className = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-labelledby', 'cookie-banner-title');
    banner.setAttribute('aria-describedby', 'cookie-banner-text');
    banner.setAttribute('tabindex', '-1');
    banner.hidden = true;
    banner.innerHTML =
      '<div class="cookie-banner__inner">' +
        '<div class="cookie-banner__content">' +
          '<p class="cookie-banner__title" id="cookie-banner-title">Pliki cookies</p>' +
          '<p class="cookie-banner__text" id="cookie-banner-text">' +
            'Ta strona korzysta z niezb\u0119dnych plik\u00f3w cookies. Za Twoj\u0105 zgod\u0105 wczytamy r\u00f3wnie\u017c tre\u015bci zewn\u0119trzne ' +
            '(map\u0119 Google oraz formularz rezerwacji wizyt ZnanyLekarz), kt\u00f3re mog\u0105 zapisywa\u0107 w\u0142asne pliki cookies. ' +
            'Szczeg\u00f3\u0142y znajdziesz w dokumencie ' +
            '<a href="' + POLICY + '" target="_blank" rel="noopener">Polityka cookies</a>.' +
          '</p>' +
        '</div>' +
        '<div class="cookie-banner__actions">' +
          '<button type="button" class="btn btn--outline cookie-banner__btn" data-cookie-reject>Odrzucam</button>' +
          '<button type="button" class="btn btn--primary cookie-banner__btn" data-cookie-accept>Akceptuj\u0119</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(banner);
    return banner;
  }

  function showBanner() {
    var el = buildBanner();
    if (!el.hidden) return;
    lastFocus = document.activeElement;
    el.hidden = false;
    document.body.classList.add('has-cookie-banner');
    var first = el.querySelector('[data-cookie-accept]');
    window.setTimeout(function () { (first || el).focus(); }, 30);
  }

  function hideBanner() {
    if (!banner || banner.hidden) return;
    banner.hidden = true;
    document.body.classList.remove('has-cookie-banner');
    if (lastFocus && typeof lastFocus.focus === 'function' && document.contains(lastFocus)) {
      lastFocus.focus();
    }
    lastFocus = null;
  }

  function dispatch(value) {
    var evt;
    try {
      evt = new CustomEvent('oc:consent', { detail: { value: value } });
    } catch (e) {
      evt = document.createEvent('CustomEvent');
      evt.initCustomEvent('oc:consent', false, false, { value: value });
    }
    document.dispatchEvent(evt);
  }

  function accept() {
    write('accepted');
    hideBanner();
    loadMaps();
    dispatch('accepted');
  }

  function reject() {
    write('rejected');
    hideBanner();
    dispatch('rejected');
  }

  /* ---------- mapa Google ---------- */
  function mapPlaceholderHtml(link) {
    return (
      '<div class="map-consent__box">' +
        '<p class="map-consent__text">Aby wy\u015bwietli\u0107 map\u0119, zaakceptuj pliki cookies.</p>' +
        '<div class="map-consent__actions">' +
          '<button type="button" class="btn btn--primary" data-cookie-accept>Akceptuj\u0119</button>' +
          '<a class="btn btn--outline" href="' + link + '" target="_blank" rel="noopener">Otw\u00f3rz w Google Maps</a>' +
        '</div>' +
      '</div>'
    );
  }

  function prepareMaps() {
    var nodes = document.querySelectorAll('[data-consent-map]');
    Array.prototype.forEach.call(nodes, function (node) {
      if (node.getAttribute('data-ready')) return;
      node.setAttribute('data-ready', '1');
      if (!node.innerHTML.trim()) {
        node.innerHTML = mapPlaceholderHtml(node.getAttribute('data-map-link') || MAPS_FALLBACK);
      }
    });
  }

  function loadMaps() {
    var nodes = document.querySelectorAll('[data-consent-map]');
    Array.prototype.forEach.call(nodes, function (node) {
      var src = node.getAttribute('data-map-src');
      if (!src || node.querySelector('iframe')) return;
      var iframe = document.createElement('iframe');
      iframe.src = src;
      iframe.title = node.getAttribute('data-map-title') || 'Mapa';
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('loading', 'lazy');
      iframe.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
      node.innerHTML = '';
      node.appendChild(iframe);
      node.classList.add('map-consent--loaded');
    });
  }

  /* ---------- start ---------- */
  function init() {
    prepareMaps();
    if (api.accepted()) {
      loadMaps();
    } else if (!api.rejected()) {
      showBanner();
    }

    document.addEventListener('click', function (e) {
      var t = e.target;
      if (!t || !t.closest) return;
      if (t.closest('[data-cookie-accept]')) { e.preventDefault(); accept(); return; }
      if (t.closest('[data-cookie-reject]')) { e.preventDefault(); reject(); return; }
      if (t.closest('[data-cookie-settings]')) { e.preventDefault(); showBanner(); }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
