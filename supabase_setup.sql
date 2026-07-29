-- ============================================================
-- Mon Premier Livre — script d'installation Supabase
-- À copier-coller intégralement dans Supabase > SQL Editor > New query, puis "Run"
-- ============================================================

-- 1. Table des produits
create table if not exists products (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  name_en text not null,
  price numeric(10,2) not null default 30.00,
  age text,
  age_en text,
  short text,
  short_en text,
  long_desc text,
  long_desc_en text,
  care text,
  care_en text,
  tags text[] default '{}',
  image_url text,
  stock integer default 100,
  published boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- 2. Activer la sécurité au niveau des lignes (RLS)
alter table products enable row level security;

-- 3. Tout le monde (visiteurs du site) peut LIRE les produits publiés
create policy "Public can read published products"
  on products for select
  using (published = true);

-- 4. Seul un utilisateur connecté (toi, via le compte admin) peut ajouter/modifier/supprimer
create policy "Authenticated users can insert products"
  on products for insert
  to authenticated
  with check (true);

create policy "Authenticated users can update products"
  on products for update
  to authenticated
  using (true);

create policy "Authenticated users can delete products"
  on products for delete
  to authenticated
  using (true);

-- 5. Mettre à jour updated_at automatiquement
create or replace function set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists trg_products_updated_at on products;
create trigger trg_products_updated_at
  before update on products
  for each row execute function set_updated_at();

-- 6. Bucket de stockage pour les photos produits
insert into storage.buckets (id, name, public)
values ('product-images', 'product-images', true)
on conflict (id) do nothing;

create policy "Public can view product images"
  on storage.objects for select
  using (bucket_id = 'product-images');

create policy "Authenticated users can upload product images"
  on storage.objects for insert
  to authenticated
  with check (bucket_id = 'product-images');

-- ============================================================
-- Terminé ! Une fois exécuté, tu devrais voir la table "products"
-- apparaître dans Table Editor, et le bucket "product-images"
-- apparaître dans Storage.
-- ============================================================
