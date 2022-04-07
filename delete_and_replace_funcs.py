# -> Tous les imports nécessaires.
import unicodedata
import cursed_file


def supprime_accent(k):
    k = unicodedata.normalize('NFKD', k)
    k = k.encode('ASCII', 'ignore')
    k = k.decode('utf-8')
    return k


# -> Cette fonction vient supprimer le debut le l'intitulé des références.
# -> Et vient remplacer la référence FG par l'EAN 13.
def replace_all_FGref(k):
    counter = 0
    while counter < len(k) - 1:
        if " FG-" in k[counter]:
            # -> On change le FG- par l'EAN 13 correspondant.
            k[counter] = cursed_file.cursed_func(k[counter])
            # -> Une fois article' localisée on supprime la ref du debut qui est pas utile.
            temp_list = k[counter].split(" ", 1)
            k.remove(k[counter])
            temp_list.remove(temp_list[0])
            # -> On réintègre l'article au bout de notre liste après avoir changé la ref et supprimer le libelle.
            for element in temp_list:
                k.append(element)
            # -> On rappelle la même fonction pour verifier qu'il n'y a pas d'erreurs.
        else:
            counter = counter + 1


# -> Cette fonction vient supprimer la date du str global
# -> Et c'est tout
def supprime_date(k):
    # -> Comme la date ne sera pas exportée je la supprime.
    for counter in range(len(k) - 1):
        if "/" in k[counter] and len(k[counter]) == 10:
            # -> Une fois la date localisée on supprime
            k.remove(k[counter])


# -> Une autre fonction un peu moche pour supprimer tout le contenu inutile de notre string T.
# -> Le code pourrait être alleger par un fonction MAP, plus rapide et plus propre que des .replace
def supprime_useless_info(t):
    # -> Je supprime tout ce qui ne correspond pas aux informations attendues du CSV
    # -> Je supprime les espaces en trop, les retours à la ligne en trop
    t = cursed_file.hidethecrap(t)
    # -> Après avoir tout supprimé je rajoute Le PAYS et le CODE TRANSPORTEUR ainsi que l'ID_CLIENT
    t = t + "\nFRANCE\n" + "\n309\n" + "\nIDCLIENT\n"
    # -> Je mets en page proprement mes infos en enlevant les espaces de debut de ligne
    t = "\n".join([ll.rstrip() for ll in t.splitlines() if ll.strip()])
    return t


# -> Cette fonction vient nettoyer le nom de la commande
# -> On pourra avec ça créer un dossier lisible sans espaces et caractères spéciaux
def clean_name(text):
    # -> On remplace les espaces par des _, on remplaces les minuscules par des majuscules pour faciliter la lecture.
    return "".join(c if c.isalnum() else "_" for c in text)
