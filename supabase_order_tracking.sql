-- ============================================================
-- Mon Premier Livre — suivi de commande (numéro de suivi + statut expédiée)
-- À copier-coller intégralement dans Supabase > SQL Editor > New query, puis "Run"
-- ============================================================

-- 1. Nouvelles colonnes sur la table orders
alter table orders add column if not exists tracking_number text;
alter table orders add column if not exists tracking_url text;
-- Le statut existe déjà (pending / paid / failed) ; on l'utilisera aussi avec la
-- valeur "shipped" une fois que l'admin ajoute un numéro de suivi (pas besoin
-- de contrainte supplémentaire, la colonne est un simple texte libre).

-- 2. Permettre aux admins de MODIFIER les commandes (ajouter le suivi, changer le statut)
--    Jusqu'ici seul service_role (les fonctions Netlify) pouvait écrire dans orders.
drop policy if exists "orders_update_admin" on orders;
create policy "orders_update_admin"
  on orders for update
  to authenticated
  using (auth.jwt() ->> 'email' in (select email from admins))
  with check (auth.jwt() ->> 'email' in (select email from admins));
