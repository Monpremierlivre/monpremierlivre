// Netlify Function — envoie une newsletter (ex : nouvel article de blog) à tous les abonnés.
// Appelée depuis admin.html (onglet "Newsletter"), protégée : seul un compte présent dans la
// table `admins` peut déclencher un envoi (vérifié via le token de session Supabase envoyé
// dans l'en-tête Authorization).
//
// Variables d'environnement nécessaires :
//   SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY
//   BREVO_API_KEY / BREVO_SENDER_EMAIL

const { createClient } = require("@supabase/supabase-js");
const { escapeHtml, sendBrevoEmail } = require("./lib/email");
const { listNewsletterSubscribers, buildUnsubscribeUrl } = require("./lib/newsletter");

exports.handler = async function (event) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const authHeader = event.headers["authorization"] || event.headers["Authorization"] || "";
  const token = authHeader.replace(/^Bearer\s+/i, "").trim();
  if (!token) {
    return { statusCode: 401, body: "Non authentifié." };
  }

  // On vérifie l'identité avec la clé anon (comme le ferait le navigateur), puis on vérifie
  // le statut admin avec la clé service_role (qui seule peut lire la table admins sans RLS).
  const anonClient = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
  const { data: userData, error: userError } = await anonClient.auth.getUser(token);
  if (userError || !userData || !userData.user) {
    return { statusCode: 401, body: "Session invalide." };
  }

  const adminClient = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
  const { data: adminRow } = await adminClient
    .from("admins")
    .select("email")
    .eq("email", userData.user.email)
    .maybeSingle();
  if (!adminRow) {
    return { statusCode: 403, body: "Accès refusé : ce compte n'est pas administrateur." };
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch (e) {
    return { statusCode: 400, body: "JSON invalide." };
  }

  const title = (body.title || "").trim();
  const url = (body.url || "").trim();
  const excerpt = (body.excerpt || "").trim();
  if (!title || !url) {
    return { statusCode: 400, body: JSON.stringify({ error: "Titre et lien requis." }) };
  }

  const subscribers = await listNewsletterSubscribers(adminClient);
  if (!subscribers.length) {
    return { statusCode: 200, body: JSON.stringify({ ok: true, sent: 0 }) };
  }

  function buildHtml(unsubscribeUrl) {
    return `
  <div style="background:#FDFBF7;padding:40px 20px;font-family:Helvetica,Arial,sans-serif">
    <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E7DFCE">
      <div style="background:#1D4E64;padding:26px 32px;text-align:center">
        <span style="color:#fff;font-size:19px;font-weight:600;letter-spacing:.02em">Mon Premier Livre</span>
      </div>
      <div style="padding:32px">
        <p style="font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#EF6F5E;font-weight:700;margin:0 0 10px;text-align:center">Nouvel article</p>
        <h1 style="font-size:20px;color:#1D2B33;margin:0 0 14px;text-align:center">${escapeHtml(title)}</h1>
        ${excerpt ? `<p style="font-size:14px;color:#33454E;line-height:1.6;text-align:center">${escapeHtml(excerpt)}</p>` : ""}
        <div style="text-align:center;margin-top:22px">
          <a href="${escapeHtml(url)}" style="display:inline-block;background:#1D4E64;color:#fff;text-decoration:none;padding:12px 26px;border-radius:999px;font-size:14px;font-weight:600">Lire l'article</a>
        </div>
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
    await sendBrevoEmail({ toEmail: sub.email, subject: `Nouvel article : ${title}`, html });
    sent++;
  }

  return { statusCode: 200, body: JSON.stringify({ ok: true, sent }) };
};
