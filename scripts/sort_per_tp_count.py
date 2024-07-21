import pandas as pd
import sys

def main(file_path):
    # Charger le fichier CSV
    df = pd.read_csv(file_path)

    # Renommer les colonnes
    df.columns = ['query_name', 'nbtp', 'count']

    # Grouper par 'nbtp' et obtenir les 5 requêtes avec le plus grand 'count' pour chaque groupe
    top_queries_per_nbtp = df.sort_values('count', ascending=False).groupby('nbtp').head(5).reset_index(drop=True)
    top_queries_per_nbtp = top_queries_per_nbtp[top_queries_per_nbtp['count'] >= 100]
    # Afficher les résultats avec des colonnes non tronquées
    top_queries_per_nbtp.to_csv(sys.stdout, index=False)

# python scripts/sort_per_tp.py original_watdiv_tp_count.csv > top5_nbtp_original_watdiv.csv
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        main(file_path)
