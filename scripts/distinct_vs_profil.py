import rdflib

# Create a Graph
g = rdflib.Graph()

# Parse the N-Triples file
file_path = 'path_to_your_file.nt'  # Make sure to replace this with the path to your .nt file
g.parse("./watdiv.10M.nt", format='nt')

# distincts
query_d = """
SELECT (COUNT(distinct ?s) AS ?ds) (COUNT(distinct ?p) AS ?dp) (COUNT(distinct ?o) AS ?do) 
WHERE {
  ?s ?p ?o.
}
"""

##
## Watdiv Profiles
##
query_s = """
select ?ds (count(distinct ?s) as ?dds) {
  select ?s (count(?s) as ?ds) where {
   select * { ?s ?p ?o }
  } group by ?s
} group by ?ds order by ?ds
"""

query_p = """
select ?dp (count(distinct ?p) as ?ddp) {
  select ?p (count(?p) as ?dp) where {
   select * { ?s ?p ?o }
  } group by ?p
} group by ?dp order by ?dp
"""

query_o = """
select ?do (count(distinct ?o) as ?ddo) {
  select ?o (count(?o) as ?do) where {
   select * { ?s ?p ?o }
  } group by ?o
} group by ?do order by ?do
"""

queries={"distincts":query_d,
         "subject":query_s,
         "predicat":query_p,
         "object":query_o
         }

for k,v in queries.items():
    print(f"executing:{k}")
    
    # Exécuter la requête
    i=0
    for row in g.query(v):
        i+=1
        print(f"{row}")
    print(f"nb solutions:{i}")
    



