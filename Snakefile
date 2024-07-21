##
# the main objective is to generate count-distinct queries from the original watdiv queries
# 1 - select top 5 count(*) queries per nbtp from the original watdiv queries
# 2 - generate top 5 count-distinct queries per nbtp from the top 5 count(*) queries
# results should be in the queries/top5_cd_original directory
# main commands:
# /opt/homebrew/bin/snakemake queries/top5_count_original/generated.mark (generate top 5 count(*) queries
# /opt/homebrew/bin/snakemake  (evaluate all possible count-distinct queries with distinct frequencies)
# /opt/homebrew/bin/snakemake queries/top5_cd_original/generated.mark (generate top 5 count-distinct queries)

import yaml
import glob
import sys
import os
import csv

def list_files(path):
    if not os.path.isdir(path):
        return glob.glob(path)
    files = list()
    for filename in os.listdir(path):
        print(f"filename: {filename}")
        if filename.endswith(".sparql") and not filename.startswith("Q-10069"):
#        if filename.endswith(".sparql") :
            files.append(f"{path}/{filename}")
    return files


def load_queries(path):
    print(f"load_queries: {path}")
    queries = list()
    for file in list_files(path):
        with open(file, 'r') as reader:
            filename = os.path.basename(file).split('.')[0]
            query = reader.read()
            queries.append((filename, query))
    return queries

def run_files(wcs):
    files = []
    output = "output" if "output" not in config else config["output"]
#    for dir in ["cd_watdiv","top5_nbtp_original_watdiv"]:
    for dir in ["top5_nbtp_original_watdiv"]:
        if not os.path.exists(f"{output}/{dir}"):
            os.makedirs(f"{output}/{dir}")
        for filename, query in load_queries(f"queries/{dir}"):
            files.append((f"{output}/{dir}/{filename}.csv"))
    print(f"run_files: {files}")
    return files


rule run_all:
    input: ancient(run_files) 

rule run_query:
    input:
        query = ancient("queries/{dir}/{query}.sparql")
    output:
        metrics = "{output}/{dir}/{query}.csv"
    shell:
        "python scripts/sparql_rewrite.py  {input.query}  > {output.metrics}"

rule check_python:
    shell:
        "which python; python -V"

def list_files_in_directory(wildcards):
    print(f"wildcards: {wildcards}")
    return glob(os.path.join(wildcards.dir, "*"))

from glob import glob
rule collect_original:
    input:
        expand("{csv}",csv=glob("output/top5_nbtp_original_watdiv/*.csv"))
    output:
        final="{output}/original_final.csv"
    run:
        print("Collecting data")
        with open(output[0], 'w') as outfile:
            outfile.write("query, nbtp,count,countime,var,dv,df,timedv,timedf\n")
            for path in input:
                with open(path) as infile:
                    for line in infile:
                        outfile.write(line)
        import pandas as pd
        df = pd.read_csv(output[0])
        df.sort_values(by='dv', ascending=False,inplace=True)
        df.to_csv(output[0], index=False)

rule top_5_cdcount_per_tp:
    input:
        "output/original_final.csv"
    output:
        "output/original_final_top5.csv"
    shell:
        "python scripts/sort_per_tp_cd.py {input} > {output}"

rule generate_cd_queries:
    input:
        file="output/original_final_top5.csv",
        src="queries/top5_nbtp_original_watdiv"
    output:
        "queries/top5_cd_original/generated.mark"
    run:
        output_dir = os.path.dirname(output[0])
        shell_cmd = f"python scripts/generate_cd_queries.py {input.file} {input.src} {output_dir}"
        
        # Exécuter la commande shell
        shell(shell_cmd)
        
        # Créer le fichier de sortie pour marquer la fin de la tâche
        shell(f"touch {output[0]}")

## carefull: very long 12400 queries to test (blazegraph have to run)
## maybe easy to parallelize if needed. many time-out
rule search_in_original_watdiv:
    input:
        dir="queries/original_watdiv/",
        endpoint="http://localhost:9999/blazegraph/sparql",
        timeout="30"
    output:
        "output/original_watdiv_tp_count.csv"
    shell:
        "python scripts/search_in_watdiv.py {input.dir} > {output}"

rule top5_count_per_tp:
    input:
        "output/original_watdiv_tp_count.csv"
    output:
        "output/top5_original_watdiv_tp_count.csv"
    shell:
        "python scripts/sort_per_tp_count.py {input} > {output}"

rule generate_top_count_queries:
    input:
        file="output/top5_original_watdiv_tp_count.csv",
        src="queries/original_watdiv"
    output:
        "queries/top5_count_original/generated.mark"
    run:
        output_dir = os.path.dirname(output[0])
        shell_cmd = f"python scripts/copy_in_the_list.py {input.file} {input.src} {output_dir}"
        
        # Exécuter la commande shell
        shell(shell_cmd)
        
        # Créer le fichier de sortie pour marquer la fin de la tâche
        shell(f"touch {output[0]}") 