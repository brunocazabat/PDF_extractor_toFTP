# -> Pas d'imports pour ce fichier là.

# -> Cette fonction vient vérifier si la commande n'a pas déjà été acquise par le programme.
# -> On pourra donc éviter tout doublon vis-à-vis des commandes de *****.
def check_dup(file_name, string_to_search):
    # -> On ouvre le fichier en mode lecture-seule
    with open(file_name, 'r') as read_obj:
        # -> On lis les lignes du fichier une par une.
        for line in read_obj:
            # -> Pour chaques lignes du fichier, on vérifie si il y a une correspondance.
            if string_to_search in line:
                # -> S'il y a correspondance, donc doublon, on return true.
                return True
    # -> S'il n'y a pas correspondance, donc pas de doublon, on return false.
    return False
