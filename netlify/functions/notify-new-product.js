// Netlify Function — appelée automatiquement par un trigger Postgres (pg_net) quand un
// produit passe de "brouillon" à "publié" (ou est créé directement publié).
// Envoie un e-mail "nouveauté" à tous les clients inscrits à la newsletter.
//
// Idempotence : la colonne products.newsletter_sent_at est verrouillée dès le début du
// traitement, donc même si le trigger se déclenche 2 fois, l'email ne part qu'une seule fois.
//
// Variables d'environnement nécessaires :
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY
//   BREVO_API_KEY / BREVO_SENDER_EMAIL
//   NEWSLETTER_WEBHOOK_SECRET   (doit correspondre exactement à celui mis dans le trigger SQL)

const { createClient } = require("@supabase/supabase-js");
const { escapeHtml, sendBrevoEmail } = require("./lib/email");
const { listNewsletterSubscribers, buildUnsubscribeUrl } = require("./lib/newsletter");

exports.handler = async function (event) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const secret = event.headers["x-webhook-secret"];
  if (!process.env.NEWSLETTER_WEBHOOK_SECRET || secret !== process.env.NEWSLETTER_WEBHOOK_SECRET) {
    return { statusCode: 401, body: "Unauthorized" };
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch (e) {
    return { statusCode: 400, body: "JSON invalide" };
  }

  const productId = body.product_id;
  if (!productId) return { statusCode: 400, body: "product_id requis" };

  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

  const { data: product, error } = await supabase
    .from("products")
    .select("id, slug, name, price, image_url, newsletter_sent_at, published")
    .eq("id", productId)
    .maybeSingle();

  if (error || !product || !product.published) {
    return { statusCode: 200, body: JSON.stringify({ ok: true, skipped: true }) };
  }
  if (product.newsletter_sent_at) {
    return { statusCode: 200, body: JSON.stringify({ ok: true, already: true }) };
  }

  // On verrouille tout de suite (avant même d'envoyer) pour éviter un envoi en double.
  await supabase.from("products").update({ newsletter_sent_at: new Date().toISOString() }).eq("id", productId);

  const subscribers = await listNewsletterSubscribers(supabase);
  if (!subscribers.length) {
    return { statusCode: 200, body: JSON.stringify({ ok: true, sent: 0 }) };
  }

  const productUrl = `https://monpremierlivre.com/produit.html?slug=${encodeURIComponent(product.slug)}`;

  function buildHtml(unsubscribeUrl) {
    return `
  <div style="background:#FDFBF7;padding:40px 20px;font-family:Helvetica,Arial,sans-serif">
    <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E7DFCE">
      <div style="background:#1D4E64;padding:26px 32px;text-align:center">
        <span style="color:#fff;font-size:19px;font-weight:600;letter-spacing:.02em">Mon Premier Livre</span>
      </div>
      <div style="padding:32px;text-align:center">
        <p style="font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#EF6F5E;font-weight:700;margin:0 0 10px">Nouveauté</p>
        <h1 style="font-size:20px;color:#1D2B33;margin:0 0 14px">${escapeHtml(product.name)}</h1>
        ${product.image_url ? `<img src="${escapeHtml(product.image_url)}" alt="" style="width:100%;max-width:320px;border-radius:10px;margin-bottom:18px">` : ""}
        <p style="font-size:16px;color:#1D4E64;font-weight:600;margin:0 0 22px">${Number(product.price).toFixed(2)} €</p>
        <a href="${productUrl}" style="display:inline-block;background:#1D4E64;color:#fff;text-decoration:none;padding:12px 26px;border-radius:999px;font-size:14px;font-weight:600">Découvrir ce livre</a>
      </div>
      <div style="background:#F7EFDD;padding:18px 32px;text-align:center">
        <p style="font-size:12px;color:#8A7E70;margin:0">Mon Premier Livre — monpremierlivre.com@gmail.com</p>
        <p style="font-size:11px;color:#8A7E70;margin:8px 0 0"><a href="${unsubscribeUrl}" style="color:#8A7E70;text-decoration:underline">Se désabonner de la newsletter</a></p>
      </div>
    </div>
  </div>`;
  }

  let sent = 0;
  for (const sub of subscribers) {
    const html = buildHtml(buildUnsubscribeUrl(sub.id));
    await sendBrevoEmail({ toEmail: sub.email, subject: `Nouveau livre : ${product.name}`, html });
    sent++;
  }

  return { statusCode: 200, body: JSON.stringify({ ok: true, sent }) };
};
