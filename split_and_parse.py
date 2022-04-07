# -> Tous les imports nécéssaires de fichiers.
import delete_and_replace_funcs
import re
import string_to_csv


# ->
# ->
def name_isolation(k):
    temp_list = k[0].split(' ', 2)
    for element in temp_list:
        k.append(element)
    k.remove(k[0])
    return k


# -> Cette fonction vient trouver le code EAN de l'article
# -> Et vient l'écrire dans un autre tableau au bout du str global
def pick_EAN(k):
    for counter in range(len(k)):
        if " 36625810" in k[counter]:
            EAN = k[counter][-13:]
            k[counter] = k[counter][:-14]
            k.append(EAN)
    return k


# -> Cette fonction vient trouver la quantité des produits
# -> Et Print le chiffre en question
def pick_quantity(k, product_nbr, pos):
    counter = 0
    while counter < product_nbr:
        # -> Je viens récupérer la partie du string qui contient la quantité et la coupe en deux avec un espace
        quantity = k[pos][-4:].split(' ')
        # -> Je supprime la zone qui ne correspond pas à la quantité au debut du str quantity
        quantity.remove(quantity[0])
        # -> Je supprime ma quantité de sa position actuelle du str global qui n'est pas bonne.
        size = len(quantity[0]) + 1
        k[pos] = k[pos][:-size]
        # -> J'ajoute ma quantité à la fin de la liste
        temp_list = k[pos]
        k.remove(k[pos])
        k.append(temp_list)
        k.append(quantity[0])
        counter = counter + 1
    return k


# -> Cette fonction vient trouver le nombre de produits
# -> Et vient écrire le chiffre exact.
def nbr_of_product(text):
    counter = text.count(" FG-")
    print("Il y a ", counter, "produits dans cette commande.")
    return counter


# ->
# ->
def clean_doublon(k):
    new_list = []
    for i in k:
        if i not in new_list:
            new_list.append(i)
    k = new_list
    return k


# ->
# ->
def clean_ref(k):
    counter = 0
    while counter < len(k):
        if "REF " in k[counter]:
            # -> Une fois la date localisée on supprime
            k.remove(k[counter])
        else:
            counter = counter + 1
    return k


# ->
# ->
def REFINTERNEandDATEsplitter(k):
    temp_list = k[2].split(' ', 2)
    k.remove(k[2])
    for element in temp_list:
        k.append(element)
    temp_list = k[2].split(' ', 2)
    k.remove(k[2])
    for bruh in range(2):
        k.append(temp_list[0])
        temp_list.remove(temp_list[0])
    return k


def look_for_number_or_email(k):
    pos = 0
    pattern1 = re.compile("(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})", re.IGNORECASE)
    for counter in range(len(k)):
        print(k[pos])
        if re.search(pattern1, k[pos]) or "@" in k[pos]:
            k.remove(k[pos])
        else:
            pos = pos + 1
    return k


# ->
# ->
def lookforZandAdress(k):
    postalpattern = re.compile("^[\dA-Z]{5} $", re.IGNORECASE)
    if "Z." in k[2] or "z." in k[2] or "ZAC " in k[2] or "ZI " in k[2] or "ZA " in k[2]:
        # -> on a une adresse et un deuxieme champ avec un Z dans k[2]
        if "Avenue" in k[1] or "Route" in k[1] or "Rue" in k[1] or "Allée" in k[1] or "Impasse" in k[1]:
            k[1] = k[1] + ' ' + k[2]
            k.remove(k[2])
    if "Z." in k[1] or "z." in k[1] or "ZAC " in k[1] or "ZI " in k[1] or "ZA " in k[1] or "Zone" in k[1]:
        if re.search(postalpattern, k[2][:6]):
            # -> Le code postal se trouve bien après l'adresse
            return k
        elif re.search(postalpattern, k[3][:6]):
            # -> L'adresse est sur deux cases donc on les fusionnes
            k[1] = k[1] + ' ' + k[2]
            k.remove(k[2])
        else:
            # -> Rien à faire si le code postal est ailleur. Donc erreur.
            return k

    return k


# -> Cette fonction vient diviser le string T en une list
# -> Et redécoupe chaques infos groupées en sous-liste.
def class_all_infos(t, file_path, filename):
    product_nbr = nbr_of_product(t)
    k = t.split("\n")
    k = clean_doublon(k)
    k = look_for_number_or_email(k)
    print(k)
    k = lookforZandAdress(k)
    k = REFINTERNEandDATEsplitter(k)
    k = clean_ref(k)
    k = pick_quantity(k, product_nbr, 2)
    k[0] = k[0] + ' ' + k[1]
    k.remove(k[1])
    delete_and_replace_funcs.supprime_date(k)
    delete_and_replace_funcs.replace_all_FGref(k)
    pick_EAN(k)
    k = name_isolation(k)
    counter = 0
    while counter < len(k) - 1:
        k[counter] = delete_and_replace_funcs.supprime_accent(k[counter])
        counter = counter + 1
    string_to_csv.prep_to_transform(k, file_path, product_nbr, filename)
