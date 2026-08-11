-- ============================================================
-- Mon Premier Livre — code de réduction -10% envoyé automatiquement
-- à chaque client qui confirme son adresse e-mail pour la première fois.
-- À copier-coller intégralement dans Supabase > SQL Editor > New query, puis "Run"
-- ============================================================

-- 1. Table qui garde une trace du code envoyé à chaque client (protège contre les doublons).
create table if not exists welcome_discount_codes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  email text not null,
  code text not null unique,
  stripe_promotion_code_id text,
  stripe_coupon_id text,
  created_at timestamptz not null default now()
);

alter table welcome_discount_codes enable row level security;

drop policy if exists "Users can view their own welcome code" on welcome_discount_codes;
create policy "Users can view their own welcome code"
  on welcome_discount_codes for select
  to authenticated
  using (user_id = auth.uid());

-- 2. Extension nécessaire pour appeler notre fonction Netlify depuis Postgres.
create extension if not exists pg_net with schema extensions;

-- 3. Fonction + trigger : dès que email_confirmed_at passe de vide à rempli sur un compte,
--    on appelle la fonction Netlify qui génère le code et envoie l'email.
create or replace function public.handle_email_confirmed()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if (old.email_confirmed_at is null and new.email_confirmed_at is not null) then
    perform net.http_post(
      url := 'https://monpremierlivre.com/api/send-welcome-code',
      headers := jsonb_build_object(
        'Content-Type', 'application/json',
        'x-webhook-secret', 'bfa8483a0d38608882995716a0e147af1bc530b4376ded58'
      ),
      body := jsonb_build_object('user_id', new.id, 'email', new.email)
    );
  end if;
  return new;
end;
$$;

drop trigger if exists on_auth_user_email_confirmed on auth.users;
create trigger on_auth_user_email_confirmed
  after update on auth.users
  for each row
  execute function public.handle_email_confirmed();
