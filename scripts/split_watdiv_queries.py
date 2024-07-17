import re

# Lire le contenu du fichier source
with open('top10-watdiv.txt', 'r') as file:
    content = file.read()

# Utiliser une expression régulière pour extraire les requêtes et leurs informations
queries = re.split(r'-------------------------------------', content)

for query in queries:
    if query.strip():  # Ignorer les lignes vides
        # Extraire l'ID de la requête
        query_id_match = re.search(r'(\d+).Query:', query)
        if query_id_match:
            query_id = query_id_match.group(1)
            # Extraire la requête SPARQL
            sparql_query_match = re.search(r'SELECT.*?\}', query, re.DOTALL)
            if sparql_query_match:
                sparql_query = sparql_query_match.group(0)
                print(sparql_query)
                filename = f'Q-{query_id}.sparql'
                with open('test/'+filename, 'w') as output_file:
                    output_file.write(sparql_query.strip() + "\n")

print("Les fichiers de requêtes SPARQL ont été générés.")