// Utilitaire partagé — construit un lien de suivi de commande accessible SANS compte client
// (utile pour les clients qui commandent sans créer de compte). Le lien contient un jeton
// signé (HMAC) basé sur l'id de session Stripe : impossible à deviner ou modifier sans
// connaître TRACK_ORDER_SECRET, donc personne ne peut consulter la commande de quelqu'un
// d'autre juste en changeant l'id dans l'URL.

const crypto = require("crypto");

function makeTrackToken(sessionId) {
  const secret = process.env.TRACK_ORDER_SECRET || "";
  return crypto.createHmac("sha256", secret).update(String(sessionId)).digest("hex").slice(0, 32);
}

function buildTrackOrderUrl(sessionId) {
  const token = makeTrackToken(sessionId);
  return `https://monpremierlivre.com/suivi-commande.html?s=${encodeURIComponent(sessionId)}&t=${token}`;
}

module.exports = { makeTrackToken, buildTrackOrderUrl };
