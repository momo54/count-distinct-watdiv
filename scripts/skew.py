import rdflib

# Create a Graph
g = rdflib.Graph()

# Parse the N-Triples file
file_path = 'path_to_your_file.nt'  # Make sure to replace this with the path to your .nt file
g.parse("./watdiv.10M.nt", format='nt')

# Définir la requête SPARQL
query_s = """
SELECT (COUNT(*) AS ?f)
WHERE {
  ?s ?p ?o.
}
GROUP BY ?s
ORDER BY ?f
"""

query_p = """
SELECT (COUNT(*) AS ?f)
WHERE {
  ?s ?p ?o.
}
GROUP BY ?p
ORDER BY ?f
"""

query_o = """
SELECT (COUNT(*) AS ?f)
WHERE {
  ?s ?p ?o.
}
GROUP BY ?o
ORDER BY ?f
"""

queries={"subject_freq.txt":query_s,
         "predicat_freq.txt":query_p,
         "object_freq.txt":query_o
         }

for k,v in queries.items():
    print(f"executing:{k}")
    with open(k, "w") as file:
        # Exécuter la requête
        i=0
        for row in g.query(v):
            i+=1
            file.write(f"{row.f}\n")
        print(f"nb solutions:{i}")

    


