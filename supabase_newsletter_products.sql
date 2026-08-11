-- ============================================================
-- Mon Premier Livre — newsletter automatique quand un produit est publié
-- À copier-coller intégralement dans Supabase > SQL Editor > New query, puis "Run"
-- ============================================================

-- 1. Colonne qui empêche d'envoyer la newsletter 2 fois pour le même produit.
alter table products add column if not exists newsletter_sent_at timestamptz;

-- 2. Extension nécessaire pour appeler notre fonction Netlify depuis Postgres
--    (ne fait rien si déjà activée par le script précédent).
create extension if not exists pg_net with schema extensions;

-- 3. Fonction + trigger : dès qu'un produit devient publié (à la création, ou en passant
--    de "Brouillon" à "Publié" dans admin.html), on appelle la fonction Netlify qui envoie
--    l'email "nouveauté" à tous les abonnés à la newsletter.
create or replace function public.notify_new_product()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if new.published = true and (tg_op = 'INSERT' or coalesce(old.published, false) = false) then
    perform net.http_post(
      url := 'https://monpremierlivre.com/api/notify-new-product',
      headers := jsonb_build_object(
        'Content-Type', 'application/json',
        'x-webhook-secret', '34749eb2cde8c0743c2003ecd698a6690f684d52cb66c340'
      ),
      body := jsonb_build_object('product_id', new.id)
    );
  end if;
  return new;
end;
$$;

drop trigger if exists on_product_published on products;
create trigger on_product_published
  after insert or update on products
  for each row
  execute function public.notify_new_product();
