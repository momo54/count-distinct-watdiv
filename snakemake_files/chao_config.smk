import os
from glob import glob
from snakemake.utils import validate
from snakemake.shell import shell
import json

import rdflib

## cannot work
from scripts.sparql_rewrite import get_nbtp

# Directory for input SPARQL files
ROOT="/Users/molli-p/count-distinct-watdiv"
QUERY_DIR = f"{ROOT}/queries/top5_cd_original"
QUERY_FILES = [os.path.splitext(f)[0] for f in os.listdir(QUERY_DIR) if f.endswith(".sparql")]
RESULT_DIR = f"{ROOT}/output/CHAOLEE-original"

# Not sure what it does...
#include: "../scripts/sparql_rewrite.py" 

with open(f"{ROOT}/config-exp.json") as f1:
    CONFIG = json.load(f1)

rule all:
    input:
        expand(
            f"{RESULT_DIR}/{{config}}/{{query}}.result",
            config=CONFIG.keys(),
            query=QUERY_FILES
        )

rule prepare_result_directories:
    output:
        [f"{RESULT_DIR}/{config_name}" for config_name in CONFIG.keys()]
    run:
        for config_name in CONFIG.keys():
            os.makedirs(f"{RESULT_DIR}/{config_name}", exist_ok=True)


rule run_sparql_query:
    input:
        query_file=f"{QUERY_DIR}/{{query}}.sparql",
        config_file=f"{ROOT}/config-exp.json"
    output:
        f"{RESULT_DIR}/{{config}}/{{query}}.result"
    run:
        with open(input.config_file) as f:
            config = json.load(f)
        limit = config[wildcards.config]["limit"]
        with open(input.query_file) as qfile:
            query_str = qfile.read()
        tp=get_nbtp(query_str)
        sl = tp * config[wildcards.config]["sl"]
        print(f"Running query {wildcards.query} with limit {limit} and sl {sl}" )
        result_dir = f"{RESULT_DIR}/{wildcards.config}"

        # shell("""
        #     cd {ROOT}/sage-jena
        #     echo $(pwd)  > {output}
        #     """)

        shell_cmd = f"""
            cd {ROOT}/sage-jena
            mvn exec:java -pl rawer -Dexec.args=" --database={ROOT}/data/blazegraph.jnl --file={input.query_file} --limit={limit} --chao-lee -sl={sl} --threads=1 -n=5 --report" &>  {output}
           """

        shell(shell_cmd)




