// Utilitaire partagé — envoi d'e-mails transactionnels via l'API Brevo.
// Utilisé par plusieurs fonctions (confirmation de commande, code de bienvenue, newsletter...).

function escapeHtml(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

async function sendBrevoEmail({ toEmail, subject, html }) {
  const apiKey = process.env.BREVO_API_KEY;
  const senderEmail = process.env.BREVO_SENDER_EMAIL || "monpremierlivre.com@gmail.com";
  if (!apiKey || !toEmail) return { skipped: true };
  try {
    const res = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: {
        accept: "application/json",
        "api-key": apiKey,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        sender: { name: "Mon Premier Livre", email: senderEmail },
        to: [{ email: toEmail }],
        subject,
        htmlContent: html,
      }),
    });
    return { ok: res.ok, status: res.status };
  } catch (e) {
    // non-bloquant : un échec d'envoi d'email ne doit jamais faire planter la fonction appelante
    return { ok: false, error: e.message };
  }
}

module.exports = { escapeHtml, sendBrevoEmail };
