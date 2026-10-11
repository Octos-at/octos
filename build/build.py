#!/usr/bin/env python3
"""Builds the OCTOS website prototype in English (/) and German (/de/).

Run:  python3 build/build.py   (from the site folder, or anywhere)
Every page is written from the bilingual text below, so a copy change is made
once here and both languages are rebuilt.
"""
import json
import os

CUR = ' aria-current="page"'
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOCIAL = [
    ("Instagram", "https://www.instagram.com/octos.at/", "@octos.at",
     '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/></svg>'),
    ("YouTube", "https://www.youtube.com/@OCTOS-LLC", "@OCTOS-LLC",
     '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="4" fill="currentColor"/><path d="M10 9v6l5.2-3z" fill="var(--icon-cut, #0d0d0c)"/></svg>'),
    ("TikTok", "https://www.tiktok.com/@octos_llc", "@octos_llc",
     '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3h3c.3 2.2 1.7 3.6 4 3.9v3.1c-1.5 0-2.9-.4-4-1.2V15a6 6 0 1 1-6-6v3.2A2.8 2.8 0 1 0 14 15z" fill="currentColor"/></svg>'),
    ("Facebook", "https://www.facebook.com/profile.php?id=61594530514316", "OCTOS",
     '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z" fill="currentColor"/></svg>'),
]
SLOTS = [  # (key, EN, DE, example EN, example DE, open?)
    ("small", "Small project", "Kleines Projekt", "e.g. a part redesign or a 3D-printed prototype", "z. B. ein Bauteil-Redesign oder ein 3D-gedruckter Prototyp", True),
    ("medium", "Medium project", "Mittleres Projekt", "e.g. a new product from concept to prototype", "z. B. ein neues Produkt vom Konzept bis zum Prototyp", True),
    ("demanding", "Highly demanding project", "Anspruchsvolles Projekt", "e.g. full development with testing and production", "z. B. Komplettentwicklung mit Prüfung und Produktion", True),
]
PHONE = "+43 670 6500 200"
PHONE_TEL = "+436706500200"
MAIL = "info@octos.at"
SITE_URL = "https://octos.at"
DATE = "9 Oct 2026"


def build(lang):
    de = lang == "de"
    R = "../" if de else ""  # path back to shared assets

    def t(en, de_):
        return de_ if de else en

    # ------------------------------------------------------------------ shared
    def social_icons(labels=False):
        return "".join(
            f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}">{icon}{f"<span><b>{name}</b>{handle}</span>" if labels else ""}</a>'
            for name, url, handle, icon in SOCIAL)

    # search + sharing (Daniel's go 2026-10-10, notes/idea4-seo): titles, absolute hreflang, canonical, share tags, JSON-LD
    TITLES = {
        "index": ("Product Development &amp; Prototyping in Austria · OCTOS", "Produktentwicklung &amp; Prototypenbau in Innsbruck · OCTOS"),
        "services": ("Product Design, Prototypes &amp; Manufacturing · OCTOS", "Produktdesign, Prototypen &amp; Fertigung · OCTOS"),
        "products": ("Products Designed &amp; Built in Austria · OCTOS", "Produkte, entwickelt &amp; gebaut in Tirol · OCTOS"),
        "octostool": ("OctoStool: Barber Stool on a Swivel Arm · OCTOS", "OctoStool: Barbierhocker mit Schwenkarm · OCTOS"),
        "about": ("About OCTOS · Product Development in Innsbruck", "Über OCTOS · Produktentwicklung in Innsbruck"),
        "contact": ("Contact · Start Your Product Project · OCTOS", "Kontakt · Ihr Produktprojekt starten · OCTOS"),
        "offer": ("Get an OctoStool Offer · OCTOS", "OctoStool-Angebot anfordern · OCTOS"),
    }

    def seo(page, title, desc):
        slug = "" if page == "index" else page
        en_url, de_url = f"{SITE_URL}/{slug}", f"{SITE_URL}/de/{slug}"
        url = de_url if de else en_url
        tags = f"""<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OCTOS">
<meta property="og:locale" content="{t("en_GB", "de_AT")}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/img/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">"""
        ld = None
        if page == "index":
            ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "OCTOS", "url": f"{SITE_URL}/",
                  "logo": f"{SITE_URL}/img/logo.svg", "image": f"{SITE_URL}/img/share.jpg", "email": MAIL, "telephone": PHONE,
                  "address": {"@type": "PostalAddress", "addressLocality": "Innsbruck", "addressRegion": "Tirol", "addressCountry": "AT"},
                  "areaServed": ["AT", "DE", "CH"], "slogan": "We Design, We Develop, We Deliver",
                  "sameAs": [u for _n, u, _h, _i in SOCIAL]}
        elif page == "octostool":
            ld = {"@context": "https://schema.org", "@type": "Product", "name": "OctoStool",
                  "brand": {"@type": "Brand", "name": "OCTOS"}, "image": f"{SITE_URL}/img/studio-ergo.webp", "description": desc}
        if ld:
            tags += f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
        return tags

    def head(page, title, desc):
        if page in TITLES:
            title = t(*TITLES[page])
        other = f"../{page}.html" if de else f"de/{page}.html"
        return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{seo(page, title, desc)}
<link rel="icon" href="{R}img/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="{R}css/fonts.css">
<link rel="stylesheet" href="{R}css/site.css">
</head>
<body>
""" + header(page, other)

    def header(page, other):
        items = [
            ("services", t("Services", "Leistungen")),
            ("products", t("Products", "Produkte")),
            ("about", t("About", "Über uns")),
            ("contact", t("Contact", "Kontakt")),
        ]
        cur = "products" if page == "octostool" else page
        links = "\n".join(
            f'      <a href="{p}.html"{CUR if p == cur else ""}>{label}</a>'
            for p, label in items
        )
        lang_sw = (
            f'<a href="{other}" hreflang="en" lang="en">EN</a> / <b>DE</b>' if de
            else f'<b>EN</b> / <a href="{other}" hreflang="de" lang="de">DE</a>'
        )
        return f"""
<header class="top">
  <div class="wrap">
    <a href="index.html" class="logo" aria-label="{t("OCTOS home", "OCTOS Startseite")}"></a>
    <nav class="nav" id="nav" aria-label="{t("Main", "Hauptmenü")}">
{links}
    </nav>
    <span class="lang" aria-label="{t("Language", "Sprache")}">{lang_sw}</span>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <a class="btn btn-wood" href="contact.html">{t("Start your project", "Projekt starten")}</a>
  </div>
</header>
"""

    def footer(page):
        other = f"../{page}.html" if de else f"de/{page}.html"
        return f"""
<footer>
  <div class="wrap">
    <a href="index.html" class="logo" aria-label="{t("OCTOS home", "OCTOS Startseite")}"></a>
    <span class="slogan">OCTOS - We Design, We Develop, We Deliver</span>
    <nav aria-label="Footer">
      <a href="services.html">{t("Services", "Leistungen")}</a><a href="products.html">{t("Products", "Produkte")}</a><a href="about.html">{t("About", "Über uns")}</a><a href="contact.html">{t("Contact", "Kontakt")}</a><a href="impressum.html">Impressum</a><a href="impressum.html#datenschutz">{t("Privacy", "Datenschutz")}</a><a href="impressum.html#agb">{t("Terms (AGB)", "AGB")}</a><a href="{other}">{t("Deutsch", "English")}</a>
    </nav>
    <div class="social">{social_icons()}</div>
    <p class="legal">OCTOS e.U. · Ing. Daniel Varga · Innrain 103, 6020 Innsbruck · FN 676155 x, Landesgericht Innsbruck · UID-Nr. ATU83179524</p>
  </div>
</footer>
<script src="{R}js/site.js"></script>
</body>
</html>
"""

    def cta_band(h_en, h_de, p_en, p_de):
        return f"""
  <section class="cta-band" aria-label="{t("Start a project", "Projekt starten")}">
    <div class="wrap">
      <div>
        <h2>{t(h_en, h_de)}</h2>
        <p>{t(p_en, p_de)}</p>
      </div>
      <div class="ctas">
        <a class="btn btn-wood" href="contact.html">{t("Start your project", "Projekt starten")} <span class="arrow">→</span></a>
        <a class="btn btn-line" href="mailto:{MAIL}">{MAIL}</a>
      </div>
    </div>
  </section>
"""

    def idea_check(compact=False, faq="services.html#faq"):
        # free 30-min idea check offer (Daniel 2026-10-10); button presets the checkbox on the contact form
        body = f"""<div class="ideacheck{' compact' if compact else ''}">
          <div>
            <p class="eyebrow">{t("Free · 30 minutes · Video call", "Kostenlos · 30 Minuten · Videocall")}</p>
            <h3>{t("Free idea check, 30 minutes.", "Kostenloser Ideen-Check, 30 Minuten.")}</h3>
            <p>{t("Tell us your idea in a short video call. We tell you honestly what it takes: which steps, roughly how long, and what budget band to expect. Free and with no obligation. NDA on request.",
                  "Erzählen Sie uns Ihre Idee in einem kurzen Videocall. Wir sagen Ihnen ehrlich, was es braucht: welche Schritte, wie lange ungefähr und mit welchem Budgetrahmen Sie rechnen sollten. Kostenlos und unverbindlich. NDA auf Wunsch.")}</p>
          </div>
          <div class="ic-cta">
            <a class="btn btn-wood" href="{'#inq' if compact else 'contact.html?topic=idea#inq'}"{' data-idea' if compact else ''}>{t("Book a free idea check", "Kostenlosen Ideen-Check buchen")} <span class="arrow">→</span></a>
            <a class="ic-faq" href="{faq}">{t("Questions? Read the FAQ", "Fragen? Zu den FAQ")}</a>
          </div>
        </div>"""
        if compact:
            return body
        return f"""
  <section class="block ic-band" aria-label="{t("Free idea check", "Kostenloser Ideen-Check")}">
    <div class="wrap">{body}
    </div>
  </section>
"""

    FAQ = [('Is the idea check really free?', 'Ist der Ideen-Check wirklich kostenlos?', 'Yes. 30 minutes by video call, free and with no obligation.', 'Ja. 30 Minuten per Videocall, kostenlos und unverbindlich.'), ('What should I prepare for the idea check?', 'Was soll ich für den Ideen-Check vorbereiten?', 'Nothing is required. A sketch, photos, a rough budget or a target date help us give you a better first answer.', 'Nichts davon ist Pflicht. Eine Skizze, Fotos, ein grobes Budget oder ein Wunschtermin helfen uns aber, Ihnen eine bessere erste Antwort zu geben.'), ('I only have an idea, no drawings. Is that enough?', 'Ich habe nur eine Idee, keine Zeichnungen. Reicht das?', 'Yes. A napkin sketch is a fine start. Turning ideas into drawings and 3D models is part of what we do.', 'Ja. Eine Serviettenskizze ist ein guter Anfang. Aus Ideen Zeichnungen und 3D-Modelle zu machen, ist Teil unserer Arbeit.'), ('What does a project cost?', 'Was kostet ein Projekt?', 'Most projects fall into one of three bands: under €5,000, €5,000 to 20,000, or over €20,000. After the idea check you get a written offer with a fixed scope.', 'Die meisten Projekte liegen in einem von drei Rahmen: unter 5.000 €, 5.000 bis 20.000 € oder über 20.000 €. Nach dem Ideen-Check erhalten Sie ein schriftliches Angebot mit festem Umfang.'), ('How long does it take?', 'Wie lange dauert es?', 'A full project from idea to product typically takes 3 to 6 months. Single services often take 1 to 3 weeks.', 'Ein komplettes Projekt von der Idee zum Produkt dauert meist 3 bis 6 Monate. Einzelleistungen oft 1 bis 3 Wochen.'), ('Can I book only one step, like renderings or prototypes?', 'Kann ich auch nur einen Schritt buchen, etwa Renderings oder Prototypen?', 'Yes, you can join at any stage, for example with an existing design that needs prototypes and production. There is no minimum project size. Calculations or simulations on their own we arrange through partner engineering offices.', 'Ja, Sie können in jeder Phase einsteigen, etwa mit einem fertigen Design, das Prototypen und Fertigung braucht. Es gibt keine Mindestprojektgröße. Reine Berechnungen oder Simulationen vermitteln wir an Partner-Ingenieurbüros.'), ('Do you sign an NDA?', 'Unterschreiben Sie eine Geheimhaltungsvereinbarung (NDA)?', 'Yes. On request we send our standard NDA before the first call.', 'Ja. Auf Wunsch senden wir Ihnen vor dem ersten Gespräch unsere Standard-NDA.'), ('Who owns the result?', 'Wem gehört das Ergebnis?', 'We agree this per project and put it in writing in the offer, before any work starts.', 'Das vereinbaren wir pro Projekt und halten es im Angebot schriftlich fest, bevor die Arbeit beginnt.'), ('How do you charge?', 'Wie rechnen Sie ab?', 'A fixed price per phase, agreed before each phase starts. No open-ended hourly billing.', 'Zum Fixpreis pro Phase, vereinbart vor Beginn jeder Phase. Keine offene Stundenabrechnung.'), ('Can you also manufacture the product?', 'Können Sie das Produkt auch fertigen?', 'We build prototypes and small runs in our own workshop and work with manufacturing partners for larger quantities.', 'Prototypen und Kleinserien bauen wir in der eigenen Werkstatt, für größere Stückzahlen arbeiten wir mit Fertigungspartnern.'), ('Can you help with testing and certification, like CE?', 'Helfen Sie bei Prüfung und Zertifizierung, etwa CE?', 'Our team brings more than 20 years of experience in the regulated medical device industry. We test in-house or coordinate tests to the relevant standards with accredited test facilities, and prepare the technical documentation.', 'Unser Team bringt über 20 Jahre Erfahrung aus der regulierten Medizintechnik mit. Wir prüfen im Haus oder koordinieren Prüfungen nach den relevanten Normen mit akkreditierten Prüfstellen und erstellen die technische Dokumentation.'), ('Do you work with clients outside Austria?', 'Arbeiten Sie auch mit Kunden außerhalb Österreichs?', 'Yes. We work remotely, in German or English.', 'Ja. Wir arbeiten remote, auf Deutsch oder Englisch.'), ("What if my idea isn't feasible?", 'Was, wenn meine Idee nicht umsetzbar ist?', "We tell you honestly in the idea check, and if we can, we suggest a different route. You don't pay for finding that out.", 'Das sagen wir Ihnen ehrlich im Ideen-Check und schlagen, wenn möglich, einen anderen Weg vor. Dafür zahlen Sie nichts.'), ('Do you help with patents?', 'Helfen Sie bei Patenten?', "We don't file patents ourselves, but we work alongside your patent attorney and prepare the drawings for the application.", 'Patente melden wir nicht selbst an, aber wir arbeiten mit Ihrem Patentanwalt zusammen und erstellen die Zeichnungen für die Anmeldung.'), ('Do you also do packaging and branding?', 'Machen Sie auch Verpackung und Branding?', 'Yes, for the products we develop with you: packaging design, product photos, video and branding.', 'Ja, für die Produkte, die wir mit Ihnen entwickeln: Verpackungsdesign, Produktfotos, Video und Branding.'), ('What happens after the idea check?', 'Wie geht es nach dem Ideen-Check weiter?', 'Within 3 working days you get a short written summary and, if you want to go ahead, an offer with scope, timeline and price.', 'Innerhalb von 3 Werktagen erhalten Sie eine kurze schriftliche Zusammenfassung und, wenn Sie weitermachen möchten, ein Angebot mit Umfang, Zeitplan und Preis.')]

    def faq_block():
        items = "".join(f'<details><summary>{t(qe, qd)}</summary><p>{t(ae, ad)}</p></details>' for qe, qd, ae, ad in FAQ)
        return f"""
  <section class="block faq" id="faq" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">FAQ</p>
        <h2 id="faq-title">{t("Questions before you start.", "Fragen vor dem Start.")}</h2>
      </div>
      <div class="faq-list">{items}</div>
    </div>
  </section>
"""

    def contact_block(heading_tag="h2", extra=""):
        return f"""
  <section class="contact" id="contact" aria-labelledby="ct-title">
    <div class="wrap">
      <div>
        <p class="eyebrow" style="color:var(--night-mute)">{t("Start your project", "Projekt starten")}</p>
        <{heading_tag} id="ct-title" style="margin-top:18px;font-size:clamp(2.2rem, 5vw, 3.8rem)">{t("Bring the idea. <em>We bring the plan.</em>", "Sie bringen die Idee. <em>Wir den Plan.</em>")}</{heading_tag}>
        <p class="lead">{t("Tell us what you want to build. We reply with first thoughts and the next steps.", "Erzählen Sie uns, was Sie bauen möchten. Wir antworten mit ersten Gedanken und den nächsten Schritten.")}</p>
        <div class="tb" aria-label="{t("Contact details", "Kontaktdaten")}">
          <div><small>E-Mail</small><span>{MAIL}</span><button class="copy" type="button" data-copy="{MAIL}">{t("Copy", "Kopieren")}</button></div>
          <div><small>{t("Phone", "Telefon")}</small><span><a href="tel:{PHONE_TEL}" style="text-decoration:none">{PHONE}</a></span><button class="copy" type="button" data-copy="{PHONE}">{t("Copy", "Kopieren")}</button></div>
          <div class="wide"><small>{t("Meetings", "Termine")}</small>{t("Online by video call, wherever you are", "Online per Videocall, egal wo Sie sind")}</div>
          <div><small>{t("Reply time", "Antwortzeit")}</small><span>{t("Within 24 hours", "Innerhalb von 24 Stunden")}</span></div>
          <div><small>{t("Languages", "Sprachen")}</small>English · Deutsch</div>
        </div>
{extra}
      </div>
      <form class="inq" id="inq" novalidate>
        <div class="f wide"><label for="q-idea">{t("Your idea", "Ihre Idee")}</label><textarea id="q-idea" placeholder="{t("What should the product do, and who is it for?", "Was soll das Produkt können, und für wen ist es?")}"></textarea></div>
        <div class="f"><label for="q-slot">{t("Project size", "Projektgröße")}</label>
          <select id="q-slot"><option value="">{t("Not sure yet", "Noch offen")}</option>{"".join(f'<option value="{k}">{t(en, de)}{"" if o else t(" (booked)", " (belegt)")}</option>' for k, en, de, _a, _b, o in SLOTS)}</select></div>
        <div class="f"><label for="q-stage">{t("Project stage", "Projektstand")}</label>
          <select id="q-stage"><option>{t("Just an idea", "Erst eine Idee")}</option><option>{t("Sketches or drawings", "Skizzen oder Zeichnungen")}</option><option>{t("Prototype exists", "Prototyp vorhanden")}</option><option>{t("Ready for production", "Bereit für die Produktion")}</option></select></div>
        <div class="f"><label for="q-budget">{t("Budget range", "Budgetrahmen")}</label>
          <select id="q-budget"><option>{t("Not sure yet", "Noch offen")}</option><option>{t("Under €5,000", "Unter 5.000 €")}</option><option>{t("€5,000 – 20,000", "5.000 – 20.000 €")}</option><option>{t("Over €20,000", "Über 20.000 €")}</option></select></div>
        <div class="f"><label for="q-time">{t("Timeline", "Zeitrahmen")}</label>
          <select id="q-time"><option>{t("Flexible", "Flexibel")}</option><option>{t("Within 3 months", "Innerhalb von 3 Monaten")}</option><option>{t("3 – 6 months", "3 – 6 Monate")}</option><option>{t("Over 6 months", "Über 6 Monate")}</option></select></div>
        <label class="chk wide" for="q-idea-check"><input type="checkbox" id="q-idea-check"><span><b>{t("Book a free idea check", "Kostenlosen Ideen-Check buchen")}</b><small>{t("30 minutes by video call, free and with no obligation", "30 Minuten per Videocall, kostenlos und unverbindlich")}</small></span></label>
        <div class="f"><label for="q-co">{t("Company (optional)", "Firma (optional)")}</label><input id="q-co" type="text" autocomplete="organization"></div>
        <div class="f"><label for="q-name">Name</label><input id="q-name" type="text" autocomplete="name"></div>
        <div class="f"><label for="q-mail">E-Mail</label><input id="q-mail" type="email" autocomplete="email"></div>
        <button class="btn btn-wood" type="submit">{t("Send project inquiry", "Projektanfrage senden")} <span class="arrow">→</span></button>
        <p class="note" id="q-note">{t(f'Pressing the button opens your email app with everything filled in, so you only need to press send. No email app? Write to <a href="mailto:{MAIL}">{MAIL}</a>.', f'Der Button öffnet Ihr E-Mail-Programm mit allen Angaben, Sie müssen nur noch senden. Kein E-Mail-Programm? Schreiben Sie an <a href="mailto:{MAIL}">{MAIL}</a>.')}</p>
      </form>
    </div>
  </section>
"""

    ruler = f"""
      <ol class="ruler">
        <li><span>{t("Idea and briefing", "Idee und Briefing")}</span></li>
        <li><span>{t("Plan and concept", "Plan und Konzept")}</span></li>
        <li><span>{t("Industrial design and 3D models", "Industriedesign und 3D-Modelle")}</span></li>
        <li><span>{t("Prototypes and testing", "Prototypen und Tests")}</span></li>
        <li><span>{t("Construction for production and documentation", "Konstruktion für die Fertigung und Dokumentation")}</span></li>
        <li><span>{t("Production and supply chain", "Produktion und Lieferkette")}</span></li>
        <li><span>{t("Packaging", "Verpackung")}</span></li>
        <li><span>{t("Market-ready product delivered", "Marktreifes Produkt geliefert")}</span></li>
      </ol>
      <div class="ruler-foot"><span>{t("You bring: idea + budget", "Sie bringen: Idee + Budget")}</span><span>{t("Typical project length: 3 to 6 months", "Typische Projektdauer: 3 bis 6 Monate")}</span><span>{t("You receive: a product ready to sell", "Sie erhalten: ein verkaufsfertiges Produkt")}</span></div>"""

    # project capacity: flip the last value to True/False when a slot opens or is booked
    slot_rows = "".join(
        f'<li class="{"open" if is_open else "booked"}"><span class="nm"><b>{t(en, de)}</b><small>{t(ex_en, ex_de)}</small></span>'
        f'<span class="st">{t("Open", "Frei") if is_open else t("Booked", "Belegt")}</span></li>'
        for key, en, de, ex_en, ex_de, is_open in SLOTS)
    open_n = sum(1 for x in SLOTS if x[5])
    first_open = next((x[0] for x in SLOTS if x[5]), "")
    page_id = "card"

    octo_card = f"""
        <a class="card" href="octostool.html">
          <div class="im"><img src="{R}img/studio-ergo.webp" alt="{t("OctoStool with Ergo+ seat mounted to a barber chair", "OctoStool mit Ergo+-Sitz, montiert am Barbierstuhl")}" loading="lazy"></div>
          <div class="txt"><p class="eyebrow">{t("Own product · Barbershops", "Eigenes Produkt · Barbershops")}</p><h3>OctoStool</h3><p>{t("Seated, supported work around the barber chair.", "Sitzend und gestützt rund um den Barbierstuhl arbeiten.")}</p><p class="more">{t("View the OctoStool", "Zum OctoStool")} →</p></div>
        </a>
        <article class="card slots" aria-labelledby="slots-{page_id}">
          <div class="im"><ul class="slot-list">{slot_rows}</ul></div>
          <div class="txt"><p class="eyebrow">{t("Project slots", "Projektplätze")}</p><h3 id="slots-{page_id}">{t(f"{open_n} of {len(SLOTS)} slots open", f"{open_n} von {len(SLOTS)} Plätzen frei")}</h3><p>{t("We take on a limited number of client projects at a time, so each one gets our full attention. Bring the idea, we take it from here.", "Wir nehmen nur wenige Kundenprojekte gleichzeitig an, damit jedes unsere volle Aufmerksamkeit bekommt. Bringen Sie die Idee, den Rest übernehmen wir.")}</p><p class="more"><a href="contact.html?slot={first_open}">{t("Reserve a slot", "Platz reservieren")} →</a></p></div>
        </article>
        <a class="card open start" href="contact.html">
          <div class="im"><svg class="dev" viewBox="0 0 64 64" width="72" height="72" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><polygon points="51.6,28.0 57.8,28.6 57.8,35.4 51.6,36.0 48.7,43.1 52.6,47.8 47.8,52.6 43.1,48.7 36.0,51.6 35.4,57.8 28.6,57.8 28.0,51.6 20.9,48.7 16.2,52.6 11.4,47.8 15.3,43.1 12.4,36.0 6.2,35.4 6.2,28.6 12.4,28.0 15.3,20.9 11.4,16.2 16.2,11.4 20.9,15.3 28.0,12.4 28.6,6.2 35.4,6.2 36.0,12.4 43.1,15.3 47.8,11.4 52.6,16.2 48.7,20.9"/><circle cx="32" cy="32" r="8"/><path d="M32 4v-4M32 64v-4" stroke-width="0"/></svg></div>
          <div class="txt"><p class="eyebrow">{t("Your product", "Ihr Produkt")}</p><h3>{t("Start your project", "Projekt starten")}</h3><p>{t("Tell us about your idea. We reply within 24 hours with first thoughts and the next steps.", "Erzählen Sie uns von Ihrer Idee. Wir antworten innerhalb von 24 Stunden mit ersten Gedanken und den nächsten Schritten.")}</p><p class="more">{t("Start your project", "Projekt starten")} →</p></div>
        </a>"""

    pages = {}

    # ------------------------------------------------------------------ HOME
    pages["index"] = head("index", t("OCTOS · We Design, We Develop, We Deliver", "OCTOS · We Design, We Develop, We Deliver"),
                          t("OCTOS in Innsbruck takes your product from idea to market: design, 3D models, prototypes, metal manufacturing and packaging.",
                            "OCTOS in Innsbruck bringt Ihr Produkt von der Idee bis zur Marktreife: Design, 3D-Modelle, Prototypen, Metallfertigung und Verpackung.")) + f"""
<main id="top">
  <section class="hero" aria-labelledby="hero-title">
    <div class="wrap">
      <div>
        <p class="eyebrow">{t("Industrial design &amp; metal manufacturing · Innsbruck, Austria", "Industriedesign &amp; Metalltechnik · Innsbruck, Österreich")}</p>
        <h1 id="hero-title"><span>We Design,</span><span>We Develop,</span><span>We Deliver</span></h1>
        <p class="offer">{t("From idea to market-ready product.", "Von der Idee zum marktreifen Produkt.")}</p>
        <p>{t("You bring the idea and the budget. We come back with a plan and finish with a product that is designed, prototyped, documented, produced and packaged, ready to sell.",
              "Sie bringen die Idee und das Budget. Wir kommen mit einem Plan zurück und liefern ein Produkt, das gestaltet, als Prototyp getestet, dokumentiert, produziert und verpackt ist, bereit für den Verkauf.")}</p>
        <div class="ctas">
          <a class="btn btn-wood" href="contact.html">{t("Start your project", "Projekt starten")} <span class="arrow">→</span></a>
          <a class="btn btn-line" href="services.html#process">{t("See how a project runs", "So läuft ein Projekt ab")}</a>
        </div>
        <p class="tagline">Efficiency Engineered, Comfort Assured</p>
      </div>
      <div class="stage-wrap"><div class="stage">
        <video src="{R}img/hero.mp4" poster="{R}img/hero-poster.jpg" autoplay muted loop playsinline aria-label="{t("Rotating 3D render of the OctoStool mounted to a barber chair", "Rotierendes 3D-Rendering des OctoStool am Barbierstuhl")}"></video>
      </div>
      <p class="stage-cap"><b>{t("3D render", "3D-Rendering")}</b> · {t("Designed, engineered and built by OCTOS", "Von OCTOS gestaltet, konstruiert und gebaut")}</p>
      </div>
    </div>
  </section>

  <section class="block" id="services" aria-labelledby="svc-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Services", "Leistungen")}</p>
        <h2 id="svc-title">{t("One partner for the whole chain.", "Ein Partner für die ganze Kette.")}</h2>
        <p class="lead">{t("Nine services that run as one project from first sketch to delivered product. Book the full chain, or only the part your team is missing.",
                           "Neun Leistungen, die als ein Projekt laufen, von der ersten Skizze bis zum gelieferten Produkt. Buchen Sie die ganze Kette oder nur den Teil, der Ihrem Team fehlt.")}</p>
      </div>
      <div class="ddd">
        <article class="pillar">
          <div class="pic contain"><img src="{R}img/drawing.webp" alt="{t("Technical line drawing of the OctoStool", "Technische Strichzeichnung des OctoStool")}" loading="lazy"></div>
          <div class="verb"><h3>Design</h3><span>{t("idea → plan", "Idee → Plan")}</span></div>
          <ul class="svc">
            <li><strong>{t("Concept &amp; product design", "Konzept &amp; Produktdesign")}</strong><small>{t("Your idea, turned into a clear concept, a project plan and a design that can be built.", "Ihre Idee wird zu einem klaren Konzept, einem Projektplan und einem Design, das sich bauen lässt.")}</small></li>
            <li><strong>{t("Industrial design", "Industriedesign")}</strong><small>{t("Form, ergonomics, materials and finish, shaped around the people who use the product every day.", "Form, Ergonomie, Material und Oberfläche, ausgerichtet auf die Menschen, die das Produkt täglich nutzen.")}</small></li>
            <li><strong>{t("3D modelling &amp; rendering", "3D-Modellierung &amp; Rendering")}</strong><small>{t("Detailed models and photoreal renderings to settle details, pitch to investors or start marketing early.", "Detaillierte Modelle und fotorealistische Renderings, um Details zu klären, Investoren zu überzeugen oder früh mit dem Marketing zu starten.")}</small></li>
          </ul>
        </article>
        <article class="pillar">
          <div class="pic contain vid"><video src="{R}img/fea.mp4" poster="{R}img/fea-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-label="{t("FEA animation of the OctoStool frame and swivel arm deforming under load", "FEM-Animation: Rahmen und Schwenkarm des OctoStool verformen sich unter Last")}"></video></div>
          <div class="verb"><h3>Develop</h3><span>{t("plan → prototype", "Plan → Prototyp")}</span></div>
          <ul class="svc">
            <li><strong>{t("Load check in development", "Belastungscheck in der Entwicklung")}</strong><small>{t("During development we run FEA on critical parts to see how they bend and where stress builds up, before we build the prototype.", "In der Entwicklung prüfen wir kritische Teile per FEM-Simulation, wie sie sich verformen und wo Spannungen entstehen, bevor wir den Prototyp bauen.")}</small></li>
            <li><strong>{t("Prototypes &amp; testing", "Prototypen &amp; Tests")}</strong><small>{t("Printed and working prototypes, tested in our workshop or, where a standard requires it, by accredited test labs.", "Gedruckte und funktionsfähige Prototypen, in der eigenen Werkstatt getestet oder, wo eine Norm es verlangt, von akkreditierten Prüfstellen.")}</small></li>
            <li><strong>{t("Construction &amp; documentation", "Konstruktion &amp; Dokumentation")}</strong><small>{t("Parts constructed for our workshop or manufacturing partners. Your product comes with drawings, CAD data, manuals and the technical file.", "Teile konstruiert für unsere Werkstatt oder Fertigungspartner. Zum Produkt gehören Zeichnungen, CAD-Daten, Anleitungen und die technische Dokumentation.")}</small></li>
          </ul>
        </article>
        <article class="pillar">
          <div class="pic contain"><img src="{R}img/studio-classic.webp" alt="{t("OctoStool Classic unit on its base plate", "OctoStool Classic auf seiner Bodenplatte")}" loading="lazy"></div>
          <div class="verb"><h3>Deliver</h3><span>{t("prototype → market", "Prototyp → Markt")}</span></div>
          <ul class="svc">
            <li><strong>{t("Manufacturing &amp; supply chain", "Fertigung &amp; Lieferkette")}</strong><small>{t("Our own metalwork plus a supplier network, run for you through one contact.", "Eigene Metallbearbeitung und ein Lieferantennetzwerk, für Sie gesteuert über einen Ansprechpartner.")}</small></li>
            <li><strong>{t("Packaging development", "Verpackungsentwicklung")}</strong><small>{t("Packaging that protects the product, ships well and presents your brand.", "Verpackung, die das Produkt schützt, sich gut versenden lässt und Ihre Marke präsentiert.")}</small></li>
            <li><strong>{t("Worldwide delivery", "Weltweite Lieferung")}</strong><small>{t("Made in Innsbruck, shipped to you and your customers, as single orders or on schedule.", "Gefertigt in Innsbruck, geliefert an Sie und Ihre Kunden, als Einzelauftrag oder nach Plan.")}</small></li>
          </ul>
        </article>
      </div>
      <p style="margin-top:32px"><a class="btn btn-ink" href="services.html">{t("All services in detail", "Alle Leistungen im Detail")} <span class="arrow">→</span></a></p>
    </div>
  </section>

  <section class="block process" id="process" aria-labelledby="proc-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("How a project runs", "So läuft ein Projekt ab")}</p>
        <h2 id="proc-title">{t("Eight steps from idea to delivery.", "Acht Schritte von der Idee bis zur Lieferung.")}</h2>
        <p class="lead">{t("You see a plan and a budget before anything is built, and you get a result at the end of every step.", "Sie sehen Plan und Budget, bevor etwas gebaut wird, und erhalten nach jedem Schritt ein Ergebnis.")}</p>
      </div>{ruler}
    </div>
  </section>

  <section class="block" id="products" aria-labelledby="case-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Featured case · Our own product", "Referenz · Unser eigenes Produkt")}</p>
        <h2 id="case-title">{t("The OctoStool, from sketch to barbershop.", "Der OctoStool, von der Skizze in den Barbershop.")}</h2>
        <p class="lead">{t("We took our own idea through every step we offer clients. It is now in daily use in barbershops.", "Wir haben unsere eigene Idee durch jeden Schritt geführt, den wir Kunden anbieten. Heute ist er täglich in Barbershops im Einsatz.")}</p>
      </div>
      <div class="case-grid">
        <div>
          <figure class="case-hero" style="margin:0">
            <img src="{R}img/barber-at-work.webp" alt="{t("Barber seated on the OctoStool, cutting a client's hair", "Barbier sitzt auf dem OctoStool und schneidet einem Kunden die Haare")}" loading="lazy">
            <figcaption>{t("Delivered · in use in a barbershop", "Geliefert · im Einsatz im Barbershop")}</figcaption>
          </figure>
          <div class="chain">
            <figure><div class="im contain"><img src="{R}img/drawing.webp" alt="{t("OctoStool line drawing", "Strichzeichnung des OctoStool")}" loading="lazy"></div><figcaption>01 · {t("Design drawing", "Entwurfszeichnung")}</figcaption></figure>
            <figure><div class="im"><img src="{R}img/render.webp" alt="{t("3D render of the OctoStool with barber chair", "3D-Rendering des OctoStool mit Barbierstuhl")}" loading="lazy"></div><figcaption>02 · {t("3D render", "3D-Rendering")}</figcaption></figure>
            <figure><div class="im"><img src="{R}img/footrest.webp" alt="{t("Wooden footrest ring and steel base plate", "Fußring aus Holz und Bodenplatte aus Stahl")}" loading="lazy"></div><figcaption>03 · {t("Built in steel and wood", "Gebaut aus Stahl und Holz")}</figcaption></figure>
          </div>
        </div>
        <div class="case-copy">
          <p class="quote">{t('"Move like you\'re standing. Feel like you\'re not."', "„Bewegen wie im Stehen. Sitzen wie im Sessel.“")}</p>
          <p>{t("A barber's stool on a swivel arm, mounted to the base of the barber chair. The barber stays seated and supported while moving around the client.", "Ein Barbierhocker auf einem Schwenkarm, montiert am Fuß des Barbierstuhls. Der Barbier bleibt sitzend gestützt und bewegt sich trotzdem frei um den Kunden.")}</p>
          <div class="benefits">
            <div><b>Health<i>+</i></b><small>{t("Less strain on back, legs and shoulders", "Weniger Belastung für Rücken, Beine und Schultern")}</small></div>
            <div><b>Efficiency<i>+</i></b><small>{t("Move around the client with ease", "Mühelos rund um den Kunden")}</small></div>
            <div><b>Comfort<i>+</i></b><small>{t("Full reach while seated", "Volle Reichweite im Sitzen")}</small></div>
          </div>
          <dl class="specs">
            <dt>{t("Frame", "Rahmen")}</dt><dd>{t("Powder-coated steel, black or a custom colour", "Pulverbeschichteter Stahl, schwarz oder in Wunschfarbe")}</dd>
            <dt>{t("Max. load", "Max. Belastung")}</dt><dd>Essential {t("up to", "bis")} 110 kg · Power+ {t("up to", "bis")} 150 kg</dd>
            <dt>{t("Reach", "Reichweite")}</dt><dd>{t("50–70 cm horizontal", "50–70 cm horizontal")}</dd>
            <dt>{t("Swivel", "Schwenkbereich")}</dt><dd>{t("210°, magnetic park position", "210°, magnetische Parkposition")}</dd>
            <dt>{t("Seats", "Sitze")}</dt><dd>Ergo+, Ergo, Classic+, Classic</dd>
          </dl>
          <div class="row">
            <a class="btn btn-ink" href="octostool.html">{t("View the OctoStool", "Zum OctoStool")} <span class="arrow">→</span></a>
            <a class="btn btn-line" href="offer.html">{t("Get an offer", "Angebot anfordern")}</a>
          </div>
        </div>
      </div>

      <div class="shelf" aria-label="{t("Products and projects", "Produkte und Projekte")}">{octo_card}
      </div>
    </div>
  </section>
{idea_check()}
  <section class="block who" id="about" aria-labelledby="who-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Who we work with", "Für wen wir arbeiten")}</p>
        <h2 id="who-title">{t("For people with an idea, and teams without the capacity.", "Für Menschen mit einer Idee und Teams ohne Kapazität.")}</h2>
        <p class="lead">{t("Founded in Innsbruck by mechanical engineer Ing. Daniel Varga, backed by a team with a PhD in materials science, over 20 years combined in the medical device industry and our own mechanical and wood workshop.", "Gegründet in Innsbruck von Maschinenbauingenieur Ing. Daniel Varga, mit einem Team, das eine Promotion in Materialwissenschaft, über 20 Jahre gemeinsame Erfahrung in der Medizintechnik und eine eigene Metall- und Holzwerkstatt mitbringt.")}</p>
      </div>
      <div class="who-grid">
        <article>
          <h3>{t("Entrepreneurs &amp; founders", "Unternehmer:innen &amp; Gründer:innen")}</h3>
          <p>{t("You have an idea and a budget, but no product team. We become that team, from the first plan to the first shipment.", "Sie haben eine Idee und ein Budget, aber kein Produktteam. Wir werden dieses Team, vom ersten Plan bis zur ersten Lieferung.")}</p>
          <ul><li>{t("A clear plan and budget before building starts", "Klarer Plan und klares Budget, bevor gebaut wird")}</li><li>{t("Renderings to pitch to investors and customers", "Renderings für Investoren und Kunden")}</li><li>{t("One contact for the whole chain", "Ein Ansprechpartner für die ganze Kette")}</li></ul>
        </article>
        <article>
          <h3>{t("Established companies", "Etablierte Unternehmen")}</h3>
          <p>{t("Your team is at capacity or lacks a specific skill. We take on a full product, or join at the stage you are at, from design to prototypes and production.", "Ihr Team ist ausgelastet oder es fehlt eine bestimmte Kompetenz. Wir übernehmen ein ganzes Produkt oder steigen in Ihrer Phase ein, vom Design über Prototypen bis zur Fertigung.")}</p>
          <ul><li>{t("Design and development of products we build for you", "Design und Entwicklung von Produkten, die wir für Sie bauen")}</li><li>{t("Prototyping before you commit to tooling", "Prototypen, bevor Sie in Werkzeuge investieren")}</li><li>{t("Production and supply chain set up for you", "Produktion und Lieferkette für Sie aufgebaut")}</li></ul>
        </article>
      </div>
      <p style="margin-top:32px"><a class="btn btn-line on-light" href="about.html">{t("About OCTOS", "Über OCTOS")} <span class="arrow">→</span></a></p>
    </div>
  </section>
{contact_block()}
</main>
""" + footer("index")

    # ------------------------------------------------------------------ SERVICES
    def svc(n, en_name, de_name, en_hl, de_hl, en_desc, de_desc, en_for, de_for):
        return f"""
            <li data-n="{n:02d}"><h3>{t(en_name, de_name)}</h3><p class="hl">{t(en_hl, de_hl)}</p><p>{t(en_desc, de_desc)}</p><p class="for"><b>{t("For", "Für")}:</b> {t(en_for, de_for)}</p></li>"""

    pages["services"] = head("services", t("Services · OCTOS", "Leistungen · OCTOS"),
                             t("Concept and product design, 3D models and renderings, prototypes, metal manufacturing, packaging and delivery from one partner in Innsbruck.",
                               "Konzept und Produktdesign, 3D-Modelle und Renderings, Prototypen, Metallfertigung, Verpackung und Lieferung aus einer Hand in Innsbruck.")) + f"""
<main id="top">
  <section class="phead" aria-labelledby="pg-title">
    <div class="wrap">
      <div>
        <p class="eyebrow">{t("Services", "Leistungen")}</p>
        <h1 id="pg-title">{t("From idea to <em>market-ready product.</em>", "Von der Idee zum <em>marktreifen Produkt.</em>")}</h1>
        <p class="lead">{t("You bring the idea and the budget. We come back with a plan and finish with a product that is designed, prototyped, documented, produced and packaged, ready to sell. Book the full chain, or only the step your team is missing.",
                           "Sie bringen die Idee und das Budget. Wir kommen mit einem Plan zurück und liefern ein Produkt, das gestaltet, als Prototyp getestet, dokumentiert, produziert und verpackt ist, bereit für den Verkauf. Buchen Sie die ganze Kette oder nur den Schritt, der Ihrem Team fehlt.")}</p>
        <div class="ctas">
          <a class="btn btn-wood" href="contact.html">{t("Start your project", "Projekt starten")} <span class="arrow">→</span></a>
          <a class="btn btn-line" href="#process">{t("How a project runs", "So läuft ein Projekt ab")}</a>
        </div>
      </div>
      <figure><img src="{R}img/render.webp" alt="{t("Photoreal 3D render of the OctoStool mounted to a barber chair", "Fotorealistisches 3D-Rendering des OctoStool am Barbierstuhl")}"><figcaption>{t("3D render by OCTOS", "3D-Rendering von OCTOS")}</figcaption></figure>
    </div>
  </section>

  <section class="block" aria-label="{t("Services in detail", "Leistungen im Detail")}">
    <div class="wrap">
      <div class="svc-group" id="design">
        <div class="side">
          <p class="verb">Design<span>{t("idea → plan", "Idee → Plan")}</span></p>
          <div class="pic contain"><img src="{R}img/drawing.webp" alt="{t("Technical line drawing of the OctoStool", "Technische Strichzeichnung des OctoStool")}" loading="lazy"></div>
        </div>
        <ul class="svc-list">{svc(1, "Concept &amp; product design", "Konzept &amp; Produktdesign",
            "Your idea, turned into a product plan.", "Ihre Idee als Produktplan.",
            "We take your idea and turn it into a clear concept, a project plan and a design that can be built. Function, cost and production are part of the design from day one.",
            "Wir machen aus Ihrer Idee ein klares Konzept, einen Projektplan und ein Design, das sich bauen lässt. Funktion, Kosten und Fertigung sind vom ersten Tag an Teil des Entwurfs.",
            "founders with an idea; companies planning a new product", "Gründer:innen mit einer Idee; Unternehmen, die ein neues Produkt planen")}{svc(2, "Industrial design", "Industriedesign",
            "Shaped around the people who use it.", "Gestaltet für die Menschen, die es nutzen.",
            "Form, ergonomics, materials and finish, worked out for daily use. We design for the hands, backs and routines of real users, then for the shelf.",
            "Form, Ergonomie, Material und Oberfläche, ausgelegt auf den täglichen Gebrauch. Wir gestalten für die Hände, Rücken und Abläufe echter Nutzer, dann für das Regal.",
            "products that people touch, carry or work with every day", "Produkte, die Menschen täglich berühren, tragen oder mit denen sie arbeiten")}{svc(3, "3D modelling &amp; rendering", "3D-Modellierung &amp; Rendering",
            "See your product before it exists.", "Sehen Sie Ihr Produkt, bevor es existiert.",
            "We build detailed 3D models and photorealistic renderings and animations. Use them to settle details, pitch to investors or start marketing before the first part is made.",
            "Wir erstellen detaillierte 3D-Modelle, fotorealistische Renderings und Animationen. Damit klären Sie Details, überzeugen Investoren oder starten das Marketing, bevor das erste Teil gefertigt ist.",
            "founders raising money; marketing and sales teams", "Gründer:innen auf Investorensuche; Marketing- und Vertriebsteams")}
        </ul>
      </div>

      <div class="svc-group" id="develop">
        <div class="side">
          <p class="verb">Develop<span>{t("plan → prototype", "Plan → Prototyp")}</span></p>
          <div class="pic contain vid"><video src="{R}img/fea.mp4" poster="{R}img/fea-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-label="{t("FEA animation of the OctoStool frame and swivel arm deforming under load", "FEM-Animation: Rahmen und Schwenkarm des OctoStool verformen sich unter Last")}"></video></div>
        </div>
        <ul class="svc-list">{svc(4, "Load check in development", "Belastungscheck in der Entwicklung",
            "Know it holds before we build it.", "Wissen, dass es hält, bevor wir es bauen.",
            "During development we run FEA on critical parts of your product to see how they bend and where stress builds up. It helps us choose material and wall thickness before we build the prototype, so parts are safe without being heavier or more expensive than they need to be.",
            "In der Entwicklung prüfen wir kritische Teile Ihres Produkts per FEM-Simulation: Wie verformen sie sich, wo entstehen Spannungen? So wählen wir Material und Wandstärke, bevor wir den Prototyp bauen: sicher, ohne schwerer oder teurer als nötig.",
            "load-bearing parts, frames, mounts and moving mechanisms", "tragende Teile, Rahmen, Halterungen und bewegliche Mechanik")}{svc(5, "Prototypes &amp; testing", "Prototypen &amp; Tests",
            "Hold it, test it, improve it.", "In die Hand nehmen, testen, verbessern.",
            "We build printed and working prototypes in rounds, so you can test fit, function and feel early. We test them in our workshop. Where a standard requires it, accredited test labs carry out the tests. Each round brings the product closer to production.",
            "Wir bauen gedruckte und funktionsfähige Prototypen in Runden, damit Sie Passform, Funktion und Haptik früh testen können. Wir testen in der eigenen Werkstatt. Wo eine Norm es verlangt, beauftragen wir akkreditierte Prüfstellen. Jede Runde bringt das Produkt näher an die Serie.",
            "anyone who needs to prove a product before investing in production", "alle, die ein Produkt erproben wollen, bevor sie in die Produktion investieren")}{svc(6, "Construction &amp; documentation", "Konstruktion &amp; Dokumentation",
            "Built for production, documented for your customers.", "Konstruiert für die Fertigung, dokumentiert für Ihre Kunden.",
            "We turn the design into parts that can be built in our workshop or by our manufacturing partners: CAD models, drawings and tolerances. The product we build for you comes with drawings, CAD data, assembly and user manuals, and the technical file.",
            "Wir machen aus dem Design fertigbare Teile für unsere Werkstatt oder unsere Fertigungspartner: CAD-Modelle, Zeichnungen, Toleranzen. Zum Produkt, das wir für Sie bauen, gehören Zeichnungen, CAD-Daten, Montage- und Bedienungsanleitung sowie die technische Dokumentation.",
            "products we develop and build for you", "Produkte, die wir für Sie entwickeln und bauen")}
        </ul>
      </div>

      <div class="svc-group" id="deliver">
        <div class="side">
          <p class="verb">Deliver<span>{t("prototype → market", "Prototyp → Markt")}</span></p>
          <div class="pic contain"><img src="{R}img/studio-classic.webp" alt="{t("Finished OctoStool Classic unit on its base plate", "Fertiger OctoStool Classic auf seiner Bodenplatte")}" loading="lazy"></div>
        </div>
        <ul class="svc-list">{svc(7, "Manufacturing &amp; supply chain", "Fertigung &amp; Lieferkette",
            "One partner from parts to production.", "Ein Partner von den Teilen bis zur Serie.",
            "We set up production using our own metalwork and a network of suppliers, and run the chain for you. You deal with one contact instead of many.",
            "Wir bauen die Produktion mit eigener Metallbearbeitung und einem Lieferantennetzwerk auf und steuern die Kette für Sie. Sie haben einen Ansprechpartner statt vieler.",
            "companies that lack production capacity or supplier contacts", "Unternehmen ohne Produktionskapazität oder Lieferantenkontakte")}{svc(8, "Packaging development", "Verpackungsentwicklung",
            "Ready for the shelf.", "Bereit fürs Regal.",
            "We develop packaging that protects the product, suits shipping and presents your brand.",
            "Wir entwickeln Verpackungen, die das Produkt schützen, sich für den Versand eignen und Ihre Marke präsentieren.",
            "anyone bringing a product to market", "alle, die ein Produkt auf den Markt bringen")}{svc(9, "Worldwide delivery", "Weltweite Lieferung",
            "Made in Innsbruck, shipped worldwide.", "Gefertigt in Innsbruck, geliefert weltweit.",
            "We ship finished products wherever you and your customers are, as single orders or on agreed schedules.",
            "Wir liefern fertige Produkte dorthin, wo Sie und Ihre Kunden sind, als Einzelauftrag oder nach vereinbartem Plan.",
            "B2B and B2C customers in Austria and abroad", "B2B- und B2C-Kunden in Österreich und international")}
        </ul>
      </div>
    </div>
  </section>

  <section class="block process" id="process" aria-labelledby="proc-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("How a project runs", "So läuft ein Projekt ab")}</p>
        <h2 id="proc-title">{t("Eight steps, a result after each one.", "Acht Schritte, nach jedem ein Ergebnis.")}</h2>
        <p class="lead">{t("You see a plan and a budget before anything is built. You can stop after any step and keep what has been made.", "Sie sehen Plan und Budget, bevor etwas gebaut wird. Nach jedem Schritt können Sie aufhören und behalten, was entstanden ist.")}</p>
      </div>
      <ol class="steps">
        <li><span class="n">01</span><h3>{t("Idea and briefing", "Idee und Briefing")}</h3><p>{t("You tell us what the product should do, for whom, and what budget you have in mind.", "Sie erzählen uns, was das Produkt können soll, für wen, und welches Budget Sie sich vorstellen.")}</p></li>
        <li><span class="n">02</span><h3>{t("Plan and concept", "Plan und Konzept")}</h3><p>{t("We return a concept, a project plan and a budget. You decide whether to go ahead.", "Wir liefern Konzept, Projektplan und Budget. Sie entscheiden, ob es weitergeht.")}</p></li>
        <li><span class="n">03</span><h3>{t("Design and 3D models", "Design und 3D-Modelle")}</h3><p>{t("Form and function take shape as 3D models and renderings you can review.", "Form und Funktion entstehen als 3D-Modelle und Renderings, die Sie prüfen können.")}</p></li>
        <li><span class="n">04</span><h3>{t("Prototypes and testing", "Prototypen und Tests")}</h3><p>{t("Printed parts and working prototypes, improved in rounds. We test in-house, or coordinate tests to the relevant standards with accredited test facilities.", "Gedruckte Teile und funktionsfähige Prototypen, in Runden verbessert. Wir testen selbst oder koordinieren normgerechte Prüfungen mit akkreditierten Prüfstellen.")}</p></li>
        <li><span class="n">05</span><h3>{t("Construction, load check and documentation", "Konstruktion, Belastungscheck und Dokumentation")}</h3><p>{t("We construct the parts for our workshop or manufacturing partners, check critical parts with FEA and document the product.", "Wir konstruieren die Teile für unsere Werkstatt oder Fertigungspartner, prüfen kritische Teile per FEM und dokumentieren das Produkt.")}</p></li>
        <li><span class="n">06</span><h3>{t("Production and supply chain", "Produktion und Lieferkette")}</h3><p>{t("We build in our workshop or with suppliers, and manage the chain.", "Wir fertigen in unserer Werkstatt oder bei Lieferanten und steuern die Kette.")}</p></li>
        <li><span class="n">07</span><h3>{t("Packaging", "Verpackung")}</h3><p>{t("Packaging designed to protect, ship and sell.", "Verpackung, die schützt, sich versenden lässt und verkauft.")}</p></li>
        <li><span class="n">08</span><h3>{t("Delivered", "Geliefert")}</h3><p>{t("A market-ready product, delivered to you or straight to your customers.", "Ein marktreifes Produkt, geliefert an Sie oder direkt an Ihre Kunden.")}</p></li>
      </ol>
      <div class="ruler-foot"><span>{t("You bring: idea + budget", "Sie bringen: Idee + Budget")}</span><span>{t("Typical project length: 3 to 6 months", "Typische Projektdauer: 3 bis 6 Monate")}</span><span>{t("You receive: a product ready to sell", "Sie erhalten: ein verkaufsfertiges Produkt")}</span></div>
    </div>
  </section>

  <section class="block who" aria-labelledby="who-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Who we work with", "Für wen wir arbeiten")}</p>
        <h2 id="who-title">{t("The whole chain, or the stage you join at.", "Die ganze Kette oder ab der Phase, in der Sie stehen.")}</h2>
      </div>
      <div class="who-grid">
        <article>
          <h3>{t("Entrepreneurs &amp; founders", "Unternehmer:innen &amp; Gründer:innen")}</h3>
          <p>{t("You have an idea and a budget, but no product team. We become that team, from the first plan to the first shipment.", "Sie haben eine Idee und ein Budget, aber kein Produktteam. Wir werden dieses Team, vom ersten Plan bis zur ersten Lieferung.")}</p>
          <ul><li>{t("A clear plan and budget before building starts", "Klarer Plan und klares Budget, bevor gebaut wird")}</li><li>{t("Renderings to pitch to investors and customers", "Renderings für Investoren und Kunden")}</li><li>{t("One contact for the whole chain", "Ein Ansprechpartner für die ganze Kette")}</li></ul>
        </article>
        <article>
          <h3>{t("Established companies", "Etablierte Unternehmen")}</h3>
          <p>{t("Your team is at capacity or lacks a specific skill. We take on a full product, or join at the stage you are at, from design to prototypes and production.", "Ihr Team ist ausgelastet oder es fehlt eine bestimmte Kompetenz. Wir übernehmen ein ganzes Produkt oder steigen in Ihrer Phase ein, vom Design über Prototypen bis zur Fertigung.")}</p>
          <ul><li>{t("Design and development of products we build for you", "Design und Entwicklung von Produkten, die wir für Sie bauen")}</li><li>{t("Prototyping before you commit to tooling", "Prototypen, bevor Sie in Werkzeuge investieren")}</li><li>{t("Production and supply chain set up for you", "Produktion und Lieferkette für Sie aufgebaut")}</li></ul>
        </article>
      </div>
    </div>
  </section>
{idea_check(faq="#faq")}{faq_block()}{cta_band("Bring the idea. <em>We bring the plan.</em>", "Sie bringen die Idee. <em>Wir den Plan.</em>",
          "Tell us what you want to build. We reply with first thoughts and the next steps.", "Erzählen Sie uns, was Sie bauen möchten. Wir antworten mit ersten Gedanken und den nächsten Schritten.")}
</main>
""" + footer("services")

    # ------------------------------------------------------------------ PRODUCTS
    pages["products"] = head("products", t("Products · OCTOS", "Produkte · OCTOS"),
                             t("Products designed, engineered and built by OCTOS, starting with the OctoStool for barbershops.",
                               "Von OCTOS gestaltete, konstruierte und gebaute Produkte, angefangen mit dem OctoStool für Barbershops.")) + f"""
<main id="top">
  <section class="phead solo" aria-labelledby="pg-title">
    <div class="wrap">
      <div>
        <p class="eyebrow">{t("Products &amp; projects", "Produkte &amp; Projekte")}</p>
        <h1 id="pg-title">{t("Proof of the <em>whole chain.</em>", "Der Beweis für <em>die ganze Kette.</em>")}</h1>
        <p class="lead">{t("Every product here went from idea to market through the same steps we run for clients. Our own products come first; client projects follow as we are allowed to show them.",
                           "Jedes Produkt hier ging durch dieselben Schritte von der Idee bis zum Markt, die wir für Kunden umsetzen. Zuerst unsere eigenen Produkte; Kundenprojekte folgen, sobald wir sie zeigen dürfen.")}</p>
        <div class="ctas">
          <a class="btn btn-wood" href="offer.html">{t("Get an offer", "Angebot anfordern")} <span class="arrow">→</span></a>
          <a class="btn btn-line" href="contact.html">{t("Start your own product", "Eigenes Produkt starten")}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="shelf-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Our products", "Unsere Produkte")}</p>
        <h2 id="shelf-title">{t("Designed, engineered and built in Innsbruck.", "Gestaltet, konstruiert und gebaut in Innsbruck.")}</h2>
      </div>
      <div class="shelf top0">{octo_card}
      </div>
    </div>
  </section>

  <section class="block process" aria-labelledby="cp-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("What drives us", "Was uns antreibt")}</p>
        <blockquote class="quote" id="cp-title"><p>{t("“Design is not just what it looks like and feels like. Design is how it works.”", "„Design ist nicht nur, wie etwas aussieht und sich anfühlt. Design ist, wie es funktioniert.“")}</p><footer>Steve Jobs</footer></blockquote>
      </div>
      <p><a class="btn btn-ink" href="services.html">{t("See what we can do for you", "Was wir für Sie tun können")} <span class="arrow">→</span></a></p>
    </div>
  </section>
{cta_band("Have an idea for a product?", "Eine Idee für ein Produkt?",
          "We take it from first sketch to the shelf, like we did with the OctoStool.", "Wir bringen sie von der ersten Skizze bis ins Regal, so wie beim OctoStool.")}
</main>
""" + footer("products")

    # ------------------------------------------------------------------ OCTOSTOOL
    def chips(*items):
        return '<div class="chips">' + "".join(
            f'<span class="chip"><i style="background:{c}"></i>{n}</span>' if c else f'<span class="chip">{n}</span>'
            for n, c in items) + "</div>"

    pages["octostool"] = head("octostool", t("OctoStool · OCTOS", "OctoStool · OCTOS"),
                              t("The OctoStool: a barber's stool on a swivel arm, mounted to the barber chair. Designed, engineered and built by OCTOS in Innsbruck.",
                                "Der OctoStool: ein Barbierhocker auf einem Schwenkarm, montiert am Barbierstuhl. Gestaltet, konstruiert und gebaut von OCTOS in Innsbruck.")) + f"""
<main id="top">
  <section class="bleed" aria-labelledby="pg-title">
    <img src="{R}img/interior.webp" alt="{t("Barbershop with an OctoStool installed at a barber chair", "Barbershop mit einem OctoStool am Barbierstuhl")}">
    <div class="wrap">
      <p class="eyebrow">{t("Own product · For barbershops", "Eigenes Produkt · Für Barbershops")}</p>
      <h1 id="pg-title">OctoStool</h1>
      <p class="quote-l">{t('"Move like you\'re standing. Feel like you\'re not."', "„Bewegen wie im Stehen. Sitzen wie im Sessel.“")}</p>
      <div class="ctas">
        <a class="btn btn-wood" href="offer.html">{t("Get an offer", "Angebot anfordern")} <span class="arrow">→</span></a>
        <a class="btn btn-line" href="{R}docs/{t("octostool_manual_en.pdf", "octostool_manual_de.pdf")}" download>{t("Download brochure (PDF)", "Broschüre laden (PDF)")}</a>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="what-title">
    <div class="wrap">
      <div class="case-grid">
        <div class="case-copy">
          <p class="eyebrow">{t("What it is", "Was er ist")}</p>
          <h2 id="what-title">{t("Seated, supported, and always within reach.", "Sitzend, gestützt und immer in Reichweite.")}</h2>
          <p>{t("The OctoStool is a barber's stool on a swivel arm, mounted to the base of the barber chair. The barber stays seated and supported while moving around the client, without standing for hours or pushing a loose stool across the floor.",
                "Der OctoStool ist ein Barbierhocker auf einem Schwenkarm, montiert am Fuß des Barbierstuhls. Der Barbier bleibt sitzend gestützt und bewegt sich frei um den Kunden, ohne stundenlang zu stehen oder einen losen Hocker über den Boden zu schieben.")}</p>
          <div class="benefits">
            <div><b>Health<i>+</i></b><small>{t("Less strain on back, legs and shoulders", "Weniger Belastung für Rücken, Beine und Schultern")}</small></div>
            <div><b>Efficiency<i>+</i></b><small>{t("Stay close, precise and in control from every angle", "Nah, präzise und sicher aus jedem Winkel")}</small></div>
            <div><b>Comfort<i>+</i></b><small>{t("Full freedom and reach, fully supported", "Volle Freiheit und Reichweite, voll gestützt")}</small></div>
          </div>
        </div>
        <figure class="reel">
          <video src="{R}img/octostool-commercial.mp4" poster="{R}img/octostool-commercial-poster.jpg" controls playsinline preload="metadata" aria-label="{t("OctoStool commercial: a barber working seated on the OctoStool", "OctoStool-Werbespot: eine Barbierin arbeitet sitzend auf dem OctoStool")}"></video>
          <figcaption>{t("Watch the OctoStool in action · 25 s, with sound", "Der OctoStool im Einsatz · 25 Sek., mit Ton")}</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="block process" aria-labelledby="story-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("From idea to product", "Von der Idee zum Produkt")}</p>
        <h2 id="story-title">{t("Our own idea, through every step we offer.", "Unsere eigene Idee, durch jeden Schritt, den wir anbieten.")}</h2>
        <p class="lead">{t("The OctoStool is how we show clients what the chain produces. The same steps are available for your product.", "Am OctoStool zeigen wir, was unsere Kette hervorbringt. Dieselben Schritte gibt es für Ihr Produkt.")}</p>
      </div>
      <div class="story">
        <figure><div class="im contain"><img src="{R}img/drawing.webp" alt="{t("OctoStool line drawing", "Strichzeichnung des OctoStool")}" loading="lazy"></div><figcaption><b>01 · Design</b><span>{t("Concept and drawing", "Konzept und Zeichnung")}</span><small>{t("Swivel arm, seat and base laid out around the barber chair.", "Schwenkarm, Sitz und Fuß rund um den Barbierstuhl angeordnet.")}</small></figcaption></figure>
        <figure><div class="im"><img src="{R}img/render.webp" alt="{t("3D render of the OctoStool with barber chair", "3D-Rendering des OctoStool mit Barbierstuhl")}" loading="lazy"></div><figcaption><b>02 · {t("Render", "Rendering")}</b><span>{t("3D model and rendering", "3D-Modell und Rendering")}</span><small>{t("Details settled on screen before any metal was cut.", "Details am Bildschirm geklärt, bevor Metall geschnitten wurde.")}</small></figcaption></figure>
        <figure><div class="im contain"><img src="{R}img/fea.webp" alt="{t("FEA displacement plot of the frame under load", "FEM-Verformungsbild des Rahmens unter Last")}" loading="lazy"></div><figcaption><b>03 · Develop</b><span>{t("FEA and engineering", "FEM und Konstruktion")}</span><small>{t("Frame and arm simulated under load before the first part was made.", "Rahmen und Arm unter Last simuliert, bevor das erste Teil gefertigt wurde.")}</small></figcaption></figure>
        <figure><div class="im"><img src="{R}img/footrest.webp" alt="{t("Wooden footrest ring and steel base plate", "Fußring aus Holz und Bodenplatte aus Stahl")}" loading="lazy"></div><figcaption><b>04 · Deliver</b><span>{t("Built and delivered", "Gebaut und geliefert")}</span><small>{t("Steel and wood, made in Innsbruck and installed in barbershops.", "Stahl und Holz, gefertigt in Innsbruck und in Barbershops installiert.")}</small></figcaption></figure>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="opt-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Options &amp; specifications", "Ausführungen &amp; technische Daten")}</p>
        <h2 id="opt-title">{t("Configured for your shop.", "Konfiguriert für Ihren Shop.")}</h2>
      </div>
      <div class="opts">
        <div class="pics">
          <figure><div class="im"><img src="{R}img/studio-ergo.webp" alt="{t("OctoStool with Ergo+ seat mounted to a barber chair", "OctoStool mit Ergo+-Sitz am Barbierstuhl")}" loading="lazy"></div><figcaption>{t("Ergo+ seat, mounted", "Ergo+-Sitz, montiert")}</figcaption></figure>
          <figure><div class="im"><img src="{R}img/studio-classic.webp" alt="{t("OctoStool Classic unit on its base plate", "OctoStool Classic auf seiner Bodenplatte")}" loading="lazy"></div><figcaption>{t("Classic unit on base plate", "Classic auf Bodenplatte")}</figcaption></figure>
        </div>
        <div>
          <table class="opt-table">
            <tr><th scope="row">{t("Seat", "Sitz")}</th><td>{chips(("Ergo+", None), ("Ergo", None), ("Classic+", None), ("Classic", None))}</td></tr>
            <tr><th scope="row">{t("Leather", "Leder")}</th><td>{chips((t("Black", "Schwarz"), "#161616"), (t("Grey", "Grau"), "#8b8b88"), (t("White", "Weiß"), "#f4f3ef"), (t("Individual", "Individuell"), None))}</td></tr>
            <tr><th scope="row">{t("Frame", "Rahmen")}</th><td>{chips((t("Black", "Schwarz"), "#161616"), (t("Custom colour", "Wunschfarbe"), "conic-gradient(#c0392b,#e6a23c,#3a7d44,#2b5d9b,#7a3e9d,#c0392b)"))}</td></tr>
            <tr><th scope="row">{t("Arm", "Arm")}</th><td>{chips((t("Mahogany", "Mahagoni"), "#7a3b22"), (t("Oak", "Eiche"), "#c98d5e"), (t("Powder-coated steel", "Pulverbeschichteter Stahl"), "#2a2a28"))}</td></tr>
          </table>
          <dl class="specs" style="margin-top:28px">
            <dt>{t("Material", "Material")}</dt><dd>{t("Powder-coated steel frame", "Rahmen aus pulverbeschichtetem Stahl")}</dd>
            <dt>{t("Max. load", "Max. Belastung")}</dt><dd>Essential {t("up to", "bis")} 110 kg · Power+ {t("up to", "bis")} 150 kg</dd>
            <dt>{t("Reach", "Reichweite")}</dt><dd>{t("50–70 cm horizontal", "50–70 cm horizontal")}</dd>
            <dt>{t("Swivel", "Schwenkbereich")}</dt><dd>210°</dd>
            <dt>{t("Seat", "Sitz")}</dt><dd>{t("Detachable, height adjustable", "Abnehmbar, höhenverstellbar")}</dd>
            <dt>{t("Parking", "Parken")}</dt><dd>{t("Park position with magnetic lock", "Parkposition mit Magnetverriegelung")}</dd>
          </dl>
        </div>
      </div>
    </div>
  </section>

  <section class="block process" aria-labelledby="gal-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Gallery", "Galerie")}</p>
        <h2 id="gal-title">{t("In the barbershop.", "Im Barbershop.")}</h2>
      </div>
      <div class="gallery">
        <figure class="g1"><img src="{R}img/interior.webp" alt="{t("Barbershop interior with the OctoStool at a barber chair", "Barbershop mit OctoStool am Barbierstuhl")}" loading="lazy"><figcaption>{t("Installed", "Installiert")}</figcaption></figure>
        <figure class="g2"><img src="{R}img/handle.webp" alt="{t("Hand on the OctoStool handle with the OCTOS logo", "Hand am OctoStool-Griff mit OCTOS-Logo")}" loading="lazy"><figcaption>{t("Handle", "Griff")}</figcaption></figure>
        <figure class="g3"><img src="{R}img/footrest.webp" alt="{t("Wooden footrest ring and base plate", "Fußring aus Holz und Bodenplatte")}" loading="lazy"><figcaption>{t("Footrest", "Fußring")}</figcaption></figure>
        <figure class="g4"><img src="{R}img/height-1.webp" alt="{t("Seated barber adjusting the seat height", "Sitzender Barbier verstellt die Sitzhöhe")}" loading="lazy"><figcaption>{t("Height adjustment", "Höhenverstellung")}</figcaption></figure>
        <figure class="g5"><img src="{R}img/height-2.webp" alt="{t("Seat height adjustment from the side", "Höhenverstellung von der Seite")}" loading="lazy"><figcaption>{t("Seated at the chair", "Sitzend am Stuhl")}</figcaption></figure>
        <figure class="g6"><img src="{R}img/barber-at-work.webp" alt="{t("Barber at work on the OctoStool", "Barbier bei der Arbeit auf dem OctoStool")}" loading="lazy"><figcaption>{t("At work", "Bei der Arbeit")}</figcaption></figure>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="buy-title">
    <div class="wrap">
      <h2 id="buy-title" class="eyebrow" style="font:500 .75rem/1.3 var(--mono);margin-bottom:20px">{t("Get the OctoStool", "OctoStool bestellen")}</h2>
      <div class="buy">
        <div class="dark">
          <h3>{t("Request an offer", "Angebot anfordern")}</h3>
          <p>{t("Choose Essential or Power+, your options and the quantity. We send you a written offer.", "Wählen Sie Essential oder Power+, Ihre Ausführung und die Stückzahl. Wir senden Ihnen ein schriftliches Angebot.")}</p>
          <div class="row"><a class="btn btn-wood" href="offer.html">{t("Get an offer", "Angebot anfordern")} <span class="arrow">→</span></a></div>
        </div>
        <div>
          <h3>{t("Brochure &amp; advice", "Broschüre &amp; Beratung")}</h3>
          <p>{t("All options and specs on two pages. For larger orders or an individual finish, get in touch.", "Alle Ausführungen und Daten auf zwei Seiten. Für größere Bestellungen oder eine individuelle Ausführung melden Sie sich bei uns.")}</p>
          <div class="row">
            <a class="btn btn-ink" href="{R}docs/octostool_manual_en.pdf" download>{t("Brochure EN (PDF)", "Broschüre EN (PDF)")}</a>
            <a class="btn btn-ink" href="{R}docs/octostool_manual_de.pdf" download>{t("Brochure DE (PDF)", "Broschüre DE (PDF)")}</a>
            <a class="btn btn-line on-light" href="contact.html">{t("Contact us", "Kontakt")}</a>
          </div>
        </div>
      </div>
    </div>
  </section>
{cta_band("Want a product like this <em>for your business?</em>", "Ein Produkt wie dieses <em>für Ihr Unternehmen?</em>",
          "We designed, engineered and built the OctoStool ourselves. We can do the same for your idea.", "Den OctoStool haben wir selbst gestaltet, konstruiert und gebaut. Dasselbe können wir für Ihre Idee tun.")}
</main>
""" + footer("octostool")

    # ------------------------------------------------------------------ ABOUT
    pages["about"] = head("about", t("About · OCTOS", "Über uns · OCTOS"),
                          t("OCTOS designs, develops and delivers meaningful products for entrepreneurs and companies, with a team covering industrial design, metal manufacturing, materials science, electronics, medical devices, packaging and brand.",
                            "OCTOS gestaltet, entwickelt und liefert sinnvolle Produkte für Gründer und Unternehmen, mit einem Team aus Industriedesign, Metalltechnik, Materialwissenschaft, Elektronik, Medizintechnik, Verpackung und Marke.")) + f"""
<main id="top">
  <section class="phead about-head" aria-labelledby="pg-title">
    <div class="wrap">
      <div>
        <p class="eyebrow">{t("About us", "Über uns")}</p>
        <h1 id="pg-title" class="brand-h1">OCTOS</h1>
        <p class="lead mission"><b>{t("Our mission:", "Unsere Mission:")}</b> {t("to turn good ideas into meaningful products. Engineered to last, built with care and delivered ready for the market.",
                           "aus guten Ideen sinnvolle Produkte zu machen. Gebaut für die Dauer, mit Sorgfalt gefertigt und marktreif geliefert.")}</p>
        <p class="slogan-line">We Design, We Develop, We Deliver</p>
      </div>
      <div class="stand" aria-labelledby="stand-title">
        <p class="eyebrow" id="stand-title">{t("What we stand for", "Wofür wir stehen")}</p>
        <ul>
          <li><b>{t("Meaningful products", "Sinnvolle Produkte")}</b><small>{t("We build what solves a real problem for the people who use it every day. No gadgets for the drawer.", "Wir bauen, was ein echtes Problem für die Menschen löst, die es täglich nutzen. Keine Gadgets für die Schublade.")}</small></li>
          <li><b>{t("Engineered quality", "Durchdachte Qualität")}</b><small>{t("The rigour of a highly regulated industry: calculated, tested and documented.", "Die Sorgfalt einer streng regulierten Branche: berechnet, geprüft und dokumentiert.")}</small></li>
          <li><b>{t("One team, the whole chain", "Ein Team, die ganze Kette")}</b><small>{t("From the first sketch to delivery, one contact and no lost handovers.", "Von der ersten Skizze bis zur Lieferung, ein Ansprechpartner und keine verlorenen Übergaben.")}</small></li>
          <li><b>{t("Never stop learning", "Niemals aufhören zu lernen")}</b><small>{t("Every project teaches us something new, and every client benefits from it.", "Jedes Projekt lehrt uns etwas Neues, und jeder Kunde profitiert davon.")}</small></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="story-title">
    <div class="wrap">
      <div class="prose founder-short">
        <p class="eyebrow">{t("How it started", "Wie alles begann")}</p>
        <h2 id="story-title">{t("Founded in Innsbruck.", "Gegründet in Innsbruck.")}</h2>
        <p>{t("OCTOS was founded in 2026 by Ing. Daniel Varga, a mechanical engineer from Innsbruck. After his engineering degree at HTL Anichstraße and further studies in engineering and physics, he spent more than 12 years in the medical device industry, where he learned to design for safety and document every decision. Growing up between the mountains, with skiing, the gym and squash as constant companions, taught him focus and stamina. Today he brings it all together at OCTOS, with one ambition: never stop learning, and put every new skill to work for our clients.",
              "OCTOS wurde 2026 von Ing. Daniel Varga gegründet, einem Maschinenbauingenieur aus Innsbruck. Nach seiner Ingenieursausbildung an der HTL Anichstraße und weiteren Studien in Ingenieurwesen und Physik war er über 12 Jahre in der Medizintechnik tätig, wo er gelernt hat, auf Sicherheit hin zu konstruieren und jede Entscheidung zu dokumentieren. Aufgewachsen zwischen den Bergen, mit Skifahren, Fitnessstudio und Squash als ständigen Begleitern, hat er Fokus und Ausdauer gelernt. Heute vereint er all das bei OCTOS, mit einem Anspruch: niemals aufhören zu lernen und jede neue Fähigkeit für unsere Kunden einzusetzen.")}</p>
      </div>
    </div>
  </section>

  <section class="block process" aria-labelledby="skills-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("The team", "Das Team")}</p>
        <h2 id="skills-title">{t("One team. <em>The whole chain.</em>", "Ein Team. <em>Die ganze Kette.</em>")}</h2>
        <p class="lead">{t("Behind OCTOS stands a team of experienced specialists. From the first sketch to the film that launches your product, every skill sits at one table, so your project moves fast, stays consistent and never gets lost between suppliers.",
                           "Hinter OCTOS steht ein Team erfahrener Spezialisten. Von der ersten Skizze bis zum Film, der Ihr Produkt vorstellt, sitzt jede Kompetenz an einem Tisch: Ihr Projekt kommt schnell voran, bleibt aus einem Guss und geht nie zwischen Lieferanten verloren.")}</p>
      </div>
      <div class="skills">
        <article><h3>{t("Product management", "Produktmanagement")}</h3><p>{t("Experienced in leading products from idea to launch: requirements, budget, timeline and suppliers, all in hand.", "Erfahren darin, Produkte von der Idee bis zur Markteinführung zu führen: Anforderungen, Budget, Zeitplan und Lieferanten fest im Griff.")}</p></article>
        <article><h3>{t("Materials science", "Materialwissenschaft")}</h3><p>{t("A PhD in materials science: the right material for every part, for strength, wear, weight, cost and processing.", "Promotion in Materialwissenschaft: der richtige Werkstoff für jedes Teil, nach Festigkeit, Verschleiß, Gewicht, Kosten und Verarbeitung.")}</p></article>
        <article><h3>{t("Electronic engineering", "Elektronik")}</h3><p>{t("Sensors, controls and power, developed hand in hand with the mechanics.", "Sensorik, Steuerung und Stromversorgung, Hand in Hand mit der Mechanik entwickelt.")}</p></article>
        <article><h3>{t("Medical devices &amp; technology", "Medizintechnik &amp; Technologie")}</h3><p>{t("Over 20 years combined in one of the most highly regulated industries: risk management, documentation and testing to standards.", "Über 20 Jahre gemeinsam in einer der am strengsten regulierten Branchen: Risikomanagement, Dokumentation und normgerechte Prüfungen.")}</p></article>
        <article><h3>{t("Packaging engineering", "Verpackungstechnik")}</h3><p>{t("Packaging that protects the product, ships efficiently and looks ready for the shelf.", "Verpackungen, die das Produkt schützen, effizient versendet werden und fertig fürs Regal aussehen.")}</p></article>
        <article><h3>{t("Mechanical engineering", "Maschinenbau")}</h3><p>{t("Design, CAD and load checks for the parts and mechanisms we build, so they hold up under real loads.", "Konstruktion, CAD und Belastungschecks für die Teile und Mechanik, die wir bauen, damit sie echten Belastungen standhalten.")}</p></article>
        <article><h3>{t("3D printing &amp; prototyping", "3D-Druck &amp; Prototypenbau")}</h3><p>{t("Fast, functional prototypes and parts straight from CAD, so ideas can be tested in the hand within days.", "Schnelle, funktionsfähige Prototypen und Teile direkt aus dem CAD, damit Ideen in wenigen Tagen in der Hand getestet werden können.")}</p></article>
        <article><h3>{t("Footage creation", "Videoproduktion")}</h3><p>{t("Filming and editing: product films, social clips and commercials that show your product at its best.", "Filmen und Schneiden: Produktfilme, Social Clips und Werbespots, die Ihr Produkt von seiner besten Seite zeigen.")}</p></article>
        <article><h3>{t("Logo design &amp; brand creation", "Logodesign &amp; Markenaufbau")}</h3><p>{t("A clear, memorable mark and a brand as well engineered as the product behind it, from name and look to the story you tell.", "Ein klares, einprägsames Zeichen und eine Marke, so durchdacht wie das Produkt dahinter, von Name und Erscheinungsbild bis zur Geschichte, die Sie erzählen.")}</p></article>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="facts-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("At a glance", "Auf einen Blick")}</p>
        <h2 id="facts-title">{t("Experience you can build on.", "Erfahrung, auf die Sie bauen können.")}</h2>
      </div>
      <div class="facts">
        <div><b>20+ {t("years", "Jahre")}</b><small>{t("Combined team experience in the medical device industry", "Gemeinsame Team-Erfahrung in der Medizintechnik")}</small></div>
        <div><b>PhD</b><small>{t("Materials science, in the team", "Materialwissenschaft im Team")}</small></div>
        <div><b>9</b><small>{t("Disciplines under one roof, from engineering to film", "Disziplinen unter einem Dach, vom Engineering bis zum Film")}</small></div>
        <div><b>{t("Since 2026", "Seit 2026")}</b><small>{t("Based in Innsbruck, shipping worldwide", "Sitz in Innsbruck, Lieferung weltweit")}</small></div>
      </div>
    </div>
  </section>

  <section class="block process" aria-labelledby="kit-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("In-house", "Im Haus")}</p>
        <h2 id="kit-title">{t("From screen to workshop, under one roof.", "Vom Bildschirm in die Werkstatt, unter einem Dach.")}</h2>
        <p class="lead">{t("What we can't make ourselves, we make with our manufacturing partners, managed by us.", "Was wir nicht selbst fertigen, fertigen wir mit unseren Fertigungspartnern, gesteuert von uns.")}</p>
      </div>
      <ul class="kit">
        <li><b>{t("3D CAD software", "3D-CAD-Software")}</b><small>{t("Modelling, rendering and load checks", "Modellierung, Rendering und Belastungschecks")}</small></li>
        <li><b>{t("Mechanical workshop", "Mechanische Werkstatt")}</b><small>{t("Metalwork for prototypes and small series", "Metallbearbeitung für Prototypen und Kleinserien")}</small></li>
        <li><b>{t("Wood workshop", "Holzwerkstatt")}</b><small>{t("Wooden parts like the OctoStool footrest and arm", "Holzteile wie Fußring und Arm des OctoStool")}</small></li>
        <li><b>{t("3D printers", "3D-Drucker")}</b><small>{t("Fast iterations of parts and prototypes", "Schnelle Iterationen von Teilen und Prototypen")}</small></li>
        <li><b>{t("Welding", "Schweißen")}</b><small>{t("Steel frames and assemblies", "Stahlrahmen und Baugruppen")}</small></li>
        <li><b>{t("Manufacturing partners", "Fertigungspartner")}</b><small>{t("Series production and processes beyond our workshop", "Serienfertigung und Verfahren über unsere Werkstatt hinaus")}</small></li>
      </ul>
    </div>
  </section>

  <section class="block" aria-labelledby="clients-title">
    <div class="wrap two">
      <div class="prose">
        <p class="eyebrow">{t("Who we work with", "Für wen wir arbeiten")}</p>
        <h2 id="clients-title">{t("Entrepreneurs with an idea. Companies that need a hand.", "Gründer mit einer Idee. Unternehmen, die Unterstützung brauchen.")}</h2>
        <p>{t("We work with entrepreneurs on custom-made products, from the first sketch to a product they can sell. And we support companies where their own team is short on time or a specific skill: design, materials, prototypes, testing, documentation or production of the products we build for them.",
              "Wir arbeiten mit Gründerinnen und Gründern an maßgefertigten Produkten, von der ersten Skizze bis zum verkaufsfertigen Produkt. Und wir unterstützen Unternehmen, wo dem eigenen Team Zeit oder eine bestimmte Kompetenz fehlt: Design, Werkstoffe, Prototypen, Prüfungen, Dokumentation oder Fertigung der Produkte, die wir für sie bauen.")}</p>
        <p>{t("Client projects stay confidential. We show them here only with permission.", "Kundenprojekte bleiben vertraulich. Wir zeigen sie hier nur mit Freigabe.")}</p>
      </div>
      <ul class="kit kit-1">
        <li><b>{t("Custom-made products", "Maßgefertigte Produkte")}</b><small>{t("For entrepreneurs, from idea to market", "Für Gründer, von der Idee bis zum Markt")}</small></li>
        <li><b>{t("Product development support", "Unterstützung in der Produktentwicklung")}</b><small>{t("For companies, from the stage you are at or the whole chain", "Für Unternehmen, ab Ihrer Phase oder die ganze Kette")}</small></li>
        <li><b>{t("Materials &amp; testing", "Werkstoffe &amp; Prüfungen")}</b><small>{t("Material selection and tests to standards", "Werkstoffauswahl und normgerechte Prüfungen")}</small></li>
      </ul>
    </div>
  </section>

  <section class="block" aria-labelledby="val-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("How we work", "Wie wir arbeiten")}</p>
        <h2 id="val-title">OCTOS - We Design, We Develop, We Deliver</h2>
        <p class="lead">Efficiency Engineered, Comfort Assured</p>
      </div>
      <div class="values">
        <article><h3>We Design</h3><p>{t("Custom-made mechanical designs, shaped around the people who will use them.", "Maßgeschneiderte mechanische Konstruktionen, ausgerichtet auf die Menschen, die sie nutzen.")}</p></article>
        <article><h3>We Develop</h3><p>{t("Engineered in the best quality, to high Austrian standards, and documented so others can build it.", "In bester Qualität nach hohen österreichischen Standards entwickelt und so dokumentiert, dass andere es bauen können.")}</p></article>
        <article><h3>We Deliver</h3><p>{t("No matter where you are, we ship globally, as single pieces or in series.", "Egal wo Sie sind, wir liefern weltweit, als Einzelstück oder in Serie.")}</p></article>
      </div>
      <dl class="specs" style="margin-top:48px">
        <dt>{t("Company", "Unternehmen")}</dt><dd>OCTOS e.U., Innsbruck</dd>
        <dt>{t("Memberships", "Mitgliedschaften")}</dt><dd>Wirtschaftskammer Tirol: Landesinnung Metalltechniker, Fachgruppe Gewerbliche Dienstleister, Landesgremium Elektro- und Einrichtungsfachhandel</dd>
        <dt>{t("Trade licences", "Gewerbeberechtigungen")}</dt><dd>{t("Metalltechnik für Metall- und Maschinenbau (craft, § 94 Z 59 GewO); Design/Industrial Design (free trade); Handelsgewerbe, trading business (free trade)", "Metalltechnik für Metall- und Maschinenbau (Handwerk, § 94 Z 59 GewO); Design/Industrial Design (freies Gewerbe); Handelsgewerbe (freies Gewerbe)")}</dd>
      </dl>
    </div>
  </section>
{cta_band("Let's start something <em>great together.</em>", "Lassen Sie uns <em>gemeinsam starten.</em>",
          "Tell us about your idea. We reply with first thoughts and the next steps.", "Erzählen Sie uns von Ihrer Idee. Wir antworten mit ersten Gedanken und den nächsten Schritten.")}
</main>
""" + footer("about")

    # ------------------------------------------------------------------ CONTACT
    next_steps = f"""
        <ol class="next" aria-label="{t("What happens next", "Wie es weitergeht")}">
          <li><b>01</b><span>{t("We read your inquiry", "Wir lesen Ihre Anfrage")}</span><small>{t("and reply with first thoughts and questions.", "und antworten mit ersten Gedanken und Fragen.")}</small></li>
          <li><b>02</b><span>{t("A short call", "Ein kurzes Gespräch")}</span><small>{t("to understand the product, the market and your budget.", "um Produkt, Markt und Budget zu verstehen.")}</small></li>
          <li><b>03</b><span>{t("Plan and offer", "Plan und Angebot")}</span><small>{t("a concept, a project plan and a price before anything is built.", "Konzept, Projektplan und Preis, bevor etwas gebaut wird.")}</small></li>
        </ol>"""
    pages["contact"] = head("contact", t("Contact · OCTOS", "Kontakt · OCTOS"),
                            t("Start your project with OCTOS in Innsbruck: info@octos.at, +43 670 6500 200.",
                              "Starten Sie Ihr Projekt mit OCTOS in Innsbruck: info@octos.at, +43 670 6500 200.")) + f"""
<main id="top">
{contact_block("h1", idea_check(True) + next_steps)}
  <section class="block" aria-labelledby="visit-title">
    <div class="wrap">
      <div class="block-head">
        <p class="eyebrow">{t("Other ways to reach us", "Weitere Wege zu uns")}</p>
        <h2 id="visit-title">{t("Follow us, or order an OctoStool.", "Folgen Sie uns oder bestellen Sie einen OctoStool.")}</h2>
        <p class="lead">{t("We work digitally: by email, phone and video call, with clients in Austria and abroad.", "Wir arbeiten digital: per E-Mail, Telefon und Videocall, mit Kunden in Österreich und international.")}</p>
      </div>
      <div class="map">
        <div>
          <h3>{t("Follow OCTOS", "OCTOS folgen")}</h3>
          <p>{t("New projects, behind the scenes and the OctoStool in action.", "Neue Projekte, Blicke hinter die Kulissen und der OctoStool im Einsatz.")}</p>
          <div class="social social-list">{social_icons(True)}</div>
        </div>
        <div>
          <h3>{t("Buying an OctoStool?", "Einen OctoStool kaufen?")}</h3>
          <p>{t("Barbershops and resellers can request a written offer for Essential or Power+, with the options and quantity they need.", "Barbershops und Händler können ein schriftliches Angebot für Essential oder Power anfordern, mit der gewünschten Ausführung und Stückzahl.")}</p>
          <p><a class="btn btn-ink" href="offer.html">{t("Get an offer", "Angebot anfordern")} <span class="arrow">→</span></a></p>
        </div>
      </div>
    </div>
  </section>
</main>
""" + footer("contact")

    # ------------------------------------------------------------------ OFFER (OctoStool request)
    def sel(id_, label, opts):
        o = "".join(f"<option>{x}</option>" for x in opts)
        return f'<div class="f"><label for="{id_}">{label}</label><select id="{id_}">{o}</select></div>'

    pages["offer"] = head("offer", t("Get an offer · OCTOS", "Angebot anfordern · OCTOS"),
                          t("Request a written offer for the OctoStool Essential or Power+, for barbershops and resellers.",
                            "Fordern Sie ein schriftliches Angebot für den OctoStool Essential oder Power+ an, für Barbershops und Händler.")) + f"""
<main id="top">
  <section class="phead" aria-labelledby="pg-title">
    <div class="wrap">
      <div>
        <p class="eyebrow">OctoStool · {t("Request an offer", "Angebot anfordern")}</p>
        <h1 id="pg-title">{t("Your OctoStool, <em>configured.</em>", "Ihr OctoStool, <em>konfiguriert.</em>")}</h1>
        <p class="lead">{t("Choose the version, options and quantity. We reply with a written offer including price, delivery time and shipping.",
                           "Wählen Sie Version, Ausführung und Stückzahl. Wir antworten mit einem schriftlichen Angebot inklusive Preis, Lieferzeit und Versand.")}</p>
        <ol class="next" aria-label="{t("How it works", "So funktioniert es")}">
          <li><b>01</b><span>{t("Configure", "Konfigurieren")}</span><small>{t("Version, options and quantity", "Version, Ausführung und Stückzahl")}</small></li>
          <li><b>02</b><span>{t("Get your offer", "Angebot erhalten")}</span><small>{t("Price, delivery time and shipping, in writing", "Preis, Lieferzeit und Versand, schriftlich")}</small></li>
          <li><b>03</b><span>{t("Confirm and receive", "Bestätigen und erhalten")}</span><small>{t("Made in Austria, delivered to your door", "Gefertigt in Österreich, geliefert bis vor die Tür")}</small></li>
        </ol>
      </div>
      <figure class="white"><img src="{R}img/studio-ergo.webp" alt="{t("OctoStool with Ergo+ seat mounted to a barber chair", "OctoStool mit Ergo+-Sitz am Barbierstuhl")}"><figcaption>OctoStool</figcaption></figure>
    </div>
  </section>

  <section class="block" aria-labelledby="form-title">
    <div class="wrap">
      <h2 id="form-title" class="eyebrow" style="font:500 .75rem/1.3 var(--mono);margin-bottom:20px">{t("Offer request", "Angebotsanfrage")}</h2>
      <form class="offer" id="offer" novalidate>
        <fieldset>
          <legend><b>01</b>{t("You are", "Sie sind")}</legend>
          <div class="pick">
            <label class="opt"><input type="radio" name="o-type" id="o-type-shop" value="barbershop" checked><span><b>Barbershop</b><small>{t("For use in your own shop", "Für den Einsatz im eigenen Shop")}</small></span></label>
            <label class="opt"><input type="radio" name="o-type" id="o-type-trade" value="reseller"><span><b>{t("Reseller / wholesale", "Händler / Großhandel")}</b><small>{t("For resale to barbershops", "Für den Weiterverkauf an Barbershops")}</small></span></label>
          </div>
          <label class="opt docs" id="o-docs-row" hidden><input type="checkbox" id="o-docs" value="docs"><span><b>{t("Send me the user manual and technical datasheet", "Bitte Bedienungsanleitung und technisches Datenblatt zusenden")}</b><small>{t("For resellers and wholesale: we send both with your offer.", "Für Händler und Großhandel: Wir senden beides mit Ihrem Angebot.")}</small></span></label>
        </fieldset>

        <fieldset>
          <legend><b>02</b>{t("Version and quantity", "Version und Stückzahl")}</legend>
          <div class="pick">
            <div class="opt model"><label for="o-ess"><input type="checkbox" id="o-ess" value="essential"><span><b>OctoStool Essential</b><small>{t("Durable, for loads up to 110 kg", "Robust, belastbar bis 110 kg")}</small></span></label>
              <div class="f qty"><label for="o-ess-q">{t("Quantity", "Stückzahl")}</label><input id="o-ess-q" type="number" min="1" value="1" inputmode="numeric" disabled></div></div>
            <div class="opt model"><label for="o-pow"><input type="checkbox" id="o-pow" value="power-plus"><span><b>OctoStool Power+</b><small>{t("Extra durable, for loads up to 150 kg", "Extra robust, belastbar bis 150 kg")}</small></span></label>
              <div class="f qty"><label for="o-pow-q">{t("Quantity", "Stückzahl")}</label><input id="o-pow-q" type="number" min="1" value="1" inputmode="numeric" disabled></div></div>
          </div>
        </fieldset>

        <fieldset>
          <legend><b>03</b>{t("Options", "Ausführung")}</legend>
          <div class="grid">
            {sel("o-seat", t("Seat", "Sitz"), ["Ergo+", "Ergo", "Classic+", "Classic"])}
            {sel("o-leather", t("Leather", "Leder"), [t("Black", "Schwarz"), t("Grey", "Grau"), t("White", "Weiß"), t("Individual (please describe below)", "Individuell (bitte unten beschreiben)")])}
            {sel("o-frame", t("Frame", "Rahmen"), [t("Black", "Schwarz"), t("Custom colour (please describe below)", "Wunschfarbe (bitte unten angeben)")])}
            {sel("o-arm", t("Arm", "Arm"), [t("Mahogany", "Mahagoni"), t("Oak", "Eiche"), t("Powder-coated steel", "Pulverbeschichteter Stahl")])}
          </div>
          <p class="hint">{t("The same options are available for Essential and Power+. ", "Essential und Power+ gibt es mit denselben Optionen. ")}{t("Ordering several units in different finishes? Choose the main one here and list the rest in the message.", "Mehrere Stück in unterschiedlicher Ausführung? Wählen Sie hier die Hauptvariante und beschreiben Sie den Rest in der Nachricht.")}</p>
        </fieldset>

        <fieldset>
          <legend><b>04</b>{t("Your details", "Ihre Angaben")}</legend>
          <div class="grid">
            <div class="f wide"><label for="o-co">{t("Company name", "Firmenname")}</label><input id="o-co" type="text" autocomplete="organization"></div>
            <div class="f"><label for="o-name">{t("Contact name", "Ansprechperson")}</label><input id="o-name" type="text" autocomplete="name"></div>
            <div class="f"><label for="o-mail">E-Mail</label><input id="o-mail" type="email" autocomplete="email"></div>
            <div class="f wide"><label for="o-street">{t("Street and number", "Straße und Hausnummer")}</label><input id="o-street" type="text" autocomplete="street-address"></div>
            <div class="f"><label for="o-zip">{t("Postcode and city", "PLZ und Ort")}</label><input id="o-zip" type="text" autocomplete="address-level2"></div>
            <div class="f"><label for="o-country">{t("Country", "Land")}</label><input id="o-country" type="text" autocomplete="country-name" value="{t("Austria", "Österreich")}"></div>
            <div class="f"><label for="o-phone">{t("Phone (optional)", "Telefon (optional)")}</label><input id="o-phone" type="tel" autocomplete="tel"></div>
            <div class="f"><label for="o-vat">{t("VAT ID (optional)", "UID-Nummer (optional)")}</label><input id="o-vat" type="text"></div>
            <div class="f wide"><label for="o-msg">{t("Message (optional)", "Nachricht (optional)")}</label><textarea id="o-msg" placeholder="{t("Delivery date, special finishes, questions", "Liefertermin, Sonderausführungen, Fragen")}"></textarea></div>
          </div>
        </fieldset>

        <div class="send">
          <button class="btn btn-wood" type="submit">{t("Get offer", "Angebot erhalten")} <span class="arrow">→</span></button>
          <p class="note" id="o-note">{t(f'Pressing the button opens your email app with everything filled in, so you only need to press send. No email app? Write to <a href="mailto:{MAIL}">{MAIL}</a>.', f'Der Button öffnet Ihr E-Mail-Programm mit allen Angaben, Sie müssen nur noch senden. Kein E-Mail-Programm? Schreiben Sie an <a href="mailto:{MAIL}">{MAIL}</a>.')}</p>
        </div>
      </form>
    </div>
  </section>
</main>
""" + footer("offer")

    # ------------------------------------------------------------------ IMPRESSUM / DATENSCHUTZ / AGB
    pages["impressum"] = head("impressum", t("Legal notice · OCTOS", "Impressum · OCTOS"),
                              t("Legal notice (Impressum), privacy policy and terms of OCTOS e.U., Innsbruck.",
                                "Impressum, Datenschutzerklärung und AGB der OCTOS e.U., Innsbruck.")) + f"""
<main id="top">
  <section class="phead solo" aria-labelledby="pg-title">
    <div class="wrap">
      <div>
        <p class="eyebrow">{t("Legal", "Rechtliches")}</p>
        <h1 id="pg-title">{t("Legal notice, privacy and terms.", "Impressum, Datenschutz und AGB.")}</h1>
        <nav class="legal-nav" aria-label="{t("On this page", "Auf dieser Seite")}">
          <a href="#impressum">Impressum</a><a href="#datenschutz">{t("Privacy", "Datenschutz")}</a><a href="#agb">{t("Terms (AGB)", "AGB")}</a>
        </nav>
      </div>
    </div>
  </section>

  <section class="block" aria-label="{t("Legal information", "Rechtliche Informationen")}">
    <div class="wrap">
      <div class="legal-sec" id="impressum">
        <h2>Impressum</h2>
        <p class="eyebrow" style="margin-bottom:16px">{t("Information according to § 5 ECG and § 25 MedienG", "Informationen gemäß § 5 ECG und § 25 MedienG")}</p>
        <dl class="kv">
          <dt>{t("Company name", "Firmenname")}</dt><dd>OCTOS e.U. ({t("registered sole proprietorship", "eingetragenes Einzelunternehmen")})</dd>
          <dt>{t("Owner", "Inhaber")}</dt><dd>Ing. Daniel Varga</dd>
          <dt>{t("Registered office", "Sitz")}</dt><dd>Innrain 103, 6020 Innsbruck, {t("Austria", "Österreich")}</dd>
          <dt>{t("Company register no.", "Firmenbuchnummer")}</dt><dd>FN 676155 x</dd>
          <dt>{t("Register court", "Firmenbuchgericht")}</dt><dd>Landesgericht Innsbruck</dd>
          <dt>{t("VAT ID (UID)", "UID-Nummer")}</dt><dd>ATU83179524</dd>
          <dt>{t("Trade licences", "Gewerbeberechtigungen")}</dt><dd>{t("Metalltechnik für Metall- und Maschinenbau (craft, § 94 Z 59 GewO); Design/Industrial Design (free trade); Handelsgewerbe, trading business (free trade)", "Metalltechnik für Metall- und Maschinenbau (Handwerk, § 94 Z 59 GewO); Design/Industrial Design (freies Gewerbe); Handelsgewerbe (freies Gewerbe)")}</dd>
          <dt>{t("Supervisory authority", "Aufsichtsbehörde")}</dt><dd>Bezirkshauptmannschaft Innsbruck</dd>
          <dt>{t("Applicable regulations", "Anwendbare Rechtsvorschriften")}</dt><dd>{t("Trade law", "Berufsrecht")}: Gewerbeordnung, <a href="https://www.ris.bka.gv.at" target="_blank" rel="noopener">www.ris.bka.gv.at</a></dd>
          <dt>{t("Memberships", "Mitgliedschaften")}</dt><dd>Wirtschaftskammer Tirol: Landesinnung Metalltechniker, Fachgruppe Gewerbliche Dienstleister, Landesgremium Elektro- und Einrichtungsfachhandel</dd>
          <dt>E-Mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd>
          <dt>{t("Phone", "Telefon")}</dt><dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd>
        </dl>
      </div>

      <div class="legal-sec" id="datenschutz">
        <h2>{t("Privacy policy", "Datenschutzerklärung")}</h2>
        <div class="legal-text">
          <p><b>{t("Controller", "Verantwortlicher")}:</b> OCTOS e.U., Innrain 103, 6020 Innsbruck, {t("Austria", "Österreich")} · <a href="mailto:{MAIL}">{MAIL}</a></p>
          <h3>{t("Cookies and storage", "Cookies und Speicherung")}</h3>
          <p>{t("This website does not set cookies and does not store data in your browser.", "Diese Website setzt keine Cookies und speichert keine Daten in Ihrem Browser.")}</p>
          <h3>{t("Contact form and email", "Kontaktformular und E-Mail")}</h3>
          <p>{t("Our forms do not send data through this website: they open your own email app with your details filled in, and you decide whether to send the email. The details you send us (name, email, company, address, project description) are processed only to handle your inquiry and are not passed on to third parties.",
                "Unsere Formulare übertragen keine Daten über diese Website: Sie öffnen Ihr eigenes E-Mail-Programm mit Ihren Angaben, und Sie entscheiden, ob Sie die E-Mail senden. Die Angaben, die Sie uns senden (Name, E-Mail, Firma, Adresse, Projektbeschreibung), werden nur zur Bearbeitung Ihrer Anfrage verarbeitet und nicht an Dritte weitergegeben.")}</p>
          <h3>{t("Your rights", "Ihre Rechte")}</h3>
          <p>{t("You have the right to access, rectification, erasure, restriction and objection. You can lodge a complaint with the Austrian Data Protection Authority (Datenschutzbehörde).",
                "Ihnen stehen die Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung und Widerspruch zu. Beschwerden können Sie bei der österreichischen Datenschutzbehörde einbringen.")}</p>
          <h3>{t("Hosting", "Hosting")}</h3>
          <p>{t("This website is hosted on GitHub Pages, a service of GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. When you visit the site, GitHub processes technically necessary data, in particular your IP address, in server log files to deliver the website and keep it secure (Art. 6(1)(f) GDPR). Data may be transferred to the USA; the transfer is based on the EU-US Data Privacy Framework and the EU standard contractual clauses. Details: ",
                "Diese Website wird über GitHub Pages gehostet, einen Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der Website verarbeitet GitHub technisch notwendige Daten, insbesondere Ihre IP-Adresse, in Server-Logfiles, um die Website auszuliefern und ihre Sicherheit zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO). Dabei können Daten in die USA übermittelt werden; die Übermittlung stützt sich auf das EU-US Data Privacy Framework und die EU-Standardvertragsklauseln. Details: ")}<a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub Privacy Statement</a>.</p>
          <h3>{t("Fonts", "Schriftarten")}</h3>
          <p>{t("All fonts are stored on this website itself. No connection to Google or other font providers is made.", "Alle Schriftarten werden direkt von dieser Website geladen. Es wird keine Verbindung zu Google oder anderen Schriftanbietern hergestellt.")}</p>
        </div>
      </div>

      <div class="legal-sec" id="agb">
        <h2>{t("Terms and conditions (AGB)", "Allgemeine Geschäftsbedingungen (AGB)")}</h2>
        <div class="legal-text">
          <p>{t("General terms and conditions of OCTOS e.U. for deliveries and services to businesses (B2B) and consumers (B2C). As of 21.09.2026. The terms are available in German.",
                "Allgemeine Geschäftsbedingungen der OCTOS e.U. für Lieferungen und Leistungen an Unternehmer (B2B) und Verbraucher (B2C). Stand: 21.09.2026.")}</p>
          <div class="docs">
            <a class="btn btn-ink" href="{R}docs/OCTOS_AGB_2026.pdf" target="_blank" rel="noopener">{t("AGB (PDF, German)", "AGB als PDF")}</a>
            <a class="btn btn-line on-light" href="{R}docs/OCTOS_Ruecktrittsformular.pdf" target="_blank" rel="noopener">{t("Withdrawal form (PDF, German)", "Rücktrittsformular (PDF)")}</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
""" + footer("impressum")

    out = os.path.join(SITE, "de") if de else SITE
    os.makedirs(out, exist_ok=True)
    for name, html in pages.items():
        with open(os.path.join(out, name + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
    return list(pages)


if __name__ == "__main__":
    for lang in ("en", "de"):
        print(lang, build(lang))
