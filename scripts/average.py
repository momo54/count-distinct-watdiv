import rdflib

# Charger le graphe
g = rdflib.Graph()
g.parse("./watdiv.10M.nt", format="nt")

# Requête pour le total des occurrences de sujets
query_total_occurrences = """
SELECT (COUNT(?sujet) AS ?totalOccurrences)
WHERE {
  ?sujet ?predicate ?object.
}
"""

# Requête pour le nombre de sujets uniques
query_sujets_uniques = """
SELECT (COUNT(DISTINCT ?sujet) AS ?nombreSujetsUniques)
WHERE {
  ?sujet ?predicate ?object.
}
"""

# Exécuter les requêtes et obtenir les résultats comme des entiers
total_occurrences_result = g.query(query_total_occurrences)
total_occurrences = sum(int(row.totalOccurrences) for row in total_occurrences_result)

nombre_sujets_uniques_result = g.query(query_sujets_uniques)
nombre_sujets_uniques = sum(int(row.nombreSujetsUniques) for row in nombre_sujets_uniques_result)

# Calculer la moyenne (en s'assurant que le dénominateur n'est pas zéro)
moyenne = (total_occurrences / nombre_sujets_uniques) if nombre_sujets_uniques > 0 else 0
print(f"Nombre moyen d'occurrences par sujet : {moyenne}")
