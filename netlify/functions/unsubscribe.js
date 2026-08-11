// Netlify Function — lien de désabonnement cliqué depuis un e-mail de newsletter.
// GET /api/unsubscribe?u=<user_id>&t=<jeton signé>
// Le jeton est vérifié (HMAC) avant toute modification, pour qu'on ne puisse pas désabonner
// quelqu'un d'autre juste en changeant l'id dans l'URL.
//
// Variables d'environnement nécessaires :
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY
//   UNSUBSCRIBE_SECRET

const { createClient } = require("@supabase/supabase-js");
const { makeUnsubscribeToken } = require("./lib/newsletter");

function page(title, message, ok) {
  return `<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title} — Mon Premier Livre</title></head>
<body style="margin:0;background:#FDFBF7;font-family:Helvetica,Arial,sans-serif">
  <div style="max-width:480px;margin:60px auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E7DFCE">
    <div style="background:#1D4E64;padding:26px 32px;text-align:center">
      <span style="color:#fff;font-size:19px;font-weight:600;letter-spacing:.02em">Mon Premier Livre</span>
    </div>
    <div style="padding:36px;text-align:center">
      <h1 style="font-size:19px;color:${ok ? "#1D2B33" : "#B3564A"};margin:0 0 12px">${title}</h1>
      <p style="font-size:14px;color:#33454E;line-height:1.6">${message}</p>
      <a href="https://monpremierlivre.com/" style="display:inline-block;margin-top:22px;background:#1D4E64;color:#fff;text-decoration:none;padding:11px 24px;border-radius:999px;font-size:14px;font-weight:600">Retour au site</a>
    </div>
  </div>
</body></html>`;
}

exports.handler = async function (event) {
  const params = event.queryStringParameters || {};
  const userId = params.u;
  const token = params.t;

  if (!userId || !token) {
    return { statusCode: 400, headers: { "Content-Type": "text/html; charset=utf-8" }, body: page("Lien invalide", "Ce lien de désabonnement est incomplet.", false) };
  }

  if (!process.env.UNSUBSCRIBE_SECRET || token !== makeUnsubscribeToken(userId)) {
    return { statusCode: 403, headers: { "Content-Type": "text/html; charset=utf-8" }, body: page("Lien invalide", "Ce lien de désabonnement n'est pas valide.", false) };
  }

  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

  const { data: userRes, error: getErr } = await supabase.auth.admin.getUserById(userId);
  if (getErr || !userRes || !userRes.user) {
    return { statusCode: 404, headers: { "Content-Type": "text/html; charset=utf-8" }, body: page("Compte introuvable", "Impossible de retrouver ce compte.", false) };
  }

  const currentMeta = userRes.user.user_metadata || {};
  await supabase.auth.admin.updateUserById(userId, {
    user_metadata: { ...currentMeta, newsletter_opt: false },
  });

  return {
    statusCode: 200,
    headers: { "Content-Type": "text/html; charset=utf-8" },
    body: page("Vous êtes désabonné·e", "Vous ne recevrez plus les e-mails de newsletter (nouveaux livres, articles de blog). Vous continuerez bien sûr à recevoir vos e-mails de commande.", true),
  };
};
