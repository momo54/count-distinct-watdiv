import os

# Chemin vers le fichier contenant les requêtes
input_file_path = 'stress100_test.1.sparql'  # Remplacez par le chemin correct de votre fichier

# Sous-répertoire où les fichiers de requête seront créés
output_dir = 'original_watdiv'

# Crée le sous-répertoire s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)

# Lis le fichier d'entrée et crée un fichier pour chaque requête
with open(input_file_path, 'r') as file:
    for i, line in enumerate(file):
        query = line.strip()
        if query:  # Ignore les lignes vides
            output_file_path = os.path.join(output_dir, f'query_{i+1}.sparql')
            with open(output_file_path, 'w') as output_file:
                output_file.write(query)

print(f'Tous les fichiers de requête ont été créés dans le répertoire {output_dir}.')
