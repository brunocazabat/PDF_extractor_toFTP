# -> Tous les imports nécéssaires.
import os
import time

import read_emails


# -> Le Main vient accéder aux emails, trouve et écris le nom d'é-mail dans la boite de reception.
# -> Il vient trouver ensuite le subject de chaques emails et vérifie si c'est une commande ***** ou non.
if __name__ == "__main__":
    # -> Nom du fichier qui va contenir les noms de toutes les commandes déjà vues.
    ordernames = "orders_hist.txt"
    # -> On indique au programme l'emplacement de ce fichier de commandes.
    orderhistorypath = os.path.join("ORDRTXT", ordernames)
    # -> On lance la lecture des emails -> puis la lecture des sujets -> reconnaissance de commandes -> etc.
    read_emails.read_email_list_for_subject(orderhistorypath)
    time.sleep(10)
