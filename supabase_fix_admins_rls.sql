-- ============================================================
-- Mon Premier Livre — correctif : la table admins bloquait ses propres vérifications
-- À copier-coller intégralement dans Supabase > SQL Editor > New query, puis "Run"
-- ============================================================

-- La table admins a RLS activé mais n'avait aucune policy de lecture (SELECT).
-- Résultat : quand une autre policy fait "... in (select email from admins)",
-- cette sous-requête ne voit AUCUNE ligne (même pour le vrai admin), donc
-- toutes les vérifications admin échouaient (ajout produit, upload image, etc.)
--
-- Le correctif : autoriser chaque utilisateur connecté à voir UNIQUEMENT sa
-- propre ligne dans admins (s'il y en a une). Ça suffit pour que le test
-- "mon email est-il dans admins ?" fonctionne, sans exposer les emails des
-- autres admins.

drop policy if exists "Users can check their own admin status" on admins;
create policy "Users can check their own admin status"
  on admins for select
  to authenticated
  using (email = auth.jwt() ->> 'email');
