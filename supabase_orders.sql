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
-- Elle n'est accessible que via la clé service_role, utilisée uniquement côté serveur
-- (dans les fonctions Netlify), jamais dans le navigateur. On active RLS sans ajouter
-- aucune policy publique : personne d'autre que service_role ne peut y accéder.
alter table orders enable row level security;
