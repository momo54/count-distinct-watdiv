#!/bin/bash

# Répertoire contenant les fichiers
directory="queries/cd_watdiv/"

# Itérer sur chaque fichier du répertoire
for file in "$directory"/*
do
    if [ -f "$file" ]; then
        # Exécuter la commande sur le fichier
        echo "Traitement de $file"
        # Remplacez 'commande' par la commande que vous souhaitez exécuter
        python sparql_rewrite.py "$file" > $file.json
    fi
done
