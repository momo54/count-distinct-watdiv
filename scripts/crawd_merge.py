import csv
import os
import re



def crawd_parse_results(result_file):
        path_parts = result_file.split(os.path.sep)
        config_dir = path_parts[-2]
        config = int(config_dir.replace("config", ""))
        query_name = path_parts[-1].split('.')[0]
#        print(f"Processing {result_file}")

        with open(result_file, 'r') as result_file:
            contents = result_file.read()
            block_pattern = r"\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - (?:WJ SampleSize|CRAWD SampleSize|∑Fµ SampleSize|∑Fµ success|∑Fµ fail|N̂|Nb Total Scans): .+?\n\{.+\nExecution time:.+\nNumber of Results:.+\n"
            blocks = re.findall(block_pattern, contents)
            run_data_blocks = blocks[:5]

            for run_number, run_data_block in enumerate(run_data_blocks, 1):
                run_data = run_data_block.strip()
                #print(run_data)
                WJ_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - WJ SampleSize: (\d+\.?\d*)',run_data).group(1)
                CRAWD_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - CRAWD SampleSize: (\d+\.?\d*)',run_data).group(1)
                Sum_F_mu_SampleSize = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - ∑Fµ SampleSize: (\d+\.?\d*)',run_data).group(1)
                Sum_F_mu_success = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - ∑Fµ success: (\d+\.?\d*)',run_data).group(1)
                Sum_F_mu_fail = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - ∑Fµ fail: (\d+\.?\d*)',run_data).group(1)
                N_hat = re.search( r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - N̂:\s*(\d+\.\d+([eE][+-]?\d+)?)',run_data).group(1)
                Nb_Total_Scans = re.search(r'\[fr\.gdd\.sage\.rawer\.cli\.RawerCLI\.main\(\)\] DEBUG CountDistinctCRAWD - Nb Total Scans: (\d+\.?\d*)',run_data).group(1)
                Execution_time = re.search(r"Execution time:\s*(\d+) ms", run_data).group(1).strip()
#                print(f"run_data: {run_data}")
                Result_cd = re.search(r"{\?.+->\s*\"(.*?)\"\^\^.*", run_data).group(1).strip()
#                writer.writerow([
#                    query_name,config, run_number,
#                    float(WJ_SampleSize), float(CRAWD_SampleSize), float(Sum_F_mu_SampleSize), float(Sum_F_mu_success), float(Sum_F_mu_fail),
#                    N_hat, Nb_Total_Scans, Execution_time,round(float(Result_cd[1:]))
#                ])

                result=[query_name,config, run_number,
                    float(WJ_SampleSize), float(CRAWD_SampleSize), float(Sum_F_mu_SampleSize), float(Sum_F_mu_success), float(Sum_F_mu_fail),
                    N_hat, Nb_Total_Scans, Execution_time,round(float(Result_cd[1:]))]
                results_str = [str(element) for element in result]
                return results_str

def crawd_merge_results(base_dir):

    print(",".join([
            'query_name','Config', 'Run',
            'WJ_SampleSize', 'CRAWD_SampleSize', '∑Fµ_SampleSize', '∑Fµ_success', '∑Fµ_fail',
            'N̂', 'Nb_Total_Scans', 'Execution_time', 'cd'
        ]))

    for config in range(1, 10):
        config_dir = f"config{config}"
        path = os.path.join(base_dir,  config_dir)
        for filename in os.listdir(path):
            if filename.endswith(".result"):
                query_file = os.path.join(path, filename)
                query_name = filename.split('_')[1].split('.')[0]
                print(",".join(crawd_parse_results(query_file)))



if __name__ == "__main__":
    ROOT="/GDD/count-distinct-watdiv"
    crawd_merge_results(f"{ROOT}/output/CRAWD")
