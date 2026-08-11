// Netlify Function — "mot de passe oublié" côté compte.html.
//
// Pourquoi une fonction serveur et pas juste sb.auth.resetPasswordForEmail() côté client ?
// Parce que Supabase ne révèle jamais (par sécurité, pour éviter l'énumération de comptes)
// si l'e-mail existe ou non : l'appel client renvoie toujours "email envoyé", même si le
// compte n'existe pas. Le client a explicitement demandé l'inverse : afficher clairement
// "cet e-mail n'est pas encore enregistré" quand ce n'est pas le cas. Pour savoir si le
// compte existe, il faut la clé service_role (jamais exposée au navigateur) — d'où cette
// fonction.
//
// Note vie privée : ce choix révèle volontairement si un e-mail est déjà client. C'est un
// compromis sécurité/UX assumé à la demande du client.
//
// Variables d'environnement nécessaires :
//   SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY

const { createClient } = require("@supabase/supabase-js");

async function findUserByEmail(supabaseAdmin, email) {
  const target = email.trim().toLowerCase();
  let page = 1;
  const perPage = 200;
  for (let i = 0; i < 50; i++) {
    const { data, error } = await supabaseAdmin.auth.admin.listUsers({ page, perPage });
    if (error || !data || !Array.isArray(data.users)) break;
    const match = data.users.find((u) => (u.email || "").toLowerCase() === target);
    if (match) return match;
    if (data.users.length < perPage) break;
    page += 1;
  }
  return null;
}

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

  const email = (body.email || "").trim();
  if (!email) {
    return { statusCode: 400, body: JSON.stringify({ error: "E-mail requis." }) };
  }

  const adminClient = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

  let user;
  try {
    user = await findUserByEmail(adminClient, email);
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: "Erreur serveur." }) };
  }

  if (!user) {
    return { statusCode: 200, body: JSON.stringify({ ok: true, exists: false }) };
  }

  const anonClient = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
  const { error: sendError } = await anonClient.auth.resetPasswordForEmail(email, {
    redirectTo: "https://monpremierlivre.com/compte.html",
  });

  if (sendError) {
    return { statusCode: 500, body: JSON.stringify({ error: sendError.message }) };
  }

  return { statusCode: 200, body: JSON.stringify({ ok: true, exists: true }) };
};
