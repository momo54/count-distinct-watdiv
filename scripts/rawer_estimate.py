import subprocess
from  crawd_merge import crawd_parse_results

from sparql_rewrite import rewrite_countdistinct,get_nbtp

import re
import os
import sys
import requests
import time



def crawd_parse_results(content):

    result={}
  
#    print(f"CRAWD parse:({content})")
    formatted_content = content.replace('\\n', '\n')
#    print(f"formatted:({formatted_content})")

    block_pattern = r"\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\{.+\nExecution time:.+\nNumber of Results:.+\n"
    blocks = re.findall(block_pattern, formatted_content)
    run_data_blocks = blocks[:5]

#    print(f"run_data_blocks: {run_data_blocks}")    

    run_data = run_data_blocks[0]
#    #print(run_data)
    WJ_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - WJ SampleSize: (\d+\.?\d*)',run_data).group(1)
    CRAWD_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - CRAWD SampleSize: (\d+\.?\d*)',run_data).group(1)
    Sum_F_mu_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - ∑Fµ SampleSize: (\d+\.?\d*)',run_data).group(1)
    Sum_F_mu_success = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - ∑Fµ success: (\d+\.?\d*)',run_data).group(1)
    Sum_F_mu_fail = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - ∑Fµ fail: (\d+\.?\d*)',run_data).group(1)
    N_hat = re.search( r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - N̂:\s*(\d+\.\d+([eE][+-]?\d+)?)',run_data).group(1)
    Nb_Total_Scans = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - Nb Total Scans: (\d+\.?\d*)',run_data).group(1)
    Execution_time = re.search(r"Execution time:\s*(\d+) ms", run_data).group(1).strip()
    Result_cd = re.search(r"{\?.+->\s*\"(.*?)\"\^\^.*", run_data).group(1).strip()

    result['WJ_SampleSize']= float(WJ_SampleSize)
    result['CRAWD_SampleSize']= float(CRAWD_SampleSize), 
    result['Sum_F_mu_SampleSize']= float(Sum_F_mu_SampleSize)
    result['Sum_F_mu_success']= float(Sum_F_mu_success)
    result['Sum_F_mu_fail']= float(Sum_F_mu_fail)
    result['N_hat']= N_hat 
    result['Nb_Total_Scans']= Nb_Total_Scans 
    result['Execution_time']= Execution_time 
    result['Result_cd']= round(float(Result_cd[1:]))
    return result


def rawer_estimate(rawer_dir, jnl, query, limit=10000, sublimit=100, nbthreads=1):
    cmd = [
        "mvn", "exec:java", "-pl", "rawer",
        "-Dexec.args=\"--database={jnl} --query=\'{query}\' --limit={limit} -sl={sublimit} --threads={nbthreads} --report\""
    ]

    # Remplacer les placeholders par les vraies valeurs
    cmd_str = " ".join(cmd).format(
        jnl=jnl,
        query=query,
        limit=limit,
        sublimit=sublimit,
        nbthreads=nbthreads
    )

 #   print(f"Executing command: {cmd_str}")

     # Exécuter la commande
    try:
        result = subprocess.run(cmd_str+ " 2>&1", 
                            shell=True, 
                            capture_output=True, 
                            text=True,
                            timeout=60,
                            cwd=rawer_dir)
    
    
        # Vérifier le code de retour
        if result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return None
        else:
            crawd=crawd_parse_results(result.stdout)
            return crawd
    except subprocess.TimeoutExpired:
        print(f"{cmd_str} Command timed out",sys.stderr)
        return None

def search_for_interesting_cd(query_path, rawer_dir, jnl, limit, sublimit):
    with open(query_path) as f:
        query_str = f.read()
    nbtp=get_nbtp(query_str)
    queries_str = rewrite_countdistinct(query_str)
    for var,q_str in queries_str.items():
        result = rawer_estimate(rawer_dir, jnl, q_str, limit, sublimit,  nbthreads=1)
        print(f"Result: {result}", file=sys.stderr)
        if result is not None:
            print(f"{query_path},{nbtp}, {var}, {result['Result_cd']}, {result['N_hat']}")
        else:
            print(f"{query_path},{nbtp}, {var}, None, None")

def search_for_interesting_cd_with_bg(query_path):
    with open(query_path) as f:
        query_str = f.read()
    nbtp=get_nbtp(query_str)
    queries_str = rewrite_countdistinct(query_str)
    for var,q_str in queries_str.items():
        result = rawer_estimate(rawer_dir, jnl, q_str, limit, sublimit,  nbthreads=1)
        print(f"Result: {result}", file=sys.stderr)
        if result is not None:
            print(f"{query_path},{nbtp}, {var}, {result['Result_cd']}, {result['N_hat']}")
        else:
            print(f"{query_path},{nbtp}, {var}, None, None")



if __name__ == "__main__":
        ROOT= "/Users/molli-p/count-distinct-watdiv"
        rawer_dir = f"{ROOT}/sage-jena"
        query = f"{ROOT}/queries/cd_watdiv/C6_role1.sparql"
        limit = 10000
        sublimit = 100
        jnl = f"{ROOT}/data/blazegraph.jnl"
        nbthreads = 4

        query_dir = f"{ROOT}/queries/watdiv_with_sage_plan"
        entries = os.listdir(query_dir)

        # Filtre pour obtenir seulement les fichiers
        files = [os.path.join(query_dir, file) for file in entries if os.path.isfile(os.path.join(query_dir, file))]

        print(f"query_path,nbtp, var, cd, N")
        i=0
        for query_path in files:
            i=i+1
            print(f"Processing query: {query_path}, {i}/{len(files)}", file=sys.stderr)
            search_for_interesting_cd(query_path, rawer_dir, jnl, limit, sublimit)

       
