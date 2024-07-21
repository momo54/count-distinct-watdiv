import os
import time
from SPARQLWrapper import SPARQLWrapper, JSON
from sparql_rewrite import rewrite_count,get_nbtp
import sys

# Fonction pour lire le contenu d'un fichier
def read_query_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

# Fonction pour exécuter une requête avec timeout
def execute_query(endpoint_url, query, timeout=30):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(timeout)

    try:
        result = sparql.query().convert()
        return result
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return None


def search_watdiv(queries_directory,endpoint_url="http://localhost:9999/bigdata/sparql"):
    # Chemin du répertoire contenant les fichiers de requêtes

    # URL de l'endpoint SPARQL
    endpoint_url = endpoint_url

    # Lister les fichiers de requêtes dans le répertoire
    query_files = [os.path.join(queries_directory, f) for f in os.listdir(queries_directory) if f.endswith('.sparql')]

    # Exécution des requêtes avec timeout
    results = []
    for i, query_file in enumerate(query_files):
        query = read_query_file(query_file)
        query_count= rewrite_count(query)
        nbtp=get_nbtp(query_count)
        print(f"Executing : {query_file} {i}/{len(query_files)}",file=sys.stderr)
        result = execute_query(endpoint_url, query_count, timeout=30)
        if result:
            value=result['results']['bindings'][0]['count']['value']
            print(f" {query_file}, {nbtp},  {value}")
            #results.append(result)
        #time.sleep(1)  # Pause d'une seconde entre les requêtes pour éviter de surcharger l'endpoint

    # Affichage des résultats
    #for i, result in enumerate(results):
    #    print(f"Result {i + 1}: {result}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <dir of queries>")
    else:
        file_path = sys.argv[1]
        search_watdiv(file_path)
