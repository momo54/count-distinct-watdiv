import rdflib

# Create a Graph
g = rdflib.Graph()

# Parse the N-Triples file
file_path = 'path_to_your_file.nt'  # Make sure to replace this with the path to your .nt file
g.parse("./watdiv.10M.nt", format='nt')

# Définir la requête SPARQL
query = """
SELECT ?predicate (COUNT(?object) AS ?co) (COUNT(DISTINCT ?object) AS ?dco) 
WHERE {
  ?sujet ?predicate ?object.
}
GROUP BY ?predicate
ORDER BY DESC(?co)
"""

# Exécuter la requête
for row in g.query(query):
    print(f"p: {row.predicate}, co: {row.co}, co: {row.dco}")
    


