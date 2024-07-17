import rdflib

# Create a Graph
g = rdflib.Graph()

# Parse the N-Triples file
file_path = 'path_to_your_file.nt'  # Make sure to replace this with the path to your .nt file
g.parse("./watdiv.10M.nt", format='nt')

# Définir la requête SPARQL
query = """
SELECT ?sujet (COUNT(?sujet) AS ?nombreOccurrences)
WHERE {
  ?sujet ?predicate ?object.
}
GROUP BY ?sujet
ORDER BY DESC(?nombreOccurrences)
LIMIT 1
"""

# Exécuter la requête
for row in g.query(query):
    print(f"Sujet le plus fréquent: {row.sujet}, Nombre d'occurrences: {row.nombreOccurrences}")
    


