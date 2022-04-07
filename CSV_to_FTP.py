# -> Tous les imports necessaires.
import errno
import ftplib
import os
import shutil
import stat


# -> Les identifiants du FTP de ***** <!>
FTP_HOST = "*****"
FTP_USER = "*****"
FTP_PASS = "*****"

# -> Pour rendre le code plus lisible, les chemins d'accès au programme sont écrits en amont ici.
# -> POUR LE SERVEUR D'*****
PROJPATH1 = r'C:\Users\*****\*****\ExportToCSV DisticlosOrders'
ORDRPATH1 = r'C:\Users\*****\*****\ExportToCSV DisticlosOrders\CommandesCSVPDF'
# -> POUR LE PC DE *****
PROJPATH2 = r'C:\Users\*****\*****\GitHub\*****\quickstart'
ORDRPATH2 = r'C:\Users\*****\*****\GitHub\*****\quickstart\CommandesCSVPDF'


# -> Cette fonction sert à envoyer le CSV vers le FTP de *****.
# -> Cette fonction est appelée depuis le fichier string_to_CSV.py.
def ready_tosend_CSV(filename, filepath):
    # -> Connection au FTP.
    ftp_server = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    # -> On se déplace dans le fichier de la commande contenant le CSV.
    os.chdir(ORDRPATH1 + filepath)  ################## CREDENTIAL HERE ABOUT POS
    # -> On force l'envoi vers le serveur en utf-8.
    ftp_server.encoding = "utf-8"
    # -> Depuis le serveur de *****, on va dans le sous-dossier /orders.
    ftp_server.cwd("orders")

    # -> On ouvre le fichier CSV en ReadBinary afin de l'envoyer vers le serveur.
    with open(filename, "rb") as file:
        # -> On envoie le CSV sur le FTP.
        ftp_server.storbinary(f"STOR {filename}", file)

    # -> On coupe la connection au FTP.
    ftp_server.quit()
    # -> On retourne à la base du fichier contenant le programme.
    os.chdir(PROJPATH1)  ################## CREDENTIAL HERE ABOUT POS
    # -> C'est la fin du programme, si un email doit encore être traité, le programme va se re executer.
