// Charge les produits depuis Supabase et les affiche sur les pages du site.
// Nécessite que le script https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2 soit chargé avant celui-ci.
(function(){
  var SUPABASE_URL = "https://exhlwztwbukaevlmkhta.supabase.co";
  var SUPABASE_ANON_KEY = "sb_publishable_Tk2upQykwis-EE_zgWfHjQ_Lrymxsn5";
  var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  var ICONS = {
    heart: '<path d="M12 20s-7-4.4-9.3-8.8C1.2 8.2 2.7 5 6 5c2 0 3.4 1.1 4 2.3.6-1.2 2-2.3 4-2.3 3.3 0 4.8 3.2 3.3 6.2C19 15.6 12 20 12 20Z"/>',
    book: '<path d="M5 5.5c0-.8.7-1.3 1.5-1.2 2 .3 4 1 5.5 2.2 1.5-1.2 3.5-1.9 5.5-2.2.8-.1 1.5.4 1.5 1.2v13c0 .7-.6 1.2-1.3 1.1-2-.3-4.1-.9-5.7-2.2-1.6 1.3-3.7 1.9-5.7 2.2-.7.1-1.3-.4-1.3-1.1v-13Z"/><path d="M12 6.5V19"/>'
  };
  function icon(name, size){
    size = size || 20;
    return '<svg class="icon" width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+(ICONS[name]||"")+'</svg>';
  }
  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  }

  // Renvoie le prix effectif à payer (prix réduit si une réduction est active).
  function effectivePrice(p){
    return (p.discount_active && p.discount_price != null && p.discount_price < p.price)
      ? Number(p.discount_price) : Number(p.price);
  }

  // Renvoie le HTML d'affichage du prix, avec le prix barré si une réduction est active.
  function priceHtml(p){
    if(p.discount_active && p.discount_price != null && p.discount_price < p.price){
      return '<span class="price"><span style="text-decoration:line-through;color:var(--muted);font-weight:400;margin-right:8px">'+Number(p.price).toFixed(2)+' €</span>'+
        '<span style="color:#b3564a">'+Number(p.discount_price).toFixed(2)+' €</span></span>';
    }
    return '<div class="price">'+Number(p.price).toFixed(2)+' €</div>';
  }

  function productCardHtml(p){
    var media = p.image_url
      ? '<img src="'+esc(p.image_url)+'" alt="'+esc(p.name)+'" loading="lazy">'
      : icon("book", 34);
    var price = effectivePrice(p);
    return '' +
      '<div class="product-card">' +
      '  <div class="product-media">' +
      '    <button class="wishlist-btn" data-wishlist-slug="'+esc(p.slug)+'" data-name="'+esc(p.name)+'" data-price="'+price+'">'+icon("heart",16)+'</button>' +
      '    '+media +
      '  </div>' +
      '  <div class="product-info">' +
      '    <div class="age"><span data-lang-block="fr">'+esc(p.age||"")+'</span><span data-lang-block="en" style="display:none">'+esc(p.age_en||"")+'</span></div>' +
      '    <h3><a href="produit.html?slug='+encodeURIComponent(p.slug)+'"><span data-lang-block="fr">'+esc(p.name)+'</span><span data-lang-block="en" style="display:none">'+esc(p.name_en)+'</span></a></h3>' +
      '    '+priceHtml(p) +
      '    <a href="produit.html?slug='+encodeURIComponent(p.slug)+'" class="btn btn-outline btn-small" style="width:100%" data-i18n="view_product">Voir le produit</a>' +
      '  </div>' +
      '</div>';
  }

  function afterRenderCards(){
    if(window.MPL){
      window.MPL.applyLang();
      window.MPL.initCartButtons();
      window.MPL.initWishlistButtons();
    }
  }

  // Affiche jusqu'à `limit` produits publiés dans le conteneur donné.
  // Si `tag` est fourni, priorise les produits qui ont ce tag (ex: "best-seller"),
  // et complète avec les autres produits publiés si besoin.
  function renderProducts(selector, opts){
    opts = opts || {};
    var container = document.querySelector(selector);
    if(!container) return;
    sb.from("products").select("*").eq("published", true).order("created_at", { ascending: false })
      .then(function(res){
        var data = res.data || [];
        if(res.error){
          container.innerHTML = "<p style='color:#b3564a'>Impossible de charger les produits pour le moment.</p>";
          return;
        }
        if(opts.tag){
          var withTag = data.filter(function(p){ return (p.tags||[]).indexOf(opts.tag) !== -1; });
          var rest = data.filter(function(p){ return (p.tags||[]).indexOf(opts.tag) === -1; });
          data = withTag.concat(rest);
        }
        if(opts.excludeSlug){
          data = data.filter(function(p){ return p.slug !== opts.excludeSlug; });
        }
        if(opts.limit){
          data = data.slice(0, opts.limit);
        }
        if(!data.length){
          container.innerHTML = "<p>Aucun livre disponible pour le moment.</p>";
          return;
        }
        container.innerHTML = data.map(productCardHtml).join("\n");
        afterRenderCards();
        if(typeof opts.onDone === "function") opts.onDone(data);
      });
  }

  // Charge et affiche le détail d'un produit sur produit.html (via ?slug=...)
  function renderProductDetail(){
    var params = new URLSearchParams(window.location.search);
    var slug = params.get("slug");
    var root = document.querySelector("[data-pd-root]");
    if(!root) return;
    if(!slug){
      root.innerHTML = "<p>Produit introuvable.</p>";
      return;
    }
    sb.from("products").select("*").eq("slug", slug).eq("published", true).maybeSingle()
      .then(function(res){
        var p = res.data;
        if(res.error || !p){
          root.innerHTML = "<p>Ce livre n'est plus disponible.</p>";
          return;
        }
        document.title = p.name + " | Mon Premier Livre";
        var media = p.image_url
          ? '<img src="'+esc(p.image_url)+'" alt="'+esc(p.name)+'" loading="lazy">'
          : '<span class="placeholder-tag" style="position:absolute;top:12px;right:12px">Photo à venir</span>'+icon("book",48);
        var price = effectivePrice(p);

        root.innerHTML = '' +
          '<div class="pd-wrap">' +
          '  <div class="pd-media">'+media+'</div>' +
          '  <div class="pd-info">' +
          '    <div class="age"><span data-lang-block="fr">'+esc(p.age||"")+'</span><span data-lang-block="en" style="display:none">'+esc(p.age_en||"")+'</span></div>' +
          '    <h1><span data-lang-block="fr">'+esc(p.name)+'</span><span data-lang-block="en" style="display:none">'+esc(p.name_en)+'</span></h1>' +
          '    '+priceHtml(p) +
          '    <p class="desc" data-lang-block="fr">'+esc(p.short||"")+'</p>' +
          '    <p class="desc" data-lang-block="en" style="display:none">'+esc(p.short_en||"")+'</p>' +
          '    <div class="qty-row"><div class="qty-selector"><button data-qty-minus>−</button><span data-qty-value>1</span><button data-qty-plus>+</button></div></div>' +
          '    <div class="pd-actions">' +
          '      <button class="btn btn-primary btn-block" data-buy-now="'+esc(p.slug)+'" data-name="'+esc(p.name)+'" data-price="'+price+'" data-i18n="buy_now">Acheter maintenant</button>' +
          '      <button class="btn btn-outline btn-block" data-add-cart="'+esc(p.slug)+'" data-name="'+esc(p.name)+'" data-price="'+price+'" data-i18n="add_to_cart">Ajouter au panier</button>' +
          '    </div>' +
          '    <div class="wishlist-line" data-wishlist-slug="'+esc(p.slug)+'" data-name="'+esc(p.name)+'" data-price="'+price+'">'+icon("heart",16)+' <span data-i18n="wishlist">Ajouter à ma liste de souhaits</span></div>' +
          '    <div class="pd-tabs">' +
          '      <div data-lang-block="fr"><h4>Description</h4><div>'+(p.long_desc||"")+'</div><h4>Entretien</h4><p>'+esc(p.care||"")+'</p></div>' +
          '      <div data-lang-block="en" style="display:none"><h4>Description</h4><div>'+(p.long_desc_en||"")+'</div><h4>Care</h4><p>'+esc(p.care_en||"")+'</p></div>' +
          '    </div>' +
          '  </div>' +
          '</div>';

        if(window.MPL){
          window.MPL.applyLang();
          window.MPL.initCartButtons();
          window.MPL.initWishlistButtons();
          window.MPL.initQtySelector();
        }

        renderProducts("[data-pd-others]", { limit: 4, excludeSlug: p.slug });
      });
  }

  window.MPLShop = {
    renderProducts: renderProducts,
    renderProductDetail: renderProductDetail
  };

  // Auto-initialisation : toute grille marquée data-shop-grid se remplit toute seule.
  // Attributs optionnels : data-shop-tag="best-seller" data-shop-limit="4"
  document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll("[data-shop-grid]").forEach(function(el){
      var tag = el.getAttribute("data-shop-tag") || null;
      var limitAttr = el.getAttribute("data-shop-limit");
      var limit = limitAttr ? parseInt(limitAttr, 10) : null;
      var sel = el.id ? "#"+el.id : null;
      if(!sel){
        el.id = "shop-grid-" + Math.random().toString(36).slice(2);
        sel = "#"+el.id;
      }
      renderProducts(sel, { tag: tag, limit: limit });
    });
  });
})();
