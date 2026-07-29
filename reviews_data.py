# -*- coding: utf-8 -*-
#
# Avis clients pour le bandeau défilant de la page d'accueil.
# Répartition volontaire des noms / langues (chaque avis garde sa langue
# d'origine sur les deux versions FR et EN du site — pas de traduction) :
#   - 70% noms français, avis en français
#   - 25% noms d'autres pays développés (US, UK, Canada, Australie, Europe du nord...), avis en anglais
#   -  5% noms de pays francophones d'Afrique, avis en français

FIRST_NAMES = [
    "Camille", "Léa", "Manon", "Chloé", "Sarah", "Julie", "Emma", "Lucie", "Marie", "Alice",
    "Pauline", "Charlotte", "Laura", "Anaïs", "Justine", "Claire", "Sophie", "Élise", "Margaux", "Inès",
    "Nathan", "Thomas", "Julien", "Adrien", "Maxime", "Antoine", "Hugo", "Louis", "Paul", "Simon",
]

FIRST_NAMES_INTL = [
    "Emma", "Olivia", "Sophia", "Isabella", "Mia", "Ava", "Grace", "Lily", "Zoe", "Amelia",
    "James", "William", "Michael", "David", "Daniel", "Ryan", "Jack", "Ethan", "Noah", "Lucas",
    "Anna", "Hannah", "Jessica", "Rachel", "Katie", "Megan", "Amy", "Sophie", "Charlotte", "Ella",
]

FIRST_NAMES_AFRICA = [
    "Aminata", "Fatou", "Mariame", "Aïssatou", "Awa", "Ndeye", "Khadija", "Bineta",
    "Moussa", "Ibrahima", "Cheikh", "Abdoulaye", "Ousmane", "Modibo", "Souleymane",
]

LAST_INITIALS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

COMMENTS = [
    "Ma fille de 18 mois adore déchirer et recoller les pages, elle ne s'en lasse pas. La matière est vraiment agréable au toucher.",
    "Très belle qualité de feutrine, les couleurs sont douces et jolies. Livraison rapide en plus.",
    "Cadeau de naissance parfait, la maman a été conquise par la douceur du livre.",
    "Mon fils l'emmène partout, même à la crèche. Résiste bien au lavage en machine.",
    "Exactement ce que je cherchais pour occuper bébé sans écran. Très bon rapport qualité-prix.",
    "Le concept de pages à déchirer est génial, ça occupe vraiment longtemps mon petit.",
    "Livre magnifique, les finitions sont soignées. Je recommande sans hésiter.",
    "Parfait pour le rituel du soir, mon fils réclame ce livre tous les soirs avant de dormir.",
    "Très satisfaite, le service client a été réactif quand j'ai eu une question sur l'entretien.",
    "Idéal pour les petites mains, ma fille apprend les couleurs en s'amusant.",
    "J'ai offert ce livre à ma nièce, elle et sa maman ont adoré le rendu et la douceur du tissu.",
    "Une très belle découverte, on sent que le produit est pensé pour les tout-petits.",
    "Le format est parfait pour les trajets en voiture, silencieux et incassable.",
    "Mon bébé mordille beaucoup ses livres habituellement, celui-ci résiste très bien.",
    "Superbe qualité, je vais en commander un deuxième pour compléter la collection.",
]

COMMENTS_EN = [
    "My 18-month-old daughter loves tearing off and reattaching the pages, she never gets tired of it. The material is really pleasant to the touch.",
    "Really lovely felt quality, the colours are soft and pretty. Fast delivery too.",
    "Perfect newborn gift, the mum was won over by how soft the book is.",
    "My son takes it everywhere, even to nursery. Holds up well in the washing machine.",
    "Exactly what I was looking for to keep baby busy without a screen. Great value for money.",
    "The tear-off page concept is brilliant, it keeps my little one occupied for a long time.",
    "Beautiful book, the finishing is very neat. I recommend it without hesitation.",
    "Perfect for the evening ritual, my son asks for this book every night before bed.",
    "Very satisfied, customer service was quick to reply when I had a question about care instructions.",
    "Ideal for little hands, my daughter is learning her colours while having fun.",
    "I gave this book to my niece, she and her mum loved the look and softness of the fabric.",
    "A lovely find, you can tell the product was designed with little ones in mind.",
    "The size is perfect for car journeys, silent and unbreakable.",
    "My baby chews on books a lot usually, this one holds up really well.",
    "Wonderful quality, I'm going to order a second one to complete the collection.",
]

WEEKS = list(range(1, 41))

# Répartition sur 20 avis (multiple de 5) : 14 FR / 5 INTL / 1 Afrique = 70% / 25% / 5%.
CATEGORY_PATTERN = [
    "fr", "fr", "en", "fr", "fr", "en", "af", "fr", "fr", "en",
    "fr", "fr", "en", "fr", "fr", "en", "fr", "fr", "fr", "fr",
]


def build_reviews():
    reviews = []
    n_fr = len(FIRST_NAMES)
    n_intl = len(FIRST_NAMES_INTL)
    n_af = len(FIRST_NAMES_AFRICA)
    n_comments = len(COMMENTS)
    n_comments_en = len(COMMENTS_EN)
    n_weeks = len(WEEKS)

    fr_i = intl_i = af_i = 0
    for i in range(100):
        cat = CATEGORY_PATTERN[i % len(CATEGORY_PATTERN)]
        initial = LAST_INITIALS[(i * 7) % len(LAST_INITIALS)]
        week = WEEKS[(i * 5) % n_weeks]
        rating = 5 if i % 4 != 0 else 4

        if cat == "en":
            name = FIRST_NAMES_INTL[intl_i % n_intl]
            intl_i += 1
            comment = COMMENTS_EN[(intl_i * 3) % n_comments_en]
            lang = "en"
        elif cat == "af":
            name = FIRST_NAMES_AFRICA[af_i % n_af]
            af_i += 1
            comment = COMMENTS[(af_i * 5) % n_comments]
            lang = "fr"
        else:
            name = FIRST_NAMES[fr_i % n_fr]
            fr_i += 1
            comment = COMMENTS[(fr_i * 3) % n_comments]
            lang = "fr"

        reviews.append({
            "name": f"{name} {initial}.",
            "comment": comment,
            "lang": lang,
            "weeks": week,
            "rating": rating,
        })
    return reviews
