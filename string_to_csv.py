# Bruh
import csv
import re
import CSV_to_FTP


def prep_to_transform(k, filepath, nbr_product, filename):
    counter = 0
    product_pos = 0
    fnames = ['id_commande_al', 'id_client', 'id_adress_client', 'id_transporteur', 'client_firstname',
              'client_lastname', 'libelle', 'libelle_al', 'libelle_unit', 'ean', 'quantite', 'addresse1',
              'addresse2', 'code_postal', 'ville', 'pays', 'tel', 'tel_mobile']
    while "IDCLIENT" not in k[product_pos]:
        product_pos = product_pos + 1
    k[product_pos] = k[product_pos].replace('IDCLIENT', '3')
    with open(filepath[:-4] + ".csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(fnames)
        while counter < nbr_product:
            rows = [[k[product_pos + 3], k[product_pos], '*****', k[product_pos - 1], k[len(k) - 3], k[len(k) - 2],
                     k[product_pos + 4 + counter + nbr_product], k[product_pos + 4 + counter + nbr_product],
                     k[product_pos + 4 + counter + nbr_product], k[product_pos + 4 + counter + (nbr_product * 2)],
                     k[product_pos + 4 + counter], k[len(k) - 1], '', k[product_pos + 1], k[product_pos + 2],
                     k[product_pos - 2], '*****', '']]
            writer.writerows(rows)
            counter = counter + 1
    filepath = filepath.split('\\')
    CSV_to_FTP.ready_tosend_CSV(filename[:-4] + ".csv", '\\' + filepath[0])
