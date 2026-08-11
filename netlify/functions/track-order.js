// Netlify Function — utilisée par suivi-commande.html pour afficher une commande à un
// client SANS qu'il ait besoin d'être connecté (lien reçu dans l'e-mail de confirmation).
// GET /api/track-order?s=<stripe_session_id>&t=<jeton signé>
//
// Le jeton est vérifié (HMAC) avant toute lecture, pour qu'on ne puisse pas consulter la
// commande de quelqu'un d'autre juste en changeant l'id de session dans l'URL.
//
// Variables d'environnement nécessaires :
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY
//   TRACK_ORDER_SECRET

const { createClient } = require("@supabase/supabase-js");
const { makeTrackToken } = require("./lib/tracking");

function json(statusCode, body) {
  return {
    statusCode,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
}

exports.handler = async function (event) {
  if (event.httpMethod !== "GET") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const params = event.queryStringParameters || {};
  const sessionId = params.s;
  const token = params.t;

  if (!sessionId || !token) {
    return json(400, { error: "Lien invalide." });
  }

  if (!process.env.TRACK_ORDER_SECRET || token !== makeTrackToken(sessionId)) {
    return json(403, { error: "Lien invalide." });
  }

  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

  const { data: order, error } = await supabase
    .from("orders")
    .select("created_at, items, amount_total, currency, status, tracking_number, tracking_url")
    .eq("stripe_session_id", sessionId)
    .maybeSingle();

  if (error || !order) {
    return json(404, { error: "Commande introuvable." });
  }

  return json(200, { order });
};
