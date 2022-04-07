# -> Tous les imports nécessaires.
import datetime
import email
import imaplib
import os
import traceback
from email.header import decode_header

# -> Tous les imports nécessaires de fichiers.
import check_dup
import delete_and_replace_funcs
import pdf_extractor

# -> Les identifiants <!>
# -> Toutes les infos du compte Gmail que l'on va venir lire.
# -> POUR LE SERVEUR D'*****
username1 = "*****.*****2@*****.com"
password1 = "*****"
PROJPATH1 = r'C:\Users\*****\*****\ExportToCSV DisticlosOrders'
ORDRPATH1 = r'C:\Users\*****\*****\ExportToCSV DisticlosOrders\CommandesCSVPDF'

# -> Les identifiants <!>
# -> Toutes les infos du compte Gmail que l'on va venir lire.
# -> POUR LE PC DE *****
username2 = "********@*****.com"
password2 = "*****"
PROJPATH2 = r'C:\Users\*****\*****\REPOS\*****\quickstart'
ORDRPATH2 = r'C:\Users\*****\*****\REPOS\*****\quickstart\CommandesCSVPDF'


# -> Cette fonction vient demander la vérification de si la commande à déjà été acquise ou non.
# -> On pourra donc éviter tout doublon vis-à-vis des commandes de *****.
def subject_is_an_order(subject, msg, orderhistorypath):
    print("=" * 100 + "\nObjet du mail:", subject)
    # -> On vérifie la structure du mail.
    if msg.is_multipart():
        # -> On vérifie si il y a une pièce jointe au mail.
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" in content_disposition:
                # -> On récupère le pdf.
                filename = part.get_filename()
                # -> On verifies si le nom de la commande est déjà dans orders_hist.txt
                if check_dup.check_dup("ORDRTXT/orders_hist.txt", filename):
                    print("Cette commande à déjà été traitée par le programme.\n" + "=" * 100)
                else:
                    print("C'est une nouvelle commande.")
                    folder_name = delete_and_replace_funcs.clean_name(subject)
                    if not os.path.isdir(folder_name):
                        # -> Make a folder for this email (named after the subject)
                        os.chdir(ORDRPATH2)  ################## CREDENTIAL HERE ABOUT POS
                        os.mkdir(folder_name, 777)
                    # -> On donne la bonne extension au nom du fichier, On lie le fichier à son dossier.
                    filename = delete_and_replace_funcs.clean_name(filename)[:-4] + ".pdf"
                    filepath = os.path.join(folder_name, filename)
                    # -> On télécharge le PDF
                    open(filepath, "wb").write(part.get_payload(decode=True))
                    # -> On lance la suite du programme.
                    try:
                        pdf_extractor.extract_pdf_infos(filepath, filename)
                        print("La commande " + filename + " à été importée sur le FTP de *****.\n" + "=" * 100)
                        # -> Write the name of the order in the .txt file called orders_hist.txt
                        open(orderhistorypath, "a").write(filename + "\n")
                    except IndexError:
                        os.chdir(PROJPATH2)  ################## CREDENTIAL HERE ABOUT POS
                        print("!" * 100 + "\nERROR: le programme est en faute (voir log pour l'erreur).\n" + "!" * 100)
                        with open("ICE_bugslog.log", "a") as log:
                            log.write(
                                "%s: Exception occurred:\n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            traceback.print_exc(file=log)


# -> Cette fonction est appelée après le main.
# -> Elle vient se connecter à la boite GMail, vient récuperer les messages et leurs objets pour la suite.
def read_email_list_for_subject(orderpath):
    # -> Connection à la boîte GMail.
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username1, password1)  ################################################### CREDENTIAL HERE
    # -> On va dans la boîte de reception principale.
    status, messages = imap.select("INBOX")
    # -> On affiche le nombre de mail dans l'invite de commande.
    print("#" * 100 + "\nNombre de mails dans la boiboite ->", int(messages[0]), "\n" + "=" * 100)
    for i in range(int(messages[0]), 0, -1):
        # -> On récupère le contenu du mail grâce à son ID.
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # -> On parse l'intégralité du mail pour en tirer l'objet.
                msg = email.message_from_bytes(response[1])
                # -> On décode le sujet du mail.
                subject, encoding = decode_header(msg["Subject"])[0]
                try:
                    if isinstance(subject, bytes):
                        # -> On télécharge l'objet du mail, si c'est un byte on décode le sujet en string.
                        subject = subject.decode(encoding)
                    # -> On vérifie l'objet du mail, voir s'il correspond à celui de *****.
                    if "CDE ***** " in subject:
                        # -> L'objet correspond à celui d'une commande *****, on envoie le mail vers la suite.
                        subject_is_an_order(subject, msg, orderpath)
                except TypeError:
                    os.chdir(PROJPATH2)  ################## CREDENTIAL HERE ABOUT POS
                    print("!" * 100 + "\nERROR: le mail à été rejeté (voir log pour l'erreur).\n" + "!" * 100)
                    with open("ICE_bugslog.log", "a") as log:
                        log.write("%s: Exception occurred:\n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        traceback.print_exc(file=log)
    # -> On ferme l'accès à la boîte GMail une fois tout les mails traités.
    imap.close()
    # -> On se déconnecte de la boîte GMail.
    imap.logout()
    # -> On signale à l'utilisateur la fin de l'éxécution du programme.
    print("#" * 100 + "\nFin de l'exécution du programme, plus de mails à traiter.\n" + "#" * 100)
