#!/usr/bin/env python3
"""Build multi-page OrthoCare site from shared templates and section files."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SECTIONS = SRC / "sections"

PAGES = {
    "o-nas.html": {
        "title": "O nas – Centrum Ortopedyczne OrthoCare – Radom",
        "active": "o-nas",
        "page_title": "O nas",
        "section": "o-nas.html",
        "narrow": False,
    },
    "zespol.html": {
        "title": "Lekarze – Centrum Ortopedyczne OrthoCare – Radom",
        "active": "lekarze",
        "page_title": "Lekarze",
        "section": "lekarze.html",
        "narrow": False,
    },
    "cennik.html": {
        "title": "Usługi i cennik – Centrum Ortopedyczne OrthoCare – Radom",
        "active": "cennik",
        "page_title": "Usługi i cennik",
        "section": "cennik.html",
        "narrow": True,
    },
    "zabiegi.html": {
        "title": "Zabiegi – Centrum Ortopedyczne OrthoCare – Radom",
        "active": "zabiegi",
        "page_title": "Zabiegi",
        "section": "zabiegi.html",
        "narrow": True,
    },
    "kriolezja.html": {
        "title": "Kriolezja – Centrum Ortopedyczne OrthoCare – Radom",
        "active": "kriolezja",
        "page_title": "Kriolezja",
        "section": "kriolezja.html",
        "narrow": False,
    },
}

NAV_LINKS = [
    ("o-nas", "O nas", "o-nas.html"),
    ("lekarze", "Lekarze", "zespol.html"),
    ("cennik", "Usługi i cennik", "cennik.html"),
    ("zabiegi", "Zabiegi", "zabiegi.html"),
    ("kriolezja", "Kriolezja", "kriolezja.html"),
]

LOGO = "assets/logo-orthocare.png"

HOME = """
  <section class="hero hero-desktop full-bleed">
    <picture>
      <source type="image/webp" srcset="assets/hero-desktop.webp">
      <img src="assets/hero-desktop.jpg" alt="OrthoCare centrum ortopedyczne" class="hero-desktop__img" fetchpriority="high" decoding="async" width="2800" height="1212" sizes="100vw" />
    </picture>
  </section>

  <section class="hero hero-mobile">
    <div class="hero-photos">
      <picture>
        <source type="image/webp" srcset="assets/hero-1.webp">
        <img src="assets/hero-1.jpg" alt="OrthoCare" decoding="async" width="720" height="850">
      </picture>
      <picture class="hero-center">
        <source type="image/webp" srcset="assets/hero-2.webp">
        <img src="assets/hero-2.jpg" alt="OrthoCare" class="hero-center" fetchpriority="high" decoding="async" width="720" height="850">
      </picture>
      <picture>
        <source type="image/webp" srcset="assets/hero-3.webp">
        <img src="assets/hero-3.jpg" alt="OrthoCare" decoding="async" width="720" height="850">
      </picture>
    </div>
    <div class="hero-plaque">
      <h1 class="hero-logo">
        <picture>
          <source type="image/webp" srcset="assets/logo-hero-white.webp">
          <img src="assets/logo-hero-white.png" alt="OrthoCare" width="819" height="149" decoding="async">
        </picture>
      </h1>
      <div class="hero-mobile-cta">
        <button type="button" class="btn btn--primary umow-wizyte-btn">Umów wizytę</button>
        <a href="o-nas.html" class="btn btn--outline">O nas</a>
      </div>
    </div>
  </section>

  <section class="intro-team-block">
    <div class="wrap">
      <div class="intro-text">
        <h2 class="intro-title">Medycyna oparta na doświadczeniu</h2>
        <div class="intro-body">
          <p>W OrthoCare łączymy nowoczesną ortopedię z indywidualnym podejściem do każdego pacjenta. Specjalizujemy się w małoinwazyjnych zabiegach, precyzyjnej diagnostyce i kompleksowej opiece nad narządem ruchu – od leczenia bólu kręgosłupa po artroskopię stawów.</p>
          <p>Tworzymy zespół lekarzy i specjalistów, którzy wierzą, że skuteczne leczenie zaczyna się od zaufania i czasu poświęconego pacjentowi. Pracujemy z pasją, bazując na wiedzy, doświadczeniu i najnowszych standardach medycyny.</p>
        </div>
        <p class="intro-cta-text">Poznaj nas bliżej i zobacz, jak możemy Ci pomóc</p>
        <div class="intro-actions">
          <button type="button" class="btn btn--primary umow-wizyte-btn">Umów wizytę</button>
          <a href="o-nas.html" class="btn btn--outline">O nas</a>
        </div>
      </div>
    </div>
  </section>

  <section class="intro-team-photo full-bleed">
    <img src="assets/team-photo.jpg" alt="Zespół lekarzy OrthoCare" class="intro-team-photo__img intro-team-photo__img--desktop" loading="lazy" decoding="async" fetchpriority="low" width="2800" height="937" />
    <img src="assets/team-mobile.jpg" alt="Zespół lekarzy OrthoCare" class="intro-team-photo__img intro-team-photo__img--mobile" loading="lazy" decoding="async" width="1024" height="682" />
  </section>

  <section class="section home-section">
    <div class="wrap">
      <h2 class="intro-title" style="margin-bottom:40px">Jak to wygląda w&nbsp;praktyce?</h2>
      <div class="cards-carousel" data-cards-carousel>
        <div class="cards-grid cards-grid--swipe cards-grid--steps" id="practiceCards" data-cards-track>
        <div class="card3">
          <div class="card3__img"><img src="assets/step-1.jpg" alt="Krok 1 – konsultacja" loading="lazy" decoding="async" /></div>
          <div class="card3__body">
            <p class="subhead" style="margin-bottom:8px">Krok 1</p>
            <h3 class="card3__title">Rozmowa, która naprawdę coś wnosi</h3>
            <p class="card3__text">Na początku po prostu słuchamy. Zadajemy pytania, analizujemy objawy. Nie patrzymy tylko na fragment – interesuje nas cały obraz.</p>
          </div>
        </div>
        <div class="card3">
          <div class="card3__img"><img src="assets/step-2.jpg" alt="Krok 2 – leczenie" loading="lazy" decoding="async" /></div>
          <div class="card3__body">
            <p class="subhead" style="margin-bottom:8px">Krok 2</p>
            <h3 class="card3__title">Leczenie, które ma sens</h3>
            <p class="card3__text">Gdy wiemy, z czym mamy do czynienia, działamy. Zawsze tłumaczymy, dlaczego proponujemy daną metodę.</p>
          </div>
        </div>
        <div class="card3">
          <div class="card3__img"><img src="assets/step-3.jpg" alt="Krok 3 – opieka" loading="lazy" decoding="async" /></div>
          <div class="card3__body">
            <p class="subhead" style="margin-bottom:8px">Krok 3</p>
            <h3 class="card3__title">Opieka bez ram czasowych</h3>
            <p class="card3__text">Po zabiegu czy konsultacji jesteśmy nadal dostępni i prowadzimy pacjenta tak długo, jak tego potrzebuje.</p>
          </div>
        </div>
        </div>
        <div class="cards-carousel__controls">
          <button type="button" class="slider-btn" data-cards-prev aria-label="Poprzednia karta">&#8592;</button>
          <button type="button" class="slider-btn" data-cards-next aria-label="Następna karta">&#8594;</button>
        </div>
      </div>
    </div>
  </section>
"""

TESTIMONIALS = """
  <section class="reviews-section section section--alt home-section" id="opinie">
    <div class="wrap">
      <h2 class="intro-title" style="margin-bottom:40px">Opinie naszych pacjentów</h2>
      <div class="reviews-track" id="testGrid"></div>
      <div class="reviews-controls">
        <button class="slider-btn" id="tPrev" aria-label="Poprzednia opinia">&#8592;</button>
        <button class="slider-btn" id="tNext" aria-label="Następna opinia">&#8594;</button>
      </div>
      <p class="reviews-note"><a href="https://www.google.com/maps/search/OrthoCare+Radom" target="_blank" rel="noopener">Zobacz wszystkie opinie w Google →</a></p>
    </div>
  </section>
"""

CTA = ""

KONTAKT_BODY = """
  <section class="kontakt-page section">
    <div class="wrap">
      <header class="kontakt-page__header">
        <h1 class="kontakt-page__title">Kontakt</h1>
      </header>
      <div class="kontakt-page__cards">
        <div class="kontakt-panel kontakt-panel--info">
          <div class="kontakt-panel__top">
            <h2 class="kontakt-panel__title">Skontaktuj się z nami</h2>
          </div>
          <div class="kontakt-panel__content">
          <ul class="kontakt-list">
            <li class="kontakt-list__item">
              <span class="kontakt-list__icon" aria-hidden="true">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
              </span>
              <div>
                <p class="kontakt-list__label">Zadzwoń do nas</p>
                <a href="tel:889817012" class="kontakt-list__value">889 817 012</a>
                <p class="kontakt-list__note">pn–pt, 8:00–18:00</p>
              </div>
            </li>
            <li class="kontakt-list__item">
              <span class="kontakt-list__icon" aria-hidden="true">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              </span>
              <div>
                <p class="kontakt-list__label">Napisz do nas</p>
                <a href="mailto:rejestracja@orthocare-radom.pl" class="kontakt-list__value">rejestracja@orthocare-radom.pl</a>
                <p class="kontakt-list__note">Odpowiedź w 24 h</p>
              </div>
            </li>
            <li class="kontakt-list__item">
              <span class="kontakt-list__icon" aria-hidden="true">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
              </span>
              <div>
                <p class="kontakt-list__label">Odwiedź nas</p>
                <p class="kontakt-list__value">ul. Dębowa 2, 26-600 Radom</p>
                <p class="kontakt-list__note">Parking, parter</p>
              </div>
            </li>
          </ul>
          <div class="kontakt-panel__socials">
            <a href="https://www.facebook.com/profile.php?id=61564864085861&sk=about" target="_blank" class="kontakt-social">Facebook</a>
            <a href="https://www.instagram.com/klinika_orthocare/" target="_blank" class="kontakt-social">Instagram</a>
          </div>
          </div>
        </div>
        <div class="kontakt-panel kontakt-panel--visit">
          <div class="kontakt-visit__hero">
            <img src="assets/budynek.jpg" alt="OrthoCare Radom" class="kontakt-visit__photo" loading="lazy" decoding="async">
            <div class="kontakt-visit__overlay">
              <h2 class="kontakt-visit__title">Odwiedź nas</h2>
              <a href="https://maps.google.com/?q=ul.+Dębowa+2,+26-600+Radom" target="_blank" rel="noopener" class="btn btn--white kontakt-visit__btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
                Wyznacz trasę
              </a>
            </div>
          </div>
          <div class="kontakt-visit__map">
            <!-- Mapa Google wczytywana przez js/cookies.js dopiero po akceptacji plików cookies -->
            <div class="map-consent" data-consent-map data-map-src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2458!2d21.15!3d51.405!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sul.+D%C4%99bowa+2+Radom!5e0!3m2!1spl!2spl!4v1" data-map-title="Mapa OrthoCare" data-map-link="https://maps.google.com/?q=ul.+Dębowa+2,+26-600+Radom">
              <div class="map-consent__box">
                <p class="map-consent__text">Aby wyświetlić mapę, zaakceptuj pliki cookies.</p>
                <div class="map-consent__actions">
                  <button type="button" class="btn btn--primary" data-cookie-accept>Akceptuję</button>
                  <a class="btn btn--outline" href="https://maps.google.com/?q=ul.+Dębowa+2,+26-600+Radom" target="_blank" rel="noopener">Otwórz w Google Maps</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

BOOKING_MODAL = """
<div id="booking-modal" class="booking-modal hidden">
  <div class="booking-modal__panel">
    <button id="close-modal" type="button" class="booking-modal__close" aria-label="Zamknij">
      <svg width="32" height="32" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
      </svg>
    </button>
    <div class="booking-modal__body">
      <h2 class="heading booking-modal__title">Umów wizytę w Centrum Ortopedycznym OrthoCare</h2>
      <div class="booking-modal__widget">
        <a class="zl-facility-url" href="https://www.znanylekarz.pl/placowki/klinika-orthocare" rel="nofollow" data-zlw-facility="klinika-orthocare" data-zlw-type="facility-big" data-zlw-saas-only="true" data-zlw-a11y-title="Widget umówienia wizyty lekarskiej">Centrum Ortopedyczne OrthoCare</a>
      </div>
    </div>
  </div>
</div>
"""

# Czcionki serwowane lokalnie (src/assets/fonts) – brak zapytań do Google Fonts
FONTS = """  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter-variable-latin.woff2" crossorigin>
  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/dm-serif-display-400-latin.woff2" crossorigin>
  <link href="css/fonts.css" rel="stylesheet">
"""

FAVICON = '  <link rel="icon" type="image/jpeg" href="favicon.jpg?v=1">\n'

SITE_DESCRIPTION = "Centrum Ortopedyczne OrthoCare – Radom. Nowoczesna ortopedia, diagnostyka i zabiegi."
SITE_NAME = "Centrum Ortopedyczne OrthoCare"


def meta_block(title: str, og_image: str = "") -> str:
    image = f'  <meta property="og:image" content="{og_image}">\n' if og_image else ''
    return (
        f'  <meta name="description" content="{SITE_DESCRIPTION}">\n'
        f'  <meta property="og:title" content="{title}">\n'
        f'  <meta property="og:description" content="{SITE_DESCRIPTION}">\n'
        f'{image}'
        f'  <meta property="og:site_name" content="{SITE_NAME}">\n'
        f'  <meta name="twitter:title" content="{title}">\n'
        f'  <meta name="twitter:description" content="{SITE_DESCRIPTION}">\n'
    )


# Widget ZnanyLekarz (platform.docplanner.com) ładuje js/main.js wyłącznie po akceptacji cookies.
SCRIPTS = """
<script src="js/cookies.js" defer></script>
<script src="js/main.js" defer></script>
"""


def nav_html(active: str, logo_src: str = LOGO) -> str:
    links = []
    for key, label, href in NAV_LINKS:
        cls = ' class="is-active"' if key == active else ''
        links.append(f'        <li><a href="{href}"{cls}>{label}</a></li>')
    mobile_parts = []
    for key, label, href in NAV_LINKS:
        active_cls = ' class="is-active"' if key == active else ''
        mobile_parts.append(f'    <a href="{href}"{active_cls}>{label}</a>')
    mobile = '\n'.join(mobile_parts)
    kontakt_active = ' class="is-active"' if active == 'kontakt' else ''
    return f"""<header id="site-header">
<nav class="nav">
  <div class="nav__wrap">
    <a href="index.html" class="nav__logo">
      <img src="{logo_src}" alt="OrthoCare" width="180" height="38" decoding="async" />
    </a>
    <ul class="nav__links" id="navLinks">
{chr(10).join(links)}
    </ul>
    <div class="nav__actions">
      <div class="nav__social">
        <a href="https://www.instagram.com/klinika_orthocare/" target="_blank" class="nav-social-btn" aria-label="Instagram">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
        </a>
        <a href="https://www.facebook.com/profile.php?id=61564864085861&sk=about" target="_blank" class="nav-social-btn" aria-label="Facebook">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>
        </a>
      </div>
      <a href="kontakt.html" class="nav__btn-kontakt"{kontakt_active}>Kontakt</a>
      <button type="button" class="nav__btn-rezerwuj umow-wizyte-btn">Umów wizytę</button>
    </div>
    <button class="nav__hamburger" id="menuBtn" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="nav__mobile" id="mobileMenu">
{mobile}
    <a href="kontakt.html"{kontakt_active}>Kontakt</a>
    <div class="nav-cta-wrap">
      <button type="button" class="btn btn--primary umow-wizyte-btn" style="width:100%">Umów wizytę</button>
    </div>
  </div>
</nav>
</header>"""


def footer_html() -> str:
    nav_items = ''.join(f'            <li><a href="{href}">{label}</a></li>\n' for _, label, href in NAV_LINKS)
    nav_items += '            <li><a href="kontakt.html">Kontakt</a></li>\n'
    return f"""<footer class="footer-dark">
  <div class="footer-dark__top">
    <div class="wrap">
      <div class="footer-dark__grid">
        <div class="footer-dark__brand">
          <img src="assets/logo-footer.png" alt="OrthoCare" class="footer-dark__logo" loading="lazy" decoding="async" width="240" height="96" />
          <p class="footer-dark__tagline">Ortopedia nowego pokolenia. Łączymy najnowocześniejszą wiedzę medyczną z indywidualnym podejściem.</p>
          <div class="footer-dark__social">
            <a href="https://www.facebook.com/profile.php?id=61564864085861&sk=about" target="_blank" class="footer-social-btn" aria-label="Facebook">fb</a>
            <a href="https://www.instagram.com/klinika_orthocare/" target="_blank" class="footer-social-btn" aria-label="Instagram">ig</a>
          </div>
        </div>
        <div class="footer-dark__col">
          <p class="footer-dark__heading">Nawigacja</p>
          <ul class="footer-dark__list">
{nav_items}          </ul>
        </div>
        <div class="footer-dark__col">
          <p class="footer-dark__heading">Dokumenty</p>
          <ul class="footer-dark__list">
            <li><a href="assets/rodo.pdf" target="_blank">Klauzula RODO</a></li>
            <li><a href="assets/regulamin.pdf" target="_blank">Regulamin</a></li>
            <li><a href="assets/downloads/Polityka cookies serwisu OrthoCare.pdf" target="_blank">Polityka cookies</a></li>
            <li><a href="#" data-cookie-settings>Ustawienia cookies</a></li>
          </ul>
        </div>
        <div class="footer-dark__col">
          <p class="footer-dark__heading">Nasi partnerzy</p>
          <div class="footer-dark__partners">
            <a href="https://warsaweagles.com/" target="_blank" rel="noopener" class="footer-partner-tile"><img src="assets/partner-eagles.png" alt="Warsaw Eagles" class="footer-partner-logo" loading="lazy" decoding="async" width="80" height="80" /></a>
            <a href="https://www.rplusradom.pl/" target="_blank" rel="noopener" class="footer-partner-tile"><img src="assets/partner-rehab-plus.png" alt="Rehabilitacja Plus" class="footer-partner-logo" loading="lazy" decoding="async" width="80" height="80" /></a>
            <a href="https://www.wksczarni.pl/" target="_blank" rel="noopener" class="footer-partner-tile"><img src="assets/partner-czarni-radom.png" alt="WKS Czarni Radom" class="footer-partner-logo" loading="lazy" decoding="async" width="80" height="80" /></a>
            <a href="https://gipsme.pl/" target="_blank" rel="noopener" class="footer-partner-tile footer-partner-tile--gipsme"><img src="assets/gipsme.png" alt="gipsme" class="footer-partner-logo" loading="lazy" decoding="async" width="80" height="80" /></a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-dark__bottom">
    <div class="wrap">
      <span>© 2026 Centrum Ortopedyczne OrthoCare. Wszelkie prawa zastrzeżone.</span>
      <span>ul. Dębowa 2, 26-600 Radom | <a href="tel:889817012">889 817 012</a></span>
    </div>
  </div>
</footer>"""


def page_title_block(title: str) -> str:
    return f"""<div class="page-section__head">
  <div class="wrap-inner">
    <h1 class="page-title">{title}</h1>
  </div>
</div>"""


IMG_TAG_RE = re.compile(r'<img\b[^>]*?>', re.I)
IMG_SRC_RE = re.compile(r'\bsrc="(assets/[^"]+?)\.(jpe?g|png)"', re.I)


def wrap_webp(html: str) -> str:
    """Wrap <img src="assets/x.jpg|png"> in <picture> with a WebP <source> when assets/x.webp exists.

    Images that already sit inside a <picture> (directly after <picture> or <source>) are left untouched,
    so the transformation is idempotent.
    """
    out = []
    pos = 0
    for m in IMG_TAG_RE.finditer(html):
        tag = m.group(0)
        src_m = IMG_SRC_RE.search(tag)
        before = html[pos:m.start()]
        out.append(before)
        pos = m.end()
        if not src_m:
            out.append(tag)
            continue
        webp_rel = f"{src_m.group(1)}.webp"
        if not (SRC / webp_rel).exists():
            out.append(tag)
            continue
        prev = html[max(0, m.start() - 400):m.start()].rstrip()
        if prev.endswith('>') and re.search(r'<(picture|source)\b[^>]*>$', prev, re.I):
            out.append(tag)
            continue
        clean = tag[:-1].rstrip()
        closing = '>'
        if clean.endswith('/'):
            clean = clean[:-1].rstrip()
            closing = ' >'
        out.append(f'<picture><source type="image/webp" srcset="{webp_rel}">{clean}{closing}</picture>')
    out.append(html[pos:])
    return ''.join(out)


def shell(title: str, active: str, main_body: str, extra_css: bool = True, tailwind: bool = True, logo_src: str = LOGO, head_extra: str = "", preload_hero: bool = False, og_image: str = "") -> str:
    legacy = '  <link href="css/legacy.css" rel="stylesheet">\n' if extra_css else ''
    tailwind_link = '  <link href="dist/output.css" rel="stylesheet">\n' if tailwind else ''
    preload = '  <link rel="preload" as="image" href="assets/hero-desktop.webp" type="image/webp" fetchpriority="high" media="(min-width: 769px)">\n  <link rel="preload" as="image" href="assets/hero-2.webp" type="image/webp" fetchpriority="high" media="(max-width: 768px)">\n' if preload_hero else ''
    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
{meta_block(title, og_image)}{FAVICON}{preload}{FONTS}  <link href="css/theme.css" rel="stylesheet">
{legacy}{tailwind_link}{head_extra}</head>
<body>

{nav_html(active, logo_src)}

<main>
{main_body}
</main>

{footer_html()}

{BOOKING_MODAL}

{SCRIPTS}
</body>
</html>
"""
    return wrap_webp(html)


def fix_section_links(content: str) -> str:
    return (
        content.replace('href="#kontakt"', 'href="kontakt.html"')
        .replace('href="#kriolezja"', 'href="kriolezja.html"')
        .replace('href="kontakt.html"', 'href="kontakt.html"')
    )


def main():
    # Homepage — tylko sekcje startowe
    index_html = shell(
        "Centrum Ortopedyczne OrthoCare – Radom",
        "home",
        HOME + TESTIMONIALS + CTA,
        extra_css=False,
        tailwind=False,
        preload_hero=True,
    )
    (SRC / "index.html").write_text(index_html, encoding="utf-8")
    print(f"index.html ({len(index_html)} bytes)")

    # Podstrony z sekcji
    for filename, meta in PAGES.items():
        content = (SECTIONS / meta["section"]).read_text(encoding="utf-8").strip()
        content = fix_section_links(content)
        narrow = ' wrap-inner--narrow' if meta["narrow"] else ''
        body = f"""{page_title_block(meta["page_title"])}
<div class="page-section__body">
  <div class="wrap-inner{narrow} legacy-content">
{content}
  </div>
</div>"""
        html = shell(meta["title"], meta["active"], body)
        (SRC / filename).write_text(html, encoding="utf-8")
        print(f"{filename} ({len(html)} bytes)")

    # Kontakt
    kontakt_html = shell(
        "Kontakt – Centrum Ortopedyczne OrthoCare – Radom",
        "kontakt",
        KONTAKT_BODY,
        extra_css=False,
        tailwind=False,
        og_image="https://orthocare-radom.pl/assets/budynek.jpg",
    )
    (SRC / "kontakt.html").write_text(kontakt_html, encoding="utf-8")
    print(f"kontakt.html ({len(kontakt_html)} bytes)")

    # blog → kriolezja
    blog_title = "Przekierowanie – Centrum Ortopedyczne OrthoCare"
    blog = f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0;url=kriolezja.html">
  <link rel="canonical" href="kriolezja.html">
  <title>{blog_title}</title>
{meta_block(blog_title)}{FAVICON}  <script>location.replace('kriolezja.html');</script>
</head>
<body><p><a href="kriolezja.html">Przejdź do Kriolezja</a></p></body>
</html>
"""
    (SRC / "blog.html").write_text(blog, encoding="utf-8")
    print("blog.html → kriolezja.html")


if __name__ == "__main__":
    main()
