import requests

def execute_sparql_query(query):
    url = "https://query.wikidata.org/sparql"
    headers = {
        "Accept": "application/sparql-results+json"
    }
    response = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"SPARQL query failed with status code {response.status_code}")

def test_queries(queries):
    results = []
    for query in queries:
        try:
            result = execute_sparql_query(query)
            results.append(result)
        except Exception as e:
            print(f"Query failed: {e}")
            results.append(None)
    return results

def build_query(type_id):
    return f"""
    SELECT (count(distinct ?o) as ?co)
    WHERE {{
      ?s wdt:P31 <{type_id}> .
      ?s ?p ?o
    }}
    """

def build_type():
    type_query="""
    SELECT distinct ?type 
    WHERE {
    ?s wdt:P31 ?type .
    }"""


    type_list = []
    try:
        results=execute_sparql_query(type_query)

        for result in results['results']['bindings']:
            type_id = result['type']['value']
            type_list.append((type_id))
        
    except Exception as e:
        print(f"Query {type_query} failed: {e}")
    print(len(type_list))
    print(type_list)
    return type_list


# Liste des IDs de types à tester (par exemple, Q5 pour "être humain", Q146 pour "chat")
type_ids = ["Q5", "Q146", "Q11424"]


type_ids=build_type()

# # Construire les requêtes pour chaque type
queries = [build_query(type_id) for type_id in type_ids[:10]]

# # Exécuter les requêtes et obtenir les résultats
results = test_queries(queries)

# # Afficher les résultats
for i, result in enumerate(results):
    if result:
        count = result['results']['bindings'][0]['co']['value']
        print(f"Results for type ID {type_ids[i]}: {count}")
    else:
        print(f"No results for type ID {type_ids[i]}")
