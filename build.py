# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import PRODUCTS, FAQ
from blog_data import build_articles
from reviews_data import build_reviews

ROOT = os.path.dirname(__file__)
ARTICLES = build_articles()
REVIEWS = build_reviews()

ICON_PATHS = {
    "user": '<circle cx="12" cy="8" r="3.4"/><path d="M5 20c0-3.6 3.1-6.2 7-6.2s7 2.6 7 6.2"/>',
    "bag": '<path d="M6 8h12l1 12.5a1 1 0 0 1-1 1.1H6a1 1 0 0 1-1-1.1L6 8Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
    "heart": '<path d="M12 20s-7-4.4-9.3-8.8C1.2 8.2 2.7 5 6 5c2 0 3.4 1.1 4 2.3.6-1.2 2-2.3 4-2.3 3.3 0 4.8 3.2 3.3 6.2C19 15.6 12 20 12 20Z"/>',
    "heart-filled": '<path d="M12 20s-7-4.4-9.3-8.8C1.2 8.2 2.7 5 6 5c2 0 3.4 1.1 4 2.3.6-1.2 2-2.3 4-2.3 3.3 0 4.8 3.2 3.3 6.2C19 15.6 12 20 12 20Z" fill="currentColor" stroke="none"/>',
    "chevron-down": '<path d="M5 8.5 12 15l7-6.5"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "book": '<path d="M5 5.5c0-.8.7-1.3 1.5-1.2 2 .3 4 1 5.5 2.2 1.5-1.2 3.5-1.9 5.5-2.2.8-.1 1.5.4 1.5 1.2v13c0 .7-.6 1.2-1.3 1.1-2-.3-4.1-.9-5.7-2.2-1.6 1.3-3.7 1.9-5.7 2.2-.7.1-1.3-.4-1.3-1.1v-13Z"/><path d="M12 6.5V19"/>',
    "notebook": '<rect x="5" y="4" width="14" height="16" rx="1.5"/><path d="M9 4v16"/><path d="M5 8h4M5 12h4M5 16h4"/>',
    "rotate": '<path d="M4 12a8 8 0 1 1 2.7 6"/><path d="M4 17v-4h4"/>',
    "truck": '<rect x="2.5" y="7" width="11" height="9" rx="1"/><path d="M13.5 10h3.5l3 3v3h-6.5v-6Z"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
    "card": '<rect x="3" y="6" width="18" height="12.5" rx="1.6"/><path d="M3 10.5h18"/><path d="M6.5 14.5h4"/>',
    "message": '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7A2.5 2.5 0 0 1 17.5 16H10l-4.5 4v-4h-.02A2.5 2.5 0 0 1 4 13.5v-7Z"/>',
}

def icon(name, size=20, cls=""):
    path = ICON_PATHS.get(name, "")
    return f'<svg class="icon {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'

def head(title, desc, active, depth=""):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Mon Premier Livre</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" sizes="32x32" href="{depth}assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="{depth}assets/favicon-64.png">
<link rel="apple-touch-icon" sizes="180x180" href="{depth}assets/favicon-180.png">
<link rel="stylesheet" href="{depth}css/style.css">
</head>
<body>
"""

def header(active, depth=""):
    return f"""<header class="site-header">
  <div class="header-inner">
    <div class="nav-cluster">
      <nav class="main-nav main-nav-left">
        <a href="{depth}index.html" data-i18n="nav_home">Accueil</a>
        <a href="{depth}produits.html" data-i18n="nav_shop">Nos livres</a>
      </nav>
      <a href="{depth}index.html" class="logo-link">
        <img src="{depth}assets/logo-full.png" alt="Mon Premier Livre" class="logo-img">
      </a>
      <nav class="main-nav main-nav-right">
        <a href="{depth}faq.html" data-i18n="nav_faq">FAQ</a>
        <a href="{depth}blog.html" data-i18n="nav_blog">Blog</a>
      </nav>
    </div>
    <div class="header-actions">
      <div class="lang-toggle">
        <button data-lang="fr" class="active">FR</button>
        <button data-lang="en">EN</button>
      </div>
      <a href="{depth}compte.html" class="btn btn-ghost btn-small account-btn" title="Mon compte">
        {icon('user', 16)} <span data-i18n="nav_account">Mon compte</span>
      </a>
      <a href="{depth}panier.html" class="icon-link" title="Panier">
        {icon('bag', 21)}
        <span class="badge" data-cart-badge style="display:none">0</span>
      </a>
      <button class="burger">{icon('menu', 22)}</button>
    </div>
  </div>
</header>
"""

def trust_bar():
    return f"""<div class="trust-bar">
  <div class="trust-grid">
    <div class="trust-item">{icon('rotate',26)}<h4 data-i18n="trust1_h">Satisfait ou remboursé</h4><p data-i18n="trust1_p">Pendant 14 jours</p></div>
    <div class="trust-item">{icon('truck',26)}<h4 data-i18n="trust2_h">Livraison suivie offerte</h4><p data-i18n="trust2_p">À partir de 80€ d'achat</p></div>
    <div class="trust-item">{icon('card',26)}<h4 data-i18n="trust3_h">Paiement sécurisé</h4><p data-i18n="trust3_p">Par carte bancaire ou PayPal</p></div>
    <div class="trust-item">{icon('message',26)}<h4 data-i18n="trust4_h">Réponse sous 24h</h4><p data-i18n="trust4_p">Notre équipe à votre écoute</p></div>
  </div>
</div>
"""

def footer(depth=""):
    return f"""{trust_bar()}
<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-col brand">
      <span>Mon Premier Livre</span>
      <p data-i18n="footer_about">La boutique en ligne spécialiste du livre en feutrine pour les tout-petits. Des histoires douces à déchirer, encore et encore.</p>
      <p style="margin-top:14px"><strong data-i18n="footer_contact">Contact</strong> : <a href="mailto:monpremierlivre.com@gmail.com">monpremierlivre.com@gmail.com</a></p>
      <p data-i18n="footer_hours">Du lundi au vendredi, 9h - 18h</p>
      <p style="margin-top:6px" data-i18n="footer_team_location">Équipe basée en France</p>
    </div>
    <div class="footer-col">
      <h5 data-i18n="footer_info">Informations</h5>
      <ul class="footer-links">
        <li><a href="{depth}cgv.html" data-i18n="f_cgv">CGV</a></li>
        <li><a href="{depth}cgu.html" data-i18n="f_cgu">CGU</a></li>
        <li><a href="{depth}mentions-legales.html" data-i18n="f_legal">Mentions légales</a></li>
        <li><a href="{depth}confidentialite.html" data-i18n="f_privacy">Politique de confidentialité</a></li>
        <li><a href="{depth}paiement-securise.html" data-i18n="f_payment">Paiement sécurisé</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h5 data-i18n="footer_help">Besoin d'aide ?</h5>
      <ul class="footer-links">
        <li><a href="{depth}faq.html" data-i18n="f_faq">FAQ</a></li>
        <li><a href="{depth}faq.html#Livraison" data-i18n="f_shipping">Livraison &amp; suivi</a></li>
        <li><a href="{depth}compte.html" data-i18n="f_track">Suivre ma commande</a></li>
        <li><a href="{depth}faq.html#Compte-retours" data-i18n="f_returns">Retours et remboursement</a></li>
        <li><a href="mailto:monpremierlivre.com@gmail.com" data-i18n="f_contact_form">Formulaire de contact</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">© 2026 Mon Premier Livre — <span data-i18n="rights">Tous droits réservés.</span></div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="{depth}js/app.js"></script>
<script src="{depth}js/shop.js"></script>
<script src="{depth}js/checkout.js"></script>
</body>
</html>"""

def product_card(p, depth=""):
    media = f'<img src="{depth}{p["image"]}" alt="{p["name"]}" loading="lazy">' if p.get("image") else icon('book',34)
    return f"""<div class="product-card">
  <div class="product-media">
    <button class="wishlist-btn" data-wishlist-slug="{p['slug']}" data-name="{p['name']}" data-price="{p['price']}">{icon('heart',16)}</button>
    {media}
  </div>
  <div class="product-info">
    <div class="age"><span data-lang-block="fr">{p['age']}</span><span data-lang-block="en" style="display:none">{p['age_en']}</span></div>
    <h3><a href="{depth}produits/{p['slug']}.html"><span data-lang-block="fr">{p['name']}</span><span data-lang-block="en" style="display:none">{p['name_en']}</span></a></h3>
    <div class="price">{p['price']:.2f} €</div>
    <a href="{depth}produits/{p['slug']}.html" class="btn btn-outline btn-small" style="width:100%" data-i18n="view_product">Voir le produit</a>
  </div>
</div>"""

def build_index():
    reviews_html = ""
    for r in (REVIEWS + REVIEWS[:20]):
        stars = "★" * r["rating"] + "☆" * (5 - r["rating"])
        if r.get("lang") == "en":
            quote = f"“{r['comment']}”"
            time_text = f"— {r['weeks']} weeks ago"
        else:
            quote = f"« {r['comment']} »"
            time_text = f"— il y a {r['weeks']} semaines"
        reviews_html += f"""<div class="review-card">
      <div class="stars">{stars}</div>
      <p>{quote}</p>
      <div class="meta"><strong>{r['name']}</strong> <span>{time_text}</span></div>
    </div>\n"""

    html = head("Livres en feutrine à déchirer pour bébé", "Mon Premier Livre : des livres en feutrine sensoriels et increvables, pensés pour éveiller le goût de lire dès les premiers mois.", "home")
    html += header("home")
    html += f"""
<section class="hero" style="padding:0">
  <div class="hero-media">
    <div class="hero-text">
      <h1 data-i18n="hero_title"><span class="nowrap-line">Des livres en feutrine à déchirer,</span><br><span class="nowrap-line">pour éveiller le goût de lire</span></h1>
      <p data-i18n="hero_sub">Des histoires douces, sensorielles et increvables, pensées pour les tout-petits.</p>
      <a href="produits.html" class="btn btn-primary" data-i18n="hero_cta">Découvrir la collection</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <h2 data-i18n="bestsellers">Nos best-sellers</h2>
      <p data-i18n="bestsellers_sub">Les livres préférés des familles</p>
    </div>
    <div class="product-grid" data-shop-grid data-shop-tag="best-seller" data-shop-limit="4"></div>
    <div style="text-align:center;margin-top:36px">
      <a href="produits.html" class="btn btn-outline" data-i18n="view_all">Voir tous nos livres</a>
    </div>
  </div>
</section>

<section style="background:var(--cream-2)">
  <div class="container founder">
    <div class="founder-media">
      <img src="assets/founder.jpg" alt="Camille, fondatrice de Mon Premier Livre, avec son fils">
    </div>
    <div class="founder-text">
      <div data-lang-block="fr">
        <h2>Notre histoire</h2>
        <p>Je m'appelle Camille, je suis maman d'un petit garçon et professionnelle de l'éducation depuis plus de 10 ans. J'ai accompagné plusieurs centaines d'enfants dans leurs premiers apprentissages, et j'ai toujours été convaincue d'une chose : le goût de la lecture se construit dès les tout premiers mois, bien avant de savoir lire.</p>
        <p>En cherchant des livres pour mon propre fils, j'ai réalisé qu'il manquait, sur le marché, des livres pensés pour être vraiment manipulés : déchirés, mordillés, lavés, recommencés. C'est de ce constat qu'est née Mon Premier Livre : des livres en feutrine doux, résistants et sensoriels, conçus pour accompagner les tout-petits vers le plaisir de lire, une page à la fois.</p>
        <p class="signature">— Camille, fondatrice de Mon Premier Livre</p>
      </div>
      <div data-lang-block="en" style="display:none">
        <h2>Our story</h2>
        <p>My name is Camille, I'm mum to a little boy and I've worked in education for over 10 years. I've supported several hundred children in their earliest learning, and I've always been convinced of one thing: a love of reading is built from the very first months, long before a child can actually read.</p>
        <p>While looking for books for my own son, I realised the market was missing books designed to be truly handled: torn, chewed, washed, started over. That's how Mon Premier Livre was born: soft, sturdy, sensory felt books, designed to guide little ones toward the pleasure of reading, one page at a time.</p>
        <p class="signature">— Camille, founder of Mon Premier Livre</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <h2>Elles nous font confiance</h2>
      <p>Plus de 100 familles partagent leur expérience</p>
    </div>
  </div>
  <div class="reviews-wrap">
    <div class="reviews-track">
      {reviews_html}
    </div>
  </div>
</section>
"""
    html += footer()
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def build_produits():
    html = head("Nos livres en feutrine", "Découvrez tous nos livres en feutrine à déchirer pour bébé et jeune enfant.", "shop")
    html += header("shop")
    html += f"""
<section class="page-hero">
  <div class="container">
    <h1 data-i18n="shop_title">Nos livres en feutrine</h1>
    <p data-i18n="shop_sub">Des histoires douces à déchirer et recoller, à partir de 6 mois.</p>
  </div>
</section>
<section style="padding-top:20px">
  <div class="container">
    <div class="product-grid" data-shop-grid></div>
  </div>
</section>
"""
    html += footer()
    with open(os.path.join(ROOT, "produits.html"), "w", encoding="utf-8") as f:
        f.write(html)

def build_produit_pages():
    for p in PRODUCTS:
        others = [x for x in PRODUCTS if x["slug"] != p["slug"]][:4]
        cards = "\n".join(product_card(x, depth="../") for x in others)
        html = head(p["name"], p["short"], "shop", depth="../")
        html += header("shop", depth="../")
        if p.get("image"):
            pd_media_content = f'<img src="../{p["image"]}" alt="{p["name"]}" loading="lazy">'
        else:
            pd_media_content = f'<span class="placeholder-tag" style="position:absolute;top:12px;right:12px">Photo à venir</span>{icon("book",48)}'
        html += f"""
<section style="padding-top:40px">
  <div class="container">
    <div class="pd-wrap">
      <div class="pd-media">
        {pd_media_content}
      </div>
      <div class="pd-info">
        <div class="age"><span data-lang-block="fr">{p['age']}</span><span data-lang-block="en" style="display:none">{p['age_en']}</span></div>
        <h1><span data-lang-block="fr">{p['name']}</span><span data-lang-block="en" style="display:none">{p['name_en']}</span></h1>
        <div class="price">{p['price']:.2f} €</div>
        <p class="desc" data-lang-block="fr">{p['short']}</p>
        <p class="desc" data-lang-block="en" style="display:none">{p['short_en']}</p>
        <div class="qty-row">
          <div class="qty-selector">
            <button data-qty-minus>−</button>
            <span data-qty-value>1</span>
            <button data-qty-plus>+</button>
          </div>
        </div>
        <div class="pd-actions">
          <button class="btn btn-primary btn-block" data-buy-now="{p['slug']}" data-name="{p['name']}" data-price="{p['price']}" data-i18n="buy_now">Acheter maintenant</button>
          <button class="btn btn-outline btn-block" data-add-cart="{p['slug']}" data-name="{p['name']}" data-price="{p['price']}" data-i18n="add_to_cart">Ajouter au panier</button>
        </div>
        <div class="wishlist-line" data-wishlist-slug="{p['slug']}" data-name="{p['name']}" data-price="{p['price']}">
          {icon('heart',16)} <span data-i18n="wishlist">Ajouter à ma liste de souhaits</span>
        </div>
        <div class="pd-tabs">
          <div data-lang-block="fr">
            <h4>Description</h4>
            <p>{p['long']}</p>
            <h4>Entretien</h4>
            <p>{p['care']}</p>
          </div>
          <div data-lang-block="en" style="display:none">
            <h4>Description</h4>
            <p>{p['long_en']}</p>
            <h4>Care</h4>
            <p>{p['care_en']}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head"><h2 data-i18n="also_like">Vous aimerez aussi</h2></div>
    <div class="product-grid">
      {cards}
    </div>
  </div>
</section>
"""
        html += footer(depth="../")
        with open(os.path.join(ROOT, "produits", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)

CATEGORY_EN = {
    "Commande": "Ordering",
    "Livraison": "Shipping",
    "Paiement": "Payment",
    "Produit & entretien": "Product & care",
    "Compte & retours": "Account & returns",
}

def build_faq():
    html = head("FAQ", "Toutes les réponses à vos questions sur la commande, la livraison, le paiement et nos livres en feutrine.", "faq")
    html += header("faq")
    html += """
<section class="page-hero">
  <div class="container">
    <h1 data-i18n="faq_title">Questions fréquentes</h1>
    <p data-i18n="faq_sub">Tout ce que vous devez savoir avant, pendant et après votre commande.</p>
  </div>
</section>
<section style="padding-top:10px">
  <div class="container">
    <div class="faq-layout">
      <nav class="faq-sidebar">
        <ul>
"""
    anchors = []
    for cat in FAQ:
        anchor = cat.replace(" & ", "-").replace(" ", "-")
        cat_en = CATEGORY_EN.get(cat, cat)
        anchors.append(anchor)
        html += f'<li><a href="#{anchor}" data-faq-nav="{anchor}"><span data-lang-block="fr">{cat}</span><span data-lang-block="en" style="display:none">{cat_en}</span></a></li>\n'
    html += """
        </ul>
      </nav>
      <div class="faq-content">
"""
    for cat, items in FAQ.items():
        anchor = cat.replace(" & ", "-").replace(" ", "-")
        cat_en = CATEGORY_EN.get(cat, cat)
        html += f'<div class="faq-cat" id="{anchor}"><h2><span data-lang-block="fr">{cat}</span><span data-lang-block="en" style="display:none">{cat_en}</span></h2>'
        for q, a, q_en, a_en in items:
            html += f"""<div class="faq-item">
        <div class="faq-q">
          <span data-lang-block="fr">{q}</span><span data-lang-block="en" style="display:none">{q_en}</span>
          {icon('chevron-down',16)}
        </div>
        <div class="faq-a">
          <p data-lang-block="fr">{a}</p>
          <p data-lang-block="en" style="display:none">{a_en}</p>
        </div>
      </div>"""
        html += "</div>"
    html += """
      </div>
    </div>
  </div>
</section>
"""
    html += footer()
    with open(os.path.join(ROOT, "faq.html"), "w", encoding="utf-8") as f:
        f.write(html)

BLOG_CATEGORIES = [
    ("all", "Tous les articles", "All articles"),
    ("focus-habitudes", "Concentration & habitudes de lecture", "Focus & reading habits"),
    ("securite-produit", "Sécurité & durabilité", "Safety & durability"),
    ("lien-affectif", "Lien affectif & rituels", "Bonding & rituals"),
    ("etat-esprit-parental", "État d'esprit parental", "Parenting mindset"),
]

def build_blog_list():
    per_page = 400  # keep every article on a single page so the sidebar category
    # filter (client-side) can operate across the full set, not just one page's chunk
    total_pages = (len(ARTICLES) + per_page - 1) // per_page
    for page in range(1, max(total_pages, 1) + 1):
        chunk = ARTICLES[(page-1)*per_page : page*per_page]
        cards = ""
        for a in chunk:
            cat = a.get("category", "all")
            cards += f"""<div class="blog-card" data-category="{cat}">
        <div class="body">
          <span class="tag" data-lang-block="fr">{a['display_tag_fr']}</span>
          <span class="tag" data-lang-block="en" style="display:none">{a['display_tag_en']}</span>
          <h3>
            <a href="blog/{a['slug']}.html" data-lang-block="fr">{a['title_fr']}</a>
            <a href="blog/{a['slug']}.html" data-lang-block="en" style="display:none">{a['title_en']}</a>
          </h3>
          <p data-lang-block="fr">{a['excerpt_fr']}</p>
          <p data-lang-block="en" style="display:none">{a['excerpt_en']}</p>
          <a class="read" href="blog/{a['slug']}.html" data-lang-block="fr">Lire l'article →</a>
          <a class="read" href="blog/{a['slug']}.html" data-lang-block="en" style="display:none">Read the article →</a>
        </div>
      </div>\n"""
        if total_pages > 1:
            pagi = '<div class="pagination">'
            for pnum in range(1, total_pages+1):
                fname = "blog.html" if pnum == 1 else f"blog-{pnum}.html"
                cls = "active" if pnum == page else ""
                pagi += f'<a href="{fname}" class="{cls}">{pnum}</a>'
            pagi += "</div>"
        else:
            pagi = ""

        sidebar = '<nav class="blog-sidebar"><ul>\n'
        for i, (slug, name_fr, name_en) in enumerate(BLOG_CATEGORIES):
            active = "active" if i == 0 else ""
            sidebar += f'<li><a href="#" class="{active}" data-blog-filter="{slug}"><span data-lang-block="fr">{name_fr}</span><span data-lang-block="en" style="display:none">{name_en}</span></a></li>\n'
        sidebar += '</ul></nav>'

        html = head("Blog", "Conseils de lecture, développement de l'enfant et sélection de livres en feutrine par âge.", "blog")
        html += header("blog")
        html += f"""
<section class="page-hero">
  <div class="container">
    <h1 data-i18n="blog_title">Le blog Mon Premier Livre</h1>
    <p data-i18n="blog_sub">Conseils de lecture, développement de l'enfant, et sélection de livres par âge.</p>
  </div>
</section>
<section style="padding-top:10px">
  <div class="container">
    <div class="blog-layout">
      {sidebar}
      <div class="blog-content">
        <div class="blog-grid" data-blog-grid>
          {cards}
        </div>
        {'' if ARTICLES else '<div class="empty-state"><p data-i18n="blog_empty">De nouveaux articles arrivent très bientôt.</p></div>'}
        {pagi}
      </div>
    </div>
  </div>
</section>
"""
        html += footer()
        fname = "blog.html" if page == 1 else f"blog-{page}.html"
        with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
            f.write(html)

def build_blog_articles():
    for a in ARTICLES:
        html = head(a["title_fr"], a["excerpt_fr"], "blog", depth="../")
        html += header("blog", depth="../")
        html += f"""
<section style="padding-top:44px">
  <div class="container article-body">
    <div class="article-meta">
      <span data-lang-block="fr">{a['age_band_fr']} · Mon Premier Livre</span>
      <span data-lang-block="en" style="display:none">{a['age_band_en']} · Mon Premier Livre</span>
    </div>
    <h1 class="article-title" data-lang-block="fr">{a['title_fr']}</h1>
    <h1 class="article-title" data-lang-block="en" style="display:none">{a['title_en']}</h1>
    <div data-lang-block="fr">{a['body_html_fr']}</div>
    <div data-lang-block="en" style="display:none">{a['body_html_en']}</div>
    <div style="text-align:center;margin-top:40px">
      <a href="../produits.html" class="btn btn-primary" data-i18n="hero_cta">Découvrir nos livres en feutrine</a>
    </div>
  </div>
</section>
"""
        html += footer(depth="../")
        with open(os.path.join(ROOT, "blog", a["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)

def build_compte():
    html = head("Mon compte", "Connectez-vous ou créez votre compte Mon Premier Livre pour profiter de 10% sur votre première commande.", "account")
    html += header("account")
    html += """
<section class="page-hero">
  <div class="container">
    <h1 data-i18n="account_title">Mon compte</h1>
  </div>
</section>
<section style="padding-top:10px">
  <div class="container">
    <div class="auth-wrap">
      <div class="auth-tabs">
        <button class="active" data-tab="login" data-i18n="tab_login">Connexion</button>
        <button data-tab="signup" data-i18n="tab_signup">Créer un compte</button>
      </div>
      <div class="auth-panel" data-panel="login">
        <div class="field"><label data-i18n="field_email">E-mail</label><input type="email" placeholder="vous@exemple.fr"></div>
        <div class="field"><label data-i18n="field_password">Mot de passe</label><input type="password" placeholder="••••••••"></div>
        <button class="btn btn-primary btn-block" data-i18n="login_btn">Se connecter</button>
      </div>
      <div class="auth-panel" data-panel="signup" style="display:none">
        <div class="discount-note" data-i18n="signup_discount_note">-10% sur votre première commande dès la création de votre compte.</div>
        <div class="field"><label data-i18n="field_firstname">Prénom</label><input type="text" placeholder="Votre prénom"></div>
        <div class="field"><label data-i18n="field_email">E-mail</label><input type="email" placeholder="vous@exemple.fr"></div>
        <div class="field"><label data-i18n="field_password">Mot de passe</label><input type="password" placeholder="8 caractères minimum"></div>
        <div class="checkbox-row">
          <input type="checkbox" id="newsletter-opt" checked>
          <label for="newsletter-opt" data-i18n="newsletter_opt">J'accepte de recevoir les actualités de Mon Premier Livre (nouveautés, articles de blog, offres).</label>
        </div>
        <button class="btn btn-primary btn-block" data-i18n="signup_btn">Créer mon compte</button>
      </div>
    </div>
    <p style="text-align:center;color:var(--muted);font-size:13px;margin-top:20px" data-i18n="demo_disclaimer">Ceci est une interface de démonstration. La création réelle de compte nécessite une base de données et un service d'authentification à connecter (voir README).</p>
  </div>
</section>
"""
    html += footer()
    with open(os.path.join(ROOT, "compte.html"), "w", encoding="utf-8") as f:
        f.write(html)

def build_panier():
    html = head("Panier", "Votre panier Mon Premier Livre.", "cart")
    html += header("cart")
    html += """
<section class="page-hero">
  <div class="container"><h1 data-i18n="cart_title">Mon panier</h1></div>
</section>
<section style="padding-top:10px">
  <div class="container" style="max-width:760px">
    <div data-cart-list></div>
    <div class="cart-summary" data-cart-summary>
      <div class="row"><span data-i18n="cart_subtotal">Sous-total</span><span data-sum-subtotal>0,00 €</span></div>
      <div class="row"><span data-i18n="cart_shipping">Livraison</span><span data-sum-shipping>—</span></div>
      <div class="row total"><span data-i18n="cart_total">Total</span><span data-sum-total>0,00 €</span></div>
      <p style="font-size:12.5px;color:var(--muted);margin:10px 0 16px" data-i18n="cart_shipping_note">Livraison offerte dès 80€ d'achat.</p>
      <button class="btn btn-primary btn-block" data-checkout-btn data-i18n="cart_checkout">Passer la commande</button>
      <p id="checkout-msg" style="font-size:13px;color:#b3564a;margin-top:10px"></p>
    </div>
  </div>
</section>
"""
    html += footer()
    with open(os.path.join(ROOT, "panier.html"), "w", encoding="utf-8") as f:
        f.write(html)

def build_success():
    html = head("Commande confirmée", "Merci pour votre commande Mon Premier Livre.", "cart")
    html += header("cart")
    html += """
<section class="page-hero">
  <div class="container" style="text-align:center;max-width:560px">
    <h1 data-i18n="success_title">Merci pour votre commande !</h1>
    <p data-i18n="success_sub">Votre paiement a bien été reçu. Un e-mail de confirmation va vous être envoyé sous peu.</p>
    <a href="produits.html" class="btn btn-primary" style="margin-top:20px" data-i18n="success_cta">Continuer mes achats</a>
  </div>
</section>
<script>
  // La commande est confirmée : on vide le panier local.
  localStorage.removeItem("mpl_cart");
</script>
"""
    html += footer()
    with open(os.path.join(ROOT, "success.html"), "w", encoding="utf-8") as f:
        f.write(html)

def legal_page(slug, title, desc, body_html):
    html = head(title, desc, "", "")
    html += header("")
    html += f"""
<section class="page-hero">
  <div class="container" style="max-width:760px">
    <h1>{title}</h1>
  </div>
</section>
<section style="padding-top:10px;padding-bottom:40px">
  <div class="container">
    <div class="article-body legal-body">
{body_html}
    </div>
  </div>
</section>
"""
    html += footer()
    with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_legal_pages():
    # Informations d'identification de l'éditeur (à tenir à jour) :
    #   - Statut : entreprise individuelle, régime micro-entreprise
    #   - Responsable de publication : Camille
    #   - Ville de rattachement : Strasbourg (adresse complète volontairement non publiée)
    #   - SIRET : en cours d'attribution (immatriculation micro-entreprise en cours) —
    #     À AJOUTER ICI dès réception : remplacer la ligne SIRET ci-dessous dans mentions-legales.
    #   - Contact : monpremierlivre.com@gmail.com uniquement (pas de téléphone publié)

    legal_page("mentions-legales", "Mentions légales",
        "Mentions légales du site Mon Premier Livre : éditeur, hébergement, propriété intellectuelle.",
        """
      <!-- TODO : ajouter la ligne "Numéro SIRET : ..." ci-dessous dès réception du numéro définitif. -->
      <h2>Éditeur du site</h2>
      <p>Le site monpremierlivre.com (ci-après « le Site ») est édité par Camille, entrepreneur individuel exerçant sous le régime de la micro-entreprise, domicilié à Strasbourg, France.</p>
      <p>TVA non applicable, article 293 B du Code général des impôts.</p>
      <p>Directeur de la publication : Camille.</p>
      <p>Contact : <a href="mailto:monpremierlivre.com@gmail.com">monpremierlivre.com@gmail.com</a></p>

      <h2>Hébergement</h2>
      <p>Le Site est hébergé par Netlify, Inc., 101 2nd Street, San Francisco, CA 94105, États-Unis — <a href="https://www.netlify.com" target="_blank" rel="noopener">www.netlify.com</a>.</p>

      <h2>Propriété intellectuelle</h2>
      <p>L'ensemble des éléments du Site (textes, illustrations, photographies, logo, mise en page, charte graphique) est protégé par le droit d'auteur et reste la propriété exclusive de l'éditeur, sauf mention contraire. Toute reproduction, représentation ou exploitation, totale ou partielle, sans autorisation préalable écrite, est interdite et pourrait constituer une contrefaçon au sens des articles L.335-2 et suivants du Code de la propriété intellectuelle.</p>

      <h2>Données personnelles</h2>
      <p>Le traitement des données personnelles collectées via le Site est décrit en détail dans notre <a href="confidentialite.html">Politique de confidentialité</a>.</p>

      <h2>Droit applicable</h2>
      <p>Les présentes mentions légales sont soumises au droit français. En cas de litige, les juridictions françaises seront seules compétentes, sous réserve des règles impératives applicables aux consommateurs.</p>
""")

    legal_page("cgv", "Conditions générales de vente",
        "Conditions générales de vente du site Mon Premier Livre : commande, paiement, livraison, retours et garanties.",
        """
      <p>Les présentes conditions générales de vente (CGV) régissent les ventes de produits réalisées sur le site monpremierlivre.com, édité par Camille, entrepreneur individuel (micro-entreprise), Strasbourg, France. Toute commande passée sur le Site implique l'acceptation pleine et entière des présentes CGV.</p>

      <h2>1. Produits</h2>
      <p>Le Site propose à la vente des livres en feutrine à déchirer, conçus pour les enfants de 0 à 3 ans. Les caractéristiques essentielles de chaque produit (dimensions, matière, âge conseillé) sont présentées sur sa fiche descriptive.</p>

      <h2>2. Prix</h2>
      <p>Les prix sont indiqués en euros. La micro-entreprise bénéficiant de la franchise en base de TVA (article 293 B du CGI), les prix affichés ne comportent pas de TVA. Les frais de livraison sont précisés avant la validation définitive de la commande.</p>

      <h2>3. Commande</h2>
      <p>Le client sélectionne les produits de son choix, les ajoute à son panier, puis valide sa commande en renseignant ses coordonnées et en procédant au paiement. Un e-mail de confirmation récapitulant la commande est envoyé automatiquement après validation du paiement.</p>

      <h2>4. Paiement</h2>
      <p>Le paiement s'effectue en ligne, par carte bancaire, via la plateforme sécurisée Stripe. Les informations relatives au moyen de paiement ne sont jamais stockées par le Site ; elles sont traitées exclusivement par Stripe, prestataire certifié PCI-DSS. Voir notre page <a href="paiement-securise.html">Paiement sécurisé</a> pour plus de détails.</p>

      <h2>5. Livraison</h2>
      <p>Les commandes sont préparées avec soin, avec un contrôle qualité systématique avant expédition, dans un délai généralement compris entre 48 et 72 heures. Un numéro de suivi est communiqué par e-mail dès l'expédition. La livraison est offerte à partir de 80 € d'achat ; en dessous de ce montant, des frais de port sont appliqués et affichés avant validation du paiement. Le Site livre dans le monde entier.</p>

      <h2>6. Droit de rétractation</h2>
      <p>Conformément aux articles L.221-18 et suivants du Code de la consommation, le client dispose d'un délai de 14 jours à compter de la réception de sa commande pour exercer son droit de rétractation, sans avoir à justifier de motif ni à payer de pénalité. Pour exercer ce droit, il suffit d'en informer l'éditeur par e-mail à <a href="mailto:monpremierlivre.com@gmail.com">monpremierlivre.com@gmail.com</a>, en indiquant le numéro de commande.</p>

      <h2>7. Retours et remboursements</h2>
      <p>Les produits doivent être retournés dans leur état d'origine. Le remboursement est effectué dans un délai maximal de 14 jours à compter de la réception du produit retourné, par le même moyen de paiement que celui utilisé lors de la commande, sauf accord contraire. En cas de colis perdu ou endommagé pendant le transport, le client est invité à contacter l'éditeur avec son numéro de commande afin qu'une enquête soit ouverte auprès du transporteur.</p>

      <h2>8. Garanties légales</h2>
      <p>Tous les produits vendus sur le Site bénéficient de la garantie légale de conformité (articles L.217-3 et suivants du Code de la consommation) et de la garantie contre les vices cachés (articles 1641 et suivants du Code civil), sans supplément de prix.</p>

      <h2>9. Responsabilité</h2>
      <p>L'éditeur ne saurait être tenu responsable de l'inexécution du contrat en cas de force majeure, de rupture de stock, de perturbation ou grève totale ou partielle notamment des services postaux et moyens de transport.</p>

      <h2>10. Médiation de la consommation</h2>
      <p>Conformément aux articles L.616-1 et R.616-1 du Code de la consommation, en cas de litige non résolu directement avec l'éditeur, le client peut recourir gratuitement à un médiateur de la consommation. Le client peut également utiliser la plateforme européenne de règlement en ligne des litiges, accessible à l'adresse <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">ec.europa.eu/consumers/odr</a>.</p>

      <h2>11. Droit applicable</h2>
      <p>Les présentes CGV sont soumises au droit français. Tout litige relève, à défaut de résolution amiable, des juridictions françaises compétentes, sous réserve des dispositions impératives applicables aux consommateurs.</p>
""")

    legal_page("cgu", "Conditions générales d'utilisation",
        "Conditions générales d'utilisation du site Mon Premier Livre.",
        """
      <p>Les présentes conditions générales d'utilisation (CGU) régissent l'accès et l'utilisation du site monpremierlivre.com (ci-après « le Site »). En naviguant sur le Site, l'utilisateur reconnaît avoir pris connaissance des présentes CGU et les accepter sans réserve.</p>

      <h2>1. Objet</h2>
      <p>Le Site permet la présentation et la vente en ligne de livres en feutrine pour enfants, ainsi que la consultation d'un blog dédié à l'éveil et à la lecture des tout-petits.</p>

      <h2>2. Accès au site</h2>
      <p>Le Site est accessible gratuitement depuis n'importe quel appareil disposant d'un accès à internet. L'éditeur met tout en œuvre pour assurer un accès continu au Site, sans garantie de résultat, notamment en cas de maintenance, de panne ou de force majeure.</p>

      <h2>3. Compte client</h2>
      <p>La création d'un compte client est facultative pour naviguer sur le Site, mais nécessaire pour suivre l'historique de ses commandes et gérer ses informations personnelles. L'utilisateur s'engage à fournir des informations exactes et à préserver la confidentialité de son mot de passe. Il peut à tout moment demander la suppression de son compte en écrivant à <a href="mailto:monpremierlivre.com@gmail.com">monpremierlivre.com@gmail.com</a>.</p>

      <h2>4. Propriété intellectuelle</h2>
      <p>L'ensemble des contenus du Site (textes, images, illustrations, articles de blog, charte graphique) est protégé par le droit de la propriété intellectuelle. Toute reproduction ou utilisation non autorisée est interdite.</p>

      <h2>5. Comportement de l'utilisateur</h2>
      <p>L'utilisateur s'engage à utiliser le Site conformément à sa destination et à ne pas porter atteinte à son bon fonctionnement, notamment en tentant d'accéder de manière frauduleuse à des données non destinées à être publiques.</p>

      <h2>6. Liens hypertextes</h2>
      <p>Le Site peut contenir des liens vers des sites tiers. L'éditeur n'exerce aucun contrôle sur ces sites et décline toute responsabilité quant à leur contenu.</p>

      <h2>7. Limitation de responsabilité</h2>
      <p>L'éditeur ne saurait être tenu responsable des dommages directs ou indirects résultant de l'utilisation du Site ou de l'impossibilité d'y accéder.</p>

      <h2>8. Modification des CGU</h2>
      <p>L'éditeur se réserve le droit de modifier les présentes CGU à tout moment. La version applicable est celle en vigueur au moment de la consultation du Site.</p>

      <h2>9. Droit applicable</h2>
      <p>Les présentes CGU sont soumises au droit français.</p>
""")

    legal_page("confidentialite", "Politique de confidentialité",
        "Politique de confidentialité et de protection des données personnelles du site Mon Premier Livre (RGPD).",
        """
      <p>La présente politique de confidentialité décrit comment le site monpremierlivre.com (ci-après « le Site ») collecte, utilise et protège les données personnelles de ses utilisateurs, conformément au Règlement général sur la protection des données (RGPD) et à la loi Informatique et Libertés.</p>

      <h2>1. Responsable du traitement</h2>
      <p>Le responsable du traitement des données est Camille, entrepreneur individuel (micro-entreprise), Strasbourg, France. Contact : <a href="mailto:monpremierlivre.com@gmail.com">monpremierlivre.com@gmail.com</a>.</p>

      <h2>2. Données collectées</h2>
      <p>Selon l'usage du Site, les données suivantes peuvent être collectées : nom et prénom, adresse e-mail, mot de passe (chiffré), adresse de livraison, historique de commandes, et préférence d'abonnement à la newsletter. Le contenu du panier et de la liste de souhaits est stocké localement dans le navigateur (localStorage) et n'est transmis à nos serveurs qu'au moment de la commande.</p>

      <h2>3. Finalités et bases légales</h2>
      <ul>
        <li><strong>Gestion des commandes et du compte client</strong> — exécution du contrat de vente.</li>
        <li><strong>Envoi d'e-mails transactionnels</strong> (confirmation de commande, suivi de livraison, réinitialisation de mot de passe) — exécution du contrat.</li>
        <li><strong>Envoi de la newsletter</strong> (nouveautés, articles de blog) — consentement explicite donné à l'inscription, retirable à tout moment via le lien de désabonnement présent dans chaque e-mail.</li>
        <li><strong>Amélioration du Site</strong> — intérêt légitime de l'éditeur.</li>
      </ul>

      <h2>4. Destinataires des données</h2>
      <p>Les données sont traitées par l'éditeur et par les prestataires techniques suivants, agissant en tant que sous-traitants :</p>
      <ul>
        <li><strong>Supabase</strong> — hébergement de la base de données et gestion des comptes clients.</li>
        <li><strong>Stripe</strong> — traitement sécurisé des paiements en ligne. Le Site ne stocke jamais les données bancaires.</li>
        <li><strong>Brevo</strong> — envoi des e-mails transactionnels et de la newsletter.</li>
        <li><strong>Netlify</strong> — hébergement technique du Site.</li>
      </ul>
      <p>Ces prestataires n'utilisent les données que dans la limite nécessaire à l'exécution de leur prestation et ne les revendent à aucun tiers.</p>

      <h2>5. Transferts hors Union européenne</h2>
      <p>Certains de ces prestataires (notamment Stripe et Netlify) peuvent être amenés à traiter des données en dehors de l'Union européenne, en particulier aux États-Unis. Ces transferts sont encadrés par des garanties appropriées (clauses contractuelles types de la Commission européenne ou mécanismes équivalents mis en place par chaque prestataire).</p>

      <h2>6. Durée de conservation</h2>
      <p>Les données liées à un compte client sont conservées tant que le compte est actif. Les données relatives aux commandes sont conservées pendant la durée nécessaire au respect des obligations légales et comptables. En cas d'inscription à la newsletter sans compte associé, les données sont conservées jusqu'au désabonnement.</p>

      <h2>7. Cookies et technologies similaires</h2>
      <p>Le Site utilise le stockage local du navigateur (localStorage) à des fins strictement techniques : mémoriser le contenu du panier, la liste de souhaits et la langue choisie. Ces éléments ne sont pas des cookies de suivi publicitaire et ne sont partagés avec aucun tiers à des fins commerciales.</p>

      <h2>8. Vos droits</h2>
      <p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité de vos données, ainsi que du droit de retirer votre consentement à tout moment lorsque le traitement en dépend. Pour exercer ces droits, contactez-nous à <a href="mailto:monpremierlivre.com@gmail.com">monpremierlivre.com@gmail.com</a>. Vous disposez également du droit d'introduire une réclamation auprès de la Commission nationale de l'informatique et des libertés (CNIL) — <a href="https://www.cnil.fr" target="_blank" rel="noopener">www.cnil.fr</a>.</p>

      <h2>9. Sécurité</h2>
      <p>Des mesures techniques et organisationnelles raisonnables sont mises en œuvre pour protéger vos données contre tout accès non autorisé, perte ou divulgation, notamment via le chiffrement des mots de passe et le recours à des prestataires certifiés pour le traitement des paiements.</p>
""")

    legal_page("paiement-securise", "Paiement sécurisé",
        "Comment vos paiements sont sécurisés sur le site Mon Premier Livre, via Stripe.",
        """
      <h2>Un paiement 100 % sécurisé</h2>
      <p>Tous les paiements effectués sur le Site sont traités par Stripe, l'un des principaux prestataires de paiement en ligne au monde, certifié au plus haut niveau de sécurité de l'industrie bancaire (PCI-DSS niveau 1).</p>

      <h2>Moyens de paiement acceptés</h2>
      <p>Le paiement par carte bancaire (Visa, Mastercard) est accepté sur le Site.</p>

      <h2>Vos données bancaires ne transitent jamais par nos serveurs</h2>
      <p>Au moment du paiement, vous êtes redirigé vers l'environnement sécurisé de Stripe. Vos informations bancaires sont saisies et traitées directement par Stripe : elles ne sont à aucun moment transmises, visibles ou stockées par le Site. Cette architecture réduit au minimum les risques liés au traitement de données bancaires.</p>

      <h2>Authentification renforcée</h2>
      <p>Selon votre banque et le montant de la transaction, une authentification supplémentaire (3D Secure) peut vous être demandée directement par votre banque, afin de confirmer que vous êtes bien à l'origine du paiement.</p>

      <h2>Confidentialité</h2>
      <p>Pour en savoir plus sur la manière dont vos données sont traitées, consultez notre <a href="confidentialite.html">Politique de confidentialité</a>.</p>
""")


if __name__ == "__main__":
    build_index()
    build_produits()
    # build_produit_pages()  # remplacé par produit.html (rendu dynamique via Supabase, cf. js/shop.js)
    build_faq()
    build_blog_list()
    build_blog_articles()
    # build_compte()  # compte.html est maintenant maintenu à la main (vraie auth Supabase, voir git history)
    build_panier()
    build_success()
    build_legal_pages()
    print("OK -", len(PRODUCTS), "produits,", len(ARTICLES), "articles,", len(REVIEWS), "avis")
