// Connecte le bouton "Passer la commande" du panier au paiement Stripe.
// N'agit que si un bouton [data-checkout-btn] est présent sur la page (donc uniquement panier.html).
(function(){
  function getCart(){
    try { return JSON.parse(localStorage.getItem("mpl_cart") || "[]"); }
    catch(e){ return []; }
  }

  document.addEventListener("DOMContentLoaded", function(){
    var btn = document.querySelector("[data-checkout-btn]");
    if(!btn) return;
    var msg = document.getElementById("checkout-msg");

    btn.addEventListener("click", async function(){
      var cart = getCart();
      if(!cart.length){
        if(msg) msg.textContent = "Votre panier est vide.";
        return;
      }
      var originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = "Redirection vers le paiement…";
      if(msg) msg.textContent = "";

      var items = cart.map(function(line){ return { slug: line.slug, qty: line.qty }; });

      try {
        var res = await fetch("/api/create-checkout-session", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ items: items })
        });
        var data = await res.json();
        if(!res.ok || !data.url){
          throw new Error(data.error || "Impossible de démarrer le paiement.");
        }
        window.location.href = data.url;
      } catch(e){
        btn.disabled = false;
        btn.textContent = originalText;
        if(msg) msg.textContent = "Erreur : " + e.message;
      }
    });
  });
})();
