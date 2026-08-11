// Netlify Function — crée une session de paiement Stripe Checkout.
// Le prix de chaque article est relu depuis Supabase (jamais fait confiance au prix envoyé par le
// navigateur), pour empêcher qu'un client modifie le prix affiché avant de payer.
//
// Variables d'environnement nécessaires (à définir dans Netlify, PAS dans le code) :
//   STRIPE_SECRET_KEY
//   SUPABASE_URL
//   SUPABASE_SERVICE_ROLE_KEY
//   SITE_URL   (ex: https://www.monpremierlivre.com — utilisé pour les redirections après paiement)

const Stripe = require("stripe");
const { createClient } = require("@supabase/supabase-js");

exports.handler = async function (event) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch (e) {
    return { statusCode: 400, body: JSON.stringify({ error: "JSON invalide." }) };
  }

  const items = Array.isArray(body.items) ? body.items : [];
  if (!items.length) {
    return { statusCode: 400, body: JSON.stringify({ error: "Panier vide." }) };
  }

  const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
  const siteUrl = process.env.SITE_URL || "https://www.monpremierlivre.com";

  // On récupère les vrais produits en base à partir des slugs envoyés par le panier.
  const slugs = items.map((i) => i.slug).filter(Boolean);
  const { data: products, error } = await supabase
    .from("products")
    .select("slug, name, name_en, price, discount_price, discount_active, image_url, published")
    .in("slug", slugs);

  if (error) {
    return { statusCode: 500, body: JSON.stringify({ error: "Erreur base de données." }) };
  }

  const line_items = [];
  for (const item of items) {
    const p = products.find((x) => x.slug === item.slug);
    if (!p || !p.published) continue; // on ignore silencieusement un produit retiré/dépublié entre-temps
    const qty = Math.max(1, parseInt(item.qty, 10) || 1);
    const unitPrice =
      p.discount_active && p.discount_price != null && Number(p.discount_price) < Number(p.price)
        ? Number(p.discount_price)
        : Number(p.price);

    line_items.push({
      quantity: qty,
      price_data: {
        currency: "eur",
        unit_amount: Math.round(unitPrice * 100), // Stripe attend un montant en centimes
        product_data: {
          name: p.name,
          images: p.image_url ? [p.image_url] : [],
        },
      },
    });
  }

  if (!line_items.length) {
    return { statusCode: 400, body: JSON.stringify({ error: "Aucun article valide dans le panier." }) };
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card"],
      line_items,
      allow_promotion_codes: true, // permet au client de saisir un code promo (ex : réduction 1re commande)
      shipping_address_collection: { allowed_countries: ["FR", "BE", "CH", "LU", "DE", "ES", "IT", "GB", "US", "CA"] },
      automatic_tax: { enabled: false },
      success_url: `${siteUrl}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${siteUrl}/panier.html`,
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ url: session.url }),
    };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: e.message }) };
  }
};
