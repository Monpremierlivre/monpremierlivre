-- ============================================================
-- Mon Premier Livre — activer les comptes clients en toute sécurité
-- À copier-coller intégralement dans Supabase > SQL Editor > New query, puis "Run"
--
-- IMPORTANT : avant de lancer ce script, remplace tout en bas
-- ('TON_EMAIL_ADMIN_ICI' etc.) par le ou les e-mails de tes comptes
-- admin (toi + ton associé·e si déjà créé), sinon vous perdrez l'accès
-- à admin.html une fois ce script exécuté.
-- ============================================================

-- 1. Table listant les e-mails ayant un accès admin (admin.html : produits + commandes)
create table if not exists admins (
  email text primary key
);
alter table admins enable row level security;
-- Personne ne peut lire cette table depuis le navigateur (ni clé anon, ni clé authenticated) :
-- elle n'est utilisée qu'à l'intérieur des policies ci-dessous (via "select email from admins").

-- 2. Ajoute ici tes e-mails admin (un par ligne). Remplace les valeurs avant d'exécuter !
insert into admins (email) values
  ('TON_EMAIL_ADMIN_ICI@exemple.com')
on conflict (email) do nothing;
-- Pour ajouter ton/ta associé·e, ajoute une ligne :
-- insert into admins (email) values ('email-associe@exemple.com') on conflict (email) do nothing;

-- ============================================================
-- 3. Reserrer les policies "products" : seuls les admins peuvent écrire
--    (avant, n'importe quel compte connecté — donc n'importe quel client
--    inscrit — pouvait ajouter/modifier/supprimer des produits)
-- ============================================================
drop policy if exists "Authenticated users can insert products" on products;
drop policy if exists "Authenticated users can update products" on products;
drop policy if exists "Authenticated users can delete products" on products;

create policy "Admins can insert products"
  on products for insert
  to authenticated
  with check (auth.jwt() ->> 'email' in (select email from admins));

create policy "Admins can update products"
  on products for update
  to authenticated
  using (auth.jwt() ->> 'email' in (select email from admins));

create policy "Admins can delete products"
  on products for delete
  to authenticated
  using (auth.jwt() ->> 'email' in (select email from admins));

-- 4. Pareil pour l'upload d'images produits (Storage)
drop policy if exists "Authenticated users can upload product images" on storage.objects;

create policy "Admins can upload product images"
  on storage.objects for insert
  to authenticated
  with check (
    bucket_id = 'product-images'
    and auth.jwt() ->> 'email' in (select email from admins)
  );

-- ============================================================
-- 5. Reserrer la policy "orders" : un client ne voit que SES commandes,
--    un admin voit toutes les commandes.
-- ============================================================
drop policy if exists "orders_select_authenticated" on orders;

create policy "orders_select_own_or_admin"
  on orders for select
  to authenticated
  using (
    customer_email = auth.jwt() ->> 'email'
    or auth.jwt() ->> 'email' in (select email from admins)
  );

-- ============================================================
-- Terminé ! Une fois exécuté :
-- - Seuls les e-mails listés dans "admins" peuvent gérer les produits et voir toutes les commandes.
-- - N'importe quel visiteur peut créer un compte client (via compte.html), mais un compte client
--   normal ne peut voir que ses propres commandes, et ne peut pas toucher aux produits.
-- ============================================================
