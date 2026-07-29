// Netlify Function — reçoit les notifications de Stripe (webhook).
// Sert à enregistrer une commande dans Supabase UNIQUEMENT une fois le paiement
// réellement confirmé par Stripe (jamais depuis le navigateur, pour éviter toute fraude).
//
// Variables d'environnement nécessaires :
//   STRIPE_SECRET_KEY
//   STRIPE_WEBHOOK_SECRET   (généré par Stripe quand on crée le webhook, voir instructions)
//   SUPABASE_URL
//   SUPABASE_SERVICE_ROLE_KEY
//
// Configuration Netlify requise : cette fonction doit recevoir le corps brut (raw body)
// de la requête pour que la vérification de signature Stripe fonctionne. C'est déjà le
// comportement par défaut des fonctions Netlify classiques (non-Edge).

const Stripe = require("stripe");
const { createClient } = require("@supabase/supabase-js");

exports.handler = async function (event) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
  const sig = event.headers["stripe-signature"];

  let stripeEvent;
  try {
    stripeEvent = stripe.webhooks.constructEvent(
      event.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    return { statusCode: 400, body: `Signature webhook invalide : ${err.message}` };
  }

  if (stripeEvent.type === "checkout.session.completed") {
    const session = stripeEvent.data.object;
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

    let lineItems = [];
    try {
      const stripe2 = Stripe(process.env.STRIPE_SECRET_KEY);
      const li = await stripe2.checkout.sessions.listLineItems(session.id, { limit: 100 });
      lineItems = li.data.map((l) => ({
        name: l.description,
        quantity: l.quantity,
        amount_total: l.amount_total / 100,
      }));
    } catch (e) {
      // pas bloquant : on enregistre quand même la commande sans le détail des lignes
    }

    await supabase.from("orders").upsert(
      {
        stripe_session_id: session.id,
        customer_email: session.customer_details ? session.customer_details.email : null,
        items: lineItems,
        amount_total: session.amount_total != null ? session.amount_total / 100 : null,
        currency: session.currency,
        status: "paid",
      },
      { onConflict: "stripe_session_id" }
    );
  }

  return { statusCode: 200, body: JSON.stringify({ received: true }) };
};
