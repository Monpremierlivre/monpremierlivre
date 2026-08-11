// Netlify Function — appelée automatiquement par un trigger Postgres (pg_net) quand un
// client confirme son adresse e-mail pour la première fois.
// Génère un code de réduction de bienvenue (-10%) à USAGE UNIQUE via Stripe et l'envoie par email.
//
// Fiabilité "un compte = un seul usage du code" :
//   Le code est créé côté Stripe avec max_redemptions: 1. C'est Stripe lui-même qui applique
//   cette limite au moment du paiement (Stripe Checkout a déjà "allow_promotion_codes: true"),
//   ce qui est beaucoup plus fiable qu'une vérification "maison" côté site.
//
// Idempotence (pas de double envoi) :
//   Avant de créer un code, on vérifie dans la table welcome_discount_codes si ce user_id en a
//   déjà un. Si oui, on ne fait rien. Ça protège contre un trigger qui se déclencherait 2 fois.
//
// Variables d'environnement nécessaires :
//   STRIPE_SECRET_KEY
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY
//   BREVO_API_KEY / BREVO_SENDER_EMAIL
//   WELCOME_WEBHOOK_SECRET   (doit correspondre exactement à celui mis dans le trigger SQL)

const Stripe = require("stripe");
const { createClient } = require("@supabase/supabase-js");
const { escapeHtml, sendBrevoEmail } = require("./lib/email");

function randomCode() {
  // Pas de caractères ambigus (0/O, 1/I) pour éviter les erreurs de recopie par le client.
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let s = "";
  for (let i = 0; i < 6; i++) s += chars[Math.floor(Math.random() * chars.length)];
  return "BIENVENUE-" + s;
}

async function ensureWelcomeCoupon(stripe) {
  try {
    return await stripe.coupons.retrieve("WELCOME10");
  } catch (e) {
    return await stripe.coupons.create({
      id: "WELCOME10",
      percent_off: 10,
      duration: "once",
      name: "Bienvenue -10%",
    });
  }
}

exports.handler = async function (event) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const secret = event.headers["x-webhook-secret"];
  if (!process.env.WELCOME_WEBHOOK_SECRET || secret !== process.env.WELCOME_WEBHOOK_SECRET) {
    return { statusCode: 401, body: "Unauthorized" };
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch (e) {
    return { statusCode: 400, body: "JSON invalide" };
  }

  const userId = body.user_id;
  const email = body.email;
  if (!userId || !email) {
    return { statusCode: 400, body: "user_id et email requis" };
  }

  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

  // Idempotence : si ce client a déjà un code, on ne fait rien.
  const { data: existing } = await supabase
    .from("welcome_discount_codes")
    .select("id")
    .eq("user_id", userId)
    .maybeSingle();
  if (existing) {
    return { statusCode: 200, body: JSON.stringify({ ok: true, already: true }) };
  }

  const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
  const coupon = await ensureWelcomeCoupon(stripe);

  let promoCode = null;
  let lastError = null;
  for (let attempt = 0; attempt < 5 && !promoCode; attempt++) {
    const candidate = randomCode();
    try {
      promoCode = await stripe.promotionCodes.create({
        coupon: coupon.id,
        code: candidate,
        max_redemptions: 1,
        expires_at: Math.floor(Date.now() / 1000) + 90 * 24 * 60 * 60, // valable 90 jours
      });
    } catch (e) {
      lastError = e; // code déjà pris (collision improbable) : on retente avec un autre
      promoCode = null;
    }
  }

  if (!promoCode) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Impossible de générer un code : " + (lastError && lastError.message) }),
    };
  }

  // On enregistre AVANT d'envoyer l'email : même si l'envoi échoue, on ne recréera jamais
  // un 2e code pour ce même client (c'est cette ligne que l'idempotence ci-dessus vérifie).
  await supabase.from("welcome_discount_codes").insert({
    user_id: userId,
    email,
    code: promoCode.code,
    stripe_promotion_code_id: promoCode.id,
    stripe_coupon_id: coupon.id,
  });

  const html = `
  <div style="background:#FDFBF7;padding:40px 20px;font-family:Helvetica,Arial,sans-serif">
    <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E7DFCE">
      <div style="background:#1D4E64;padding:26px 32px;text-align:center">
        <span style="color:#fff;font-size:19px;font-weight:600;letter-spacing:.02em">Mon Premier Livre</span>
      </div>
      <div style="padding:32px;text-align:center">
        <h1 style="font-size:20px;color:#1D2B33;margin:0 0 10px">Bienvenue !</h1>
        <p style="font-size:14px;color:#33454E;margin:0 0 26px">Merci d'avoir créé votre compte. Voici votre code de réduction, valable sur votre prochaine commande.</p>
        <div style="background:#F7EFDD;border:1px dashed #EF6F5E;border-radius:10px;padding:18px;margin-bottom:22px">
          <span style="font-size:22px;font-weight:700;color:#1D4E64;letter-spacing:.05em">${escapeHtml(promoCode.code)}</span>
        </div>
        <p style="font-size:13px;color:#8A7E70;line-height:1.6">-10% sur votre commande, à saisir dans le champ "Code promo" au moment du paiement.<br>Valable une seule fois, pendant 90 jours.</p>
        <a href="https://monpremierlivre.com/produits.html" style="display:inline-block;margin-top:22px;background:#1D4E64;color:#fff;text-decoration:none;padding:12px 26px;border-radius:999px;font-size:14px;font-weight:600">Découvrir nos livres</a>
      </div>
      <div style="background:#F7EFDD;padding:18px 32px;text-align:center">
        <p style="font-size:12px;color:#8A7E70;margin:0">Mon Premier Livre — monpremierlivre.com@gmail.com</p>
      </div>
    </div>
  </div>`;

  await sendBrevoEmail({
    toEmail: email,
    subject: "Votre code de réduction -10% — Mon Premier Livre",
    html,
  });

  return { statusCode: 200, body: JSON.stringify({ ok: true, code: promoCode.code }) };
};
