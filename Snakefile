import yaml
import glob
import sys
import os
import csv



def list_files(path):
    print(f"list_files: {path}")
    if not os.path.isdir(path):
        return glob.glob(path)
    files = list()
    for filename in os.listdir(path):
#        if filename.endswith(".sparql") and not filename.startswith("Q-10069"):
        if filename.endswith(".sparql") :
            files.append(f"{path}/{filename}")
    return files


def load_queries(path):
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
    for filename, query in load_queries("queries/cd_watdiv"):
        files.append((f"{output}/cd_queries/{filename}.csv"))
    print(f"run_files: {files}")
    return files


rule run_all:
    input: ancient(run_files) 

rule run_query:
    input:
        query = ancient("queries/cd_watdiv/{query}.sparql")
    output:
        metrics = "{output}/cd_queries/{query}.csv"
    shell:
        "python scripts/sparql_rewrite.py  {input.query}  > {output.metrics}"

rule check_python:
    shell:
        "which python; python -V"

rule collect_all:
    input: 
        data=ancient(run_files) 
    output: 
        final="{output}/final.csv"
    run:
        print("Collecting data")
        with open(output[0], 'w') as outfile:
            for path in input.data:
                with open(path) as infile:
                    for line in infile:
                        outfile.write(line)

rule collect_and_sort:
    input: 
        data=ancient(run_files) 
    output: 
        final="{output}/final2.csv"
    run:
        import pandas as pd

        print("Collecting data")
        dataframes = []

        # Read each CSV file and append to the list
        for file in input.data:
            df = pd.read_csv(file,sep=' ')
            dataframes.append(df)

        # Concatenate all dataframes
        combined_df = pd.concat(dataframes)
        combined_df.sort_values(by=combined_df.columns[3], inplace=True)
        combined_df.to_csv(output.final, index=False)

        # Write the combined dataframe to a new CSV file
        combined_df.to_csv('combined.csv', index=False)
