// Netlify Function — reçoit les notifications de Stripe (webhook).
// Sert à enregistrer une commande dans Supabase UNIQUEMENT une fois le paiement
// réellement confirmé par Stripe (jamais depuis le navigateur, pour éviter toute fraude).
// Envoie aussi un e-mail de confirmation de commande via Brevo.
//
// Variables d'environnement nécessaires :
//   STRIPE_SECRET_KEY
//   STRIPE_WEBHOOK_SECRET   (généré par Stripe quand on crée le webhook, voir instructions)
//   SUPABASE_URL
//   SUPABASE_SERVICE_ROLE_KEY
//   BREVO_API_KEY           (Brevo > SMTP & API > API Keys — pas la clé SMTP)
//   BREVO_SENDER_EMAIL      (optionnel, sinon monpremierlivre.com@gmail.com par défaut)
//
// Configuration Netlify requise : cette fonction doit recevoir le corps brut (raw body)
// de la requête pour que la vérification de signature Stripe fonctionne. C'est déjà le
// comportement par défaut des fonctions Netlify classiques (non-Edge).

const Stripe = require("stripe");
const { createClient } = require("@supabase/supabase-js");
const { escapeHtml, sendBrevoEmail } = require("./lib/email");

async function sendOrderConfirmationEmail({ toEmail, items, subtotal, shipping, total, sessionId, shippingAddress }) {
  if (!toEmail) return; // pas bloquant : pas d'email = on n'envoie rien

  const itemRows = items
    .map(
      (it) => `
    <tr>
      <td style="padding:10px 0;border-bottom:1px solid #E7DFCE;color:#1D2B33;font-size:14px">${it.quantity}× ${escapeHtml(it.name)}</td>
      <td style="padding:10px 0;border-bottom:1px solid #E7DFCE;text-align:right;color:#1D2B33;font-size:14px;white-space:nowrap">${Number(it.amount_total).toFixed(2)} €</td>
    </tr>`
    )
    .join("");

  const addressBlock = shippingAddress
    ? `
    <p style="font-size:13px;color:#8A7E70;margin-top:22px;line-height:1.6">
      Adresse de livraison :<br>
      ${escapeHtml(shippingAddress.name || "")}<br>
      ${escapeHtml(shippingAddress.line1 || "")}${shippingAddress.line2 ? ", " + escapeHtml(shippingAddress.line2) : ""}<br>
      ${escapeHtml(shippingAddress.postal_code || "")} ${escapeHtml(shippingAddress.city || "")}<br>
      ${escapeHtml(shippingAddress.country || "")}
    </p>`
    : "";

  const html = `
  <div style="background:#FDFBF7;padding:40px 20px;font-family:Helvetica,Arial,sans-serif">
    <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E7DFCE">
      <div style="background:#1D4E64;padding:26px 32px;text-align:center">
        <span style="color:#fff;font-size:19px;font-weight:600;letter-spacing:.02em">Mon Premier Livre</span>
      </div>
      <div style="padding:32px">
        <h1 style="font-size:20px;color:#1D2B33;margin:0 0 8px">Merci pour votre commande !</h1>
        <p style="font-size:14px;color:#33454E;margin:0 0 24px">Nous avons bien reçu votre paiement. Voici le récapitulatif de votre commande.</p>
        <table style="width:100%;border-collapse:collapse">${itemRows}</table>
        <table style="width:100%;margin-top:14px;border-collapse:collapse">
          <tr><td style="font-size:13px;color:#8A7E70;padding:4px 0">Sous-total</td><td style="text-align:right;font-size:13px;color:#8A7E70;padding:4px 0">${subtotal.toFixed(2)} €</td></tr>
          <tr><td style="font-size:13px;color:#8A7E70;padding:4px 0">Livraison</td><td style="text-align:right;font-size:13px;color:#8A7E70;padding:4px 0">${shipping === 0 ? "Offerte" : shipping.toFixed(2) + " €"}</td></tr>
          <tr><td style="font-size:16px;color:#1D2B33;font-weight:600;padding-top:10px;border-top:1px solid #E7DFCE">Total</td><td style="text-align:right;font-size:16px;color:#1D2B33;font-weight:600;padding-top:10px;border-top:1px solid #E7DFCE">${total.toFixed(2)} €</td></tr>
        </table>
        ${addressBlock}
        <p style="font-size:12px;color:#8A7E70;margin-top:26px">Numéro de commande : ${escapeHtml(sessionId)}</p>
        <p style="font-size:13px;color:#33454E;margin-top:22px;line-height:1.6">Vous pourrez suivre votre commande et votre numéro de suivi dès son expédition, directement depuis votre compte : <a href="https://monpremierlivre.com/compte.html" style="color:#1D4E64">Mon compte</a>.</p>
      </div>
      <div style="background:#F7EFDD;padding:18px 32px;text-align:center">
        <p style="font-size:12px;color:#8A7E70;margin:0">Mon Premier Livre — monpremierlivre.com@gmail.com</p>
      </div>
    </div>
  </div>`;

  await sendBrevoEmail({
    toEmail,
    subject: "Votre commande Mon Premier Livre est confirmée",
    html,
  });
}

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

    // Stripe peut renvoyer le même événement plusieurs fois (retries) : on regarde si la
    // commande était déjà enregistrée comme payée avant d'envoyer un nouvel email.
    const { data: existingOrder } = await supabase
      .from("orders")
      .select("id, status")
      .eq("stripe_session_id", session.id)
      .maybeSingle();
    const alreadyNotified = existingOrder && existingOrder.status === "paid";

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

    const customerEmail = session.customer_details ? session.customer_details.email : null;
    if (!alreadyNotified && customerEmail) {
      const total = session.amount_total != null ? session.amount_total / 100 : 0;
      const shipping = session.shipping_cost && session.shipping_cost.amount_total != null ? session.shipping_cost.amount_total / 100 : 0;
      const subtotal = session.amount_subtotal != null ? session.amount_subtotal / 100 : total - shipping;
      const shippingDetails = session.shipping_details || (session.customer_details && session.customer_details.address ? { name: session.customer_details.name, address: session.customer_details.address } : null);
      const shippingAddress = shippingDetails
        ? {
            name: shippingDetails.name,
            line1: shippingDetails.address ? shippingDetails.address.line1 : "",
            line2: shippingDetails.address ? shippingDetails.address.line2 : "",
            postal_code: shippingDetails.address ? shippingDetails.address.postal_code : "",
            city: shippingDetails.address ? shippingDetails.address.city : "",
            country: shippingDetails.address ? shippingDetails.address.country : "",
          }
        : null;

      await sendOrderConfirmationEmail({
        toEmail: customerEmail,
        items: lineItems.length ? lineItems : [{ name: "Votre commande", quantity: 1, amount_total: subtotal }],
        subtotal,
        shipping,
        total,
        sessionId: session.id,
        shippingAddress,
      });
    }
  }

  return { statusCode: 200, body: JSON.stringify({ received: true }) };
};
