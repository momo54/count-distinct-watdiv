from rdflib.plugins.sparql.parser import parseQuery
from rdflib.plugins.sparql.algebra import translateQuery
from rdflib.plugins.sparql.sparql import Bindings, QueryContext
from rdflib.plugins.sparql.parserutils import Expr
from rdflib.term import Identifier, Variable, URIRef
from rdflib.plugins.sparql.algebra import CompValue
from rdflib.util import from_n3
from rdflib.plugins.sparql.algebra import pprintAlgebra
import pprint
import requests

import click
import os
import csv
import sys
import logging
import colorlog

# a visitor pattern for RDFLIB for rewriting queries
# wdbench query 151
#query_str='''select * where {?x1 <http://www.wikidata.org/prop/direct/P106> ?x2 . ?x2 <http://www.wikidata.org/prop/direct/P31> ?x3 . ?x1 <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q5> . }
#'''

query_str='''
SELECT (COUNT(*) as ?count) WHERE {
	?v1 <http://schema.org/priceValidUntil> ?v8.
	?v1 <http://purl.org/goodrelations/validFrom> ?v2.
	?v1 <http://purl.org/goodrelations/validThrough> ?v3.
	?v1 <http://schema.org/eligibleQuantity> ?v6.
	?v0 <http://purl.org/goodrelations/offers> ?v1.
	?v1 <http://schema.org/eligibleRegion> ?v7.
	?v4 <http://schema.org/nationality> ?v7.
	?v4 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://db.uwaterloo.ca/~galuc/wsdbm/Role2>.
}
'''


def execute_sparql_query(query):
#    url = "https://query.wikidata.org/sparql"
    url="http://localhost:9999/bigdata/sparql"
    headers = {
        "Accept": "application/sparql-results+json"
    }
    response = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"SPARQL query failed with status code {response.status_code}")


class Visitor:

    my_query = []
    nbtriples=0

    def __init__(self):
        self.my_query = []
        self.nbtriples=0


    def visit(self, algebra):
        # Determine the type of the node and visit it
        method_name = 'visit_' + type(algebra).__name__
        if hasattr(algebra, 'name'):
            method_name = 'visit_' + algebra.name
        #print(f"try visiting method_name: {method_name}")
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(algebra)

    def generic_visit(self, algebra):
        # Handle generic visiting logic
        #print(f"Visiting {type(algebra).__name__}")
#        print(f"Visiting {algebra.name}")

        if isinstance(algebra, CompValue):
            #print(f"comp value: {algebra.items()}")
            for key, value in algebra.items():
                if isinstance(value, list):
                    for item in value:
                        self.visit(item)
                elif isinstance(value, CompValue):
                    self.visit(value)
        elif isinstance(algebra, list):
            print(f"list: {algebra}")
            for item in algebra:
                self.visit(item)

    def visit_Project(self, project):
        #print("Visiting Project:", project)
        self.my_query.append("select * WHERE {\n")
        self.visit(project.p)
        self.my_query.append("}")

    def visit_OrderBy(self, order_by):
        # print("Visiting OrderBy:", order_by)
        self.visit(order_by.p)

    def visit_Extend(self, node):
        # print("Visiting Extend:", node)
        self.visit(node.p)

    def visit_LeftJoin(self, node):
        # print("Visiting LeftJoin:", node)
        self.visit(node.p1)
        self.my_query.append("  OPTIONAL {")   
        self.visit(node.p2)
        self.my_query.append(" }")       

    # Example specific visit method
    def visit_BGP(self, node):
        # print("Visiting BGP:", node)
        self.nbtriples+=len(node.triples)
        triples = "".join(
                    triple[0].n3() + " " + triple[1].n3() + " " + triple[2].n3() + " . \n"
                    for triple in node.triples
                )
        self.my_query.append(triples) 

    # Add more methods for other specific types of nodes

## redefine the visitor to count the number of triples in the query
class  CountVisitor(Visitor):
   def visit_Project(self, project):
        #print("Visiting Project:", project)
        self.my_query.append("select (COUNT(*) as ?count) WHERE {\n")
        self.visit(project.p)
        self.my_query.append("}")

class  CDVisitor(Visitor):
   def visit_Project(self, project):
        #print("Visiting Project:", project)
        vars=project.PV
        self.my_query.append("select (COUNT(DISTINCT %s) as ?cd) WHERE {\n"%(vars[0].n3()))
        self.visit(project.p)
        self.my_query.append("}")

class  BGPVisitor(Visitor):
    bgp_vars=None
    def visit_BGP(self, node):
        self.bgp_vars=node._vars
        super().visit_BGP(node)

class  FreqVisitor(Visitor):
    var=""
    def __init__(self, param):
        self.var = param
        self.my_query = []
    
    def visit_Project(self, project):
        self.my_query.append("select (count (distinct ?freq) as ?dfreq) {\n");    
        self.my_query.append(" select %s (count(%s) as ?freq) WHERE {\n "%(self.var,self.var))
        self.visit(project.p)
        self.my_query.append(" } group by %s \n} \n"%(self.var))

class  MCDVisitor(Visitor):
    var=""
    def __init__(self, param):
        self.var = param
        self.my_query = []
    
    def visit_Project(self, project):
        self.my_query.append("select ");
        for var in self.var:
            self.my_query.append(" (count(distinct %s) as ?cd%s) \n"%(var.n3(),str(var)))    
        self.my_query.append("  WHERE {\n ")
        self.visit(project.p)
        self.my_query.append(" }\n")


def rewrite_count(query_str):
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
#    print(pprintAlgebra(algebra))

    visitor = CountVisitor()
    visitor.visit(algebra.algebra)
#    print(f"nbtriples in query:{visitor.nbtriples}")
    result="".join(visitor.my_query)
    return result

def get_nbtp(query_str):
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
    visitor = Visitor()
    visitor.visit(algebra.algebra)
    return visitor.nbtriples

def rewrite_mcd(query_str):
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
#    print(pprintAlgebra(algebra))

    bgp_visitor = BGPVisitor()
    bgp_visitor.visit(algebra.algebra)

    mcd_visitor = MCDVisitor(bgp_visitor.bgp_vars)
    mcd_visitor.visit(algebra.algebra)
    result="".join(mcd_visitor.my_query)

    return result


def rewrite_freq(query_str):
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
#    print(pprintAlgebra(algebra))

    bgp_visitor = BGPVisitor()
    bgp_visitor.visit(algebra.algebra)

    # print(f"vars in query:{bgp_visitor.bgp_vars}")

    queries={}
    for var in bgp_visitor.bgp_vars:
        fvisitor = FreqVisitor(var.n3())
        fvisitor.visit(algebra.algebra)
        result="".join(fvisitor.my_query)
        queries[var.n3()]=result

    return queries



@click.command()
@click.argument("query", type=click.Path(exists=True))
@click.option("--select", type=click.Choice(["count", "cd","freq"]),
    default="count", show_default=True,
    help="select count or count distinct with random projected variable")
@click.option("--verbose", is_flag=True,
    help="display the algebra of the query")
@click.option('--output', is_flag=True, help='rewrite query in a file prefixed by the number of tp in query.')
def rewrite_query(query,select,verbose,output):

    # Create a logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Create a formatter with color
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%(name)s:%(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)


    # output is dictinary with count, cd, freq...
    result={}

    with open(query) as f:
        query_str = f.read()
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
    if verbose:
        print(pprintAlgebra(algebra))

    result['query']=os.path.basename(query)

    result['nbtp']=get_nbtp(query_str)

    count_query=rewrite_count(query_str)
    logger.debug(f"executing {result['query']}:{count_query}")
    count=execute_sparql_query(count_query)
    result['count']=count['results']['bindings'][0]['count']['value']

    rewrite_query_str=rewrite_mcd(query_str)
    logger.debug(f"executing {result['query']}:{rewrite_query_str}")
    mcd=execute_sparql_query(rewrite_query_str)
    for key,info in mcd['results']['bindings'][0].items():
        result[key]=info['value']

    freq_queries=rewrite_freq(query_str)
    for var,query in freq_queries.items(): 
        logger.debug(f"executing {result['query']}:{query}")
        data=execute_sparql_query(query)
        result['freq'+var]=data['results']['bindings'][0]['dfreq']['value']
#        print(f"var:{var}, freq:{data['results']['bindings'][0]['dfreq']['value']}")    

    print(result)
#    filednames=result[0].keys()
#    writer = csv.DictWriter(sys.stdout, fieldnames=result.keys())
#    writer.writeheader()
#    writer.writerows(result)
#    print(result)


if __name__ == "__main__":

#    count_query=rewrite_count(query_str)
#    print(f"count query:{count_query}")
#    count=execute_sparql_query(count_query)
#    print(count['results']['bindings'][0]['count']['value'])

#    queries=rewrite_freq(query_str)
#    print(queries)
#    for var,query in queries.items():
#        data=execute_sparql_query(query)
#        print(f"var:{var}, freq:{data['results']['bindings'][0]['dfreq']['value']}")

    #print(rewrite_mcd(query_str))
    #print(execute_sparql_query(rewrite_mcd(query_str)))

#    mcd=execute_sparql_query(rewrite_mcd(query_str))
#    print(mcd)
#    for key,info in mcd['results']['bindings'][0].items():
#        print(key,info['value'])

#    freq_queries=rewrite_freq(query_str)
#    for f in freq_queries:
#        freq=execute_sparql_query(f)
#        for key,info in freq['results']['bindings'][0].items():
#            print(key,info['value'])

    #print(execute_sparql_query("select (count(*) as ?count) {?s ?p ?o} limit 10"))
    rewrite_query()


