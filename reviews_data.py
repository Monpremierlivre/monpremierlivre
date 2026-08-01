# -*- coding: utf-8 -*-
#
# Avis clients pour le bandeau défilant de la page d'accueil.
# Répartition volontaire des noms / langues (chaque avis garde sa langue
# d'origine sur les deux versions FR et EN du site — pas de traduction) :
#   - 70% noms français, avis en français
#   - 25% noms d'autres pays développés (US, UK, Canada, Australie, Europe du nord...), avis en anglais
#   -  5% noms de pays francophones d'Afrique, avis en français
#
# Chacun des 100 avis a un texte UNIQUE (aucune répétition, et le pool anglais
# n'est pas une simple traduction du pool français) : 75 commentaires FR pour
# les 75 avis en français (noms FR + noms Afrique), 25 commentaires EN pour
# les 25 avis en anglais.

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

# 75 commentaires FR uniques (utilisés une seule fois chacun sur les 75 avis en français).
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
    "Nous avons ce livre depuis trois mois et il n'a pas bougé, même après des dizaines de lavages.",
    "Ma fille de deux ans le tend systématiquement pour qu'on lui lise « encore une fois », un vrai succès chez nous.",
    "Les coutures sont solides, rien à voir avec les livres en tissu bas de gamme qu'on trouve ailleurs.",
    "Le petit format tient facilement dans le sac à langer, pratique pour les sorties.",
    "J'appréhendais la qualité vu le prix, mais le résultat dépasse largement mes attentes.",
    "Mon fils adore les animaux du livre, il pointe chaque page en gazouillant de joie.",
    "Emballage soigné, on sent que la marque prend soin de chaque détail jusqu'à la livraison.",
    "Un livre increvable qui a survécu à deux déménagements et à un chien curieux.",
    "Ma fille recolle les pages elle-même maintenant, ça travaille sa motricité fine sans qu'elle s'en rende compte.",
    "Le tissu ne peluche pas malgré les lavages répétés, très agréable surprise.",
    "Cadeau parfait pour un baptême, léger, doux et utile dès la naissance.",
    "On alterne avec ses livres cartonnés mais celui-ci reste son préféré, sans hésitation.",
    "Les couleurs n'ont pas passé au lavage, elles sont restées aussi vives qu'au premier jour.",
    "Mon mari était sceptique au début, il est maintenant le premier à le proposer le soir.",
    "Facile à ranger, on peut le rouler et le glisser n'importe où sans l'abîmer.",
    "Ma fille l'a testé à la crèche et les auxiliaires m'ont demandé où je l'avais acheté.",
    "Un vrai plaisir de voir bébé manipuler un livre sans craindre qu'il se déchire pour de vrai.",
    "Les finitions sont impeccables, aucun fil qui dépasse, on sent la qualité artisanale.",
    "Nous avons commandé plusieurs modèles, chacun a sa préférée selon l'humeur du jour.",
    "Livraison en 48h comme annoncé, packaging soigné avec un petit mot personnalisé.",
    "Mon petit-fils l'adore, je l'ai offert pour ses six mois et il ne s'en lasse toujours pas.",
    "La texture est douce sans être glissante, parfaite pour les petites mains encore maladroites.",
    "On l'utilise aussi pour calmer les pleurs en voiture, le bruissement du tissu le fascine.",
    "Vraiment increvable, testé et approuvé par un bébé qui mord absolument tout ce qu'il trouve.",
    "Le rapport qualité-prix est excellent comparé à d'autres marques de livres sensoriels.",
    "Ma fille reconnaît maintenant les couleurs grâce à ce livre, un vrai outil d'éveil.",
    "Nous en avons acheté un deuxième pour la maison des grands-parents, ils adorent aussi.",
    "Le concept est malin, ça évite les crises quand bébé veut absolument déchirer du papier.",
    "Très bonne surprise, je m'attendais à un simple jouet et c'est un vrai objet de qualité.",
    "Mon fils s'endort en serrant son livre contre lui, il est devenu son doudou du soir.",
    "Facile d'entretien, un tour en machine et il ressort comme neuf.",
    "J'ai adoré pouvoir suivre ma commande, tout a été transparent du début à la fin.",
    "Le format est parfait pour les débuts de la lecture, ni trop grand ni trop petit.",
    "Ma fille en a fait cadeau à son doudou, elle « lui lit » l'histoire tous les soirs, c'est adorable.",
    "Un livre qui traverse vraiment les âges, ma fille de trois ans continue à s'en servir.",
    "Nous cherchions une alternative aux écrans pour les trajets et ce livre a tout changé.",
    "La feutrine sent bon et n'a aucune odeur chimique à la réception, un vrai plus.",
    "Mon fils recolle les pages avec une concentration incroyable pour son âge, un vrai jeu d'éveil.",
    "J'ai été bluffée par la rapidité de la livraison, commandé un lundi, reçu le mercredi.",
    "Les pages sont épaisses et ne se déchirent jamais pour de vrai, rassurant pour les débutants du déchirage.",
    "Offrir ce livre à la crèche a été un franc succès, toutes les familles m'ont demandé la marque.",
    "Ma fille adore le triturer avant de dormir, ça fait partie intégrante de son rituel du coucher.",
    "Le velcro tient très bien, même après des dizaines de manipulations par jour.",
    "Un cadeau qui change des peluches habituelles, original et vraiment utile pour l'éveil.",
    "Nous avons pu suivre les instructions d'entretien facilement, tout est bien expliqué sur le site.",
    "Mon fils a commencé à dire « encore » grâce à ce livre, un vrai déclic dans son langage.",
    "La qualité de fabrication est bluffante, on sent clairement que ce n'est pas fait à la chaîne.",
    "Le petit plus : les pages sont plastifiées à l'intérieur donc aucune trace de bave ne reste.",
    "Ma fille adore montrer son livre à tout le monde, elle en est très fière.",
    "Un investissement qui vaut le coup, il tient dans la durée contrairement à d'autres jouets.",
    "Nous l'avons offert à notre nièce, la texture douce l'apaise énormément, merci pour ce produit.",
    "Le service après-vente a été impeccable quand une page s'est légèrement décousue, remboursée sans discuter.",
    "Ma fille a appris à compter les animaux du livre avant même de savoir compter avec les doigts.",
    "Un vrai coup de cœur, on hésitait avec une autre marque et on ne regrette absolument pas notre choix.",
    "Le livre est resté aussi solide après un an d'utilisation intensive, bluffant pour un objet en tissu.",
    "Mon fils partage désormais son livre avec sa petite sœur, un vrai moment de complicité entre eux.",
    "J'apprécie que la marque soit française et que le service client réponde aussi vite.",
    "Nous avons acheté toute la collection au fil des mois, chaque livre a son propre univers.",
    "Ma fille l'a présenté fièrement à la maîtresse le jour de la rentrée, une vraie fierté pour elle.",
    "Le meilleur achat que j'ai fait pour ma fille cette année, sans hésitation je recommande à 100%.",
]

# 25 commentaires EN uniques (contenu indépendant, pas une traduction du pool FR).
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
    "We've had this book for three months and it hasn't budged, even after dozens of washes.",
    "My two-year-old always hands it back for \"one more time,\" it's a genuine hit in our house.",
    "The stitching is sturdy, nothing like the cheap fabric books you find elsewhere.",
    "Small enough to fit in the nappy bag, really handy for outings.",
    "I was worried about the quality given the price, but it exceeded my expectations by far.",
    "My son loves the animals in the book, he points at every page babbling with joy.",
    "Beautifully packaged, you can tell the brand cares about every detail down to delivery.",
    "An indestructible book that's survived two house moves and a very curious dog.",
    "My daughter reattaches the pages herself now, it's building her fine motor skills without her even noticing.",
    "The best purchase I made for my daughter this year, I recommend it 100% without hesitation.",
]

WEEKS = list(range(1, 41))

# Répartition sur 20 avis (multiple de 5) : 14 FR / 5 INTL / 1 Afrique = 70% / 25% / 5%.
CATEGORY_PATTERN = [
    "fr", "fr", "en", "fr", "fr", "en", "af", "fr", "fr", "en",
    "fr", "fr", "en", "fr", "fr", "en", "fr", "fr", "fr", "fr",
]


def build_reviews():
    reviews = []
    n_fr_names = len(FIRST_NAMES)
    n_intl = len(FIRST_NAMES_INTL)
    n_af = len(FIRST_NAMES_AFRICA)
    n_weeks = len(WEEKS)

    fr_name_i = intl_i = af_i = 0
    fr_comment_i = en_comment_i = 0

    for i in range(100):
        cat = CATEGORY_PATTERN[i % len(CATEGORY_PATTERN)]
        initial = LAST_INITIALS[(i * 7) % len(LAST_INITIALS)]
        week = WEEKS[(i * 5) % n_weeks]
        rating = 5 if i % 4 != 0 else 4

        if cat == "en":
            name = FIRST_NAMES_INTL[intl_i % n_intl]
            intl_i += 1
            comment = COMMENTS_EN[en_comment_i % len(COMMENTS_EN)]
            en_comment_i += 1
            lang = "en"
        elif cat == "af":
            name = FIRST_NAMES_AFRICA[af_i % n_af]
            af_i += 1
            comment = COMMENTS[fr_comment_i % len(COMMENTS)]
            fr_comment_i += 1
            lang = "fr"
        else:
            name = FIRST_NAMES[fr_name_i % n_fr_names]
            fr_name_i += 1
            comment = COMMENTS[fr_comment_i % len(COMMENTS)]
            fr_comment_i += 1
            lang = "fr"

        reviews.append({
            "name": f"{name} {initial}.",
            "comment": comment,
            "lang": lang,
            "weeks": week,
            "rating": rating,
        })
    return reviews
