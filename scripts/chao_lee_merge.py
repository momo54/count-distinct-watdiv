import csv
import os
import re


def chaolee_parse_result(result_file):
    path_parts = result_file.split(os.path.sep)
    config_dir = path_parts[-2]
    config = int(config_dir.replace("config", ""))
    query_name = path_parts[-1].split('.')[0]

    results=[]
    with open(result_file, 'r') as result_file:
        contents = result_file.read()
        block_pattern = re.compile(r"\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - BigN SampleSize: \d+\.\d+\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - ChaoLee SampleSize: \d+\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - Nb Total Scans: \d+\n\{.+\nExecution time:\s+\d+ ms\nNumber of Results:\s+\d+")
        blocks = re.findall(block_pattern, contents)
        run_data_blocks = blocks[:5]
        #print(run_data_blocks)
        for run_number, run_data_block in enumerate(run_data_blocks, 1):
            run_data = run_data_block.strip()
            #print(run_data)
            BigN_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - BigN SampleSize: (\d+\.?\d*)',run_data).group(1)
            CHAOLEE_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - ChaoLee SampleSize: (\d+\.?\d*)',run_data).group(1)
            #Sum_F_mu_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - ∑Fµ SampleSize: (\d+\.?\d*)',run_data).group(1)
            #Sum_F_mu_success = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - ∑Fµ success: (\d+\.?\d*)',run_data).group(1)
            #Sum_F_mu_fail = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - ∑Fµ fail: (\d+\.?\d*)',run_data).group(1)
            #N_hat = re.search( r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - N̂:\s*(\d+\.\d+([eE][+-]?\d+)?)',run_data).group(1)
            Nb_Total_Scans = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctChaoLee - Nb Total Scans: (\d+\.?\d*)',run_data).group(1)
            Execution_time = re.search(r"Execution time:\s*(\d+) ms", run_data).group(1).strip()
            Result_cd = re.search(r"{\?.+->\s*\"(.*?)\"\^\^.*", run_data).group(1).strip()


            result=[query_name,config, run_number,
                float(BigN_SampleSize), float(CHAOLEE_SampleSize), 
                Nb_Total_Scans, Execution_time,round(float(Result_cd[1:]))]   
            results_str = [str(element) for element in result]
            results.append(",".join(results_str))
        return results



def chaolee_merge_results(base_dir):

    print(",".join([
             'query_name','Config', 'Run',
            'BigN_SampleSize', 'CHAOLEE_SampleSize', 'Nb_Total_Scans', 'Execution_time', 'cd'
        ]))

    for config in range(1, 10):
        config_dir = f"config{config}"
        path = os.path.join(base_dir,  config_dir)
        for filename in os.listdir(path):
            if filename.endswith(".result"):
                query_file = os.path.join(path, filename)
                query_name = filename.split('_')[1].split('.')[0]
                print("\n".join(chaolee_parse_result(query_file)))


if __name__ == "__main__":
    # python scripts/chao_lee_merge.py > output/chao.csv 
    ROOT="/GDD/count-distinct-watdiv"
    chaolee_merge_results(f"{ROOT}/output/CHAOLEE")
