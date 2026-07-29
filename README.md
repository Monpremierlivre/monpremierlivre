# Mon Premier Livre — site web

## Ce qui est prêt
- Accueil, Nos livres (9 produits d'exemple), 9 fiches produit, FAQ (50 questions), Blog (100 articles), Mon compte, Panier.
- Français par défaut, bouton FR/EN en haut à droite (l'interface bascule ; les textes longs — articles de blog, réponses FAQ, descriptions produit — restent en français pour l'instant, à traduire au fil de l'eau).
- Panier, liste de souhaits (♥) et compteur de panier fonctionnent déjà dans le navigateur (stockés localement, sans serveur).
- Logo "petite étagère" (assets/logo.svg) sur chaque page.
- Bandeau de confiance + pied de page à 3 colonnes repris sur toutes les pages, dans les couleurs Morandi du site (structure copiée de votre modèle, textes adaptés à Mon Premier Livre).
- Photos : emplacements réservés (hero, portrait fondatrice, produits) — à remplacer par vos vraies photos dès que vous me les envoyez.

## Ce qui nécessite un service externe (je ne peux pas l'héberger moi-même)
Pour que "Acheter maintenant", la création de compte réelle et l'envoi d'e-mails fonctionnent vraiment (pas seulement dans le navigateur), il faut connecter :
1. **Paiement** : Stripe Checkout (ou PayPal) — création d'une session de paiement côté serveur + webhook de confirmation.
2. **Comptes clients** : une base de données + authentification (ex. Supabase, Firebase Auth) pour stocker comptes, commandes, code de réduction -10%.
3. **E-mails automatiques** : un service comme Brevo, Mailchimp ou Resend pour l'e-mail de bienvenue, les alertes nouveautés/blog, et les factures.

Je peux vous aider à brancher chacun de ces services dès que vous aurez choisi vos prestataires (souvent gratuits pour démarrer).

## Comment voir le site
Ouvrez `index.html` dans un navigateur, ou déposez tout le dossier sur votre hébergement (Netlify, Vercel, OVH...).
