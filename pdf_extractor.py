# -> Tous les imports nécéssaires.
import pdfplumber

# -> Tous les imports nécéssaires de fichiers.
import delete_and_replace_funcs
import split_and_parse


# -> Cette fonction vient extraire toutes les infos du PDF.
# -> On se retrouve à la fin avec un string blindé d'informations inutiles.
def extract_pdf_infos(file_path, filename):
    with pdfplumber.open(file_path) as pdf:
        # -> Extraction du PDF téléchargé en string.
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        # -> Cette fonction vient supprimer toutes les infos inutiles de *****.
        # -> On se retrouve à la fin avec un string propre sans infos inutiles.
        text = delete_and_replace_funcs.supprime_useless_info(text)
        # -> On envoie notre string Text vers la prochaine étape du programme.
        split_and_parse.class_all_infos(text, file_path, filename)
