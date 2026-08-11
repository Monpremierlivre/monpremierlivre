// Utilitaire partagé — liste les clients inscrits à la newsletter, et gère les liens de désabonnement.
// Un client est considéré abonné si : (1) son compte a "newsletter_opt" coché à l'inscription,
// et (2) son e-mail est confirmé (on n'envoie jamais à une adresse non vérifiée).
//
// Nécessite un client Supabase créé avec la clé SUPABASE_SERVICE_ROLE_KEY (seule cette clé
// a accès à l'API admin listUsers()).

const crypto = require("crypto");

async function listNewsletterSubscribers(supabaseAdmin) {
  const subscribers = new Map(); // email -> user id (dédoublonné par email)
  let page = 1;
  const perPage = 200;
  for (let i = 0; i < 50; i++) {
    // garde-fou anti boucle infinie
    const { data, error } = await supabaseAdmin.auth.admin.listUsers({ page, perPage });
    if (error || !data || !Array.isArray(data.users)) break;
    data.users.forEach((u) => {
      const meta = u.user_metadata || {};
      const optedIn = meta.newsletter_opt === true || meta.newsletter_opt === "true";
      if (optedIn && u.email && u.email_confirmed_at) {
        subscribers.set(u.email, u.id);
      }
    });
    if (data.users.length < perPage) break;
    page += 1;
  }
  return Array.from(subscribers, ([email, id]) => ({ email, id }));
}

// Génère un jeton signé (HMAC) à partir de l'id du client : impossible à deviner ou à
// falsifier sans connaître UNSUBSCRIBE_SECRET, donc personne ne peut désabonner un autre
// client à sa place juste en changeant l'id dans l'URL.
function makeUnsubscribeToken(userId) {
  const secret = process.env.UNSUBSCRIBE_SECRET || "";
  return crypto.createHmac("sha256", secret).update(String(userId)).digest("hex").slice(0, 32);
}

function buildUnsubscribeUrl(userId) {
  const token = makeUnsubscribeToken(userId);
  return `https://monpremierlivre.com/api/unsubscribe?u=${encodeURIComponent(userId)}&t=${token}`;
}

module.exports = { listNewsletterSubscribers, makeUnsubscribeToken, buildUnsubscribeUrl };
