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
import pandas as pd
import time

from sparql_rewrite import CDVisitor


def gen_query(var,query_name,query_dir):
    with open(query_dir+"/"+query_name) as f:
        query_str = f.read()
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)

    cdvisitor = CDVisitor('?'+var)
    cdvisitor.visit(algebra.algebra)
    result="".join(cdvisitor.my_query)
    print(f"Generated query: {result}")
    query_name = query_name.split('.')[0]
    with open("output/selected_queries/"+query_name.split('.')[0]+"_"+var+".sparql", "w") as f:
        f.write(result)

def generate_watdiv(path,query_dir):
    df = pd.read_csv(path)
    df.sort_values(by='dv', ascending=False,inplace=True)
    for index, row in df.head(30).iterrows():
        var = row['var']
        query_name = row['query']

        gen_query(var,query_name,query_dir)
        # Your code here to process var and query_name

if __name__ == "__main__":
    generate_watdiv("output/final.csv","queries/cd_watdiv")
