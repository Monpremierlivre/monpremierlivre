-- ============================================================
-- Mon Premier Livre — table des commandes
-- À copier-coller dans Supabase > SQL Editor > New query, puis "Run"
-- ============================================================

create table if not exists orders (
  id uuid primary key default gen_random_uuid(),
  stripe_session_id text unique,
  customer_email text,
  items jsonb not null default '[]',
  amount_total numeric(10,2),
  currency text default 'eur',
  status text not null default 'pending', -- pending | paid | failed
  created_at timestamptz not null default now()
);

-- Sécurité : cette table ne doit JAMAIS être lisible publiquement (adresses e-mail, montants...).
-- Elle n'est accessible que via la clé service_role (fonctions Netlify) pour l'écriture,
-- et par les comptes admin connectés (Supabase Auth, via admin.html) pour la lecture seule.
alter table orders enable row level security;

-- Permet aux comptes admin connectés (toi + associé·e) de VOIR les commandes dans admin.html.
-- Personne d'autre (visiteur non connecté) ne peut lire cette table.
drop policy if exists "orders_select_authenticated" on orders;
create policy "orders_select_authenticated" on orders
  for select
  to authenticated
  using (true);
