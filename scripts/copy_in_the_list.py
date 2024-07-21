import os
import shutil
import pandas as pd
import sys

def move(file_path,source_directory,destination_directory):
    data = pd.read_csv(file_path)

    # Définir les répertoires source et destination
    source_directory = 'queries/original_watdiv'
    destination_directory = 'queries/top5_nbtp_original_watdiv'

    # Créer le répertoire de destination s'il n'existe pas
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Copier tous les fichiers listés dans le fichier
    for file_name in data['query_name']:
        file_name = os.path.basename(file_name)
        source_file = os.path.join(source_directory, file_name)
        destination_file = os.path.join(destination_directory, file_name)
        if os.path.exists(source_file):
            shutil.copy(source_file, destination_file)
            print(f'Copié: {file_name}')
        else:
            print(f'Fichier non trouvé: {source_file}')

# python scripts/copy_in_the_list.py top5_nbtp_original_watdiv.csv queries/original_watdiv queries/top5_nbtp_original_watdiv
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <path_to_csv_file> <src_dir> <dest_dir>")
    else:
        file_path = sys.argv[1]
        src = sys.argv[2]
        dest = sys.argv[3]
        move(file_path,src,dest)
