import requests
import time
import csv
import concurrent.futures
import statistics
import os
import sys
from typing import List, Tuple

# --- Constantes du Projet ---
CSV_HEADER = ['PARAM', 'AVG_TIME', 'RUN', 'FAILED']
NUM_RUNS = 3
CONCURRENCE = 50 
# ---------------------------

class PostsBenchmark:
    def __init__(self, base_url: str, param_value: int, prefix: str):
        self.base_url = base_url.rstrip('/')
        self.param_value = param_value
        self.prefix = prefix
        os.makedirs('out', exist_ok=True)

    def make_timeline_request(self, prefix: str, user_id: int) -> Tuple[float, bool]:
        """Faire une requete timeline et retourner le temps de reponse et le statut"""
        start_time = time.time()
        try:
            response = requests.get(
                f"{self.base_url}/api/timeline",
                params={"user": f"{prefix}{user_id}"},
                timeout=120
            )
            success = response.status_code == 200
            return (time.time() - start_time) * 1000, success
        except Exception as e:
            # print(f"Exception pour {prefix}{user_id}: {e}") # Désactiver pour éviter trop de logs
            return (time.time() - start_time) * 1000, False
    
    def warmup_specific_prefix(self):
        """Echauffement specifique pour un prefix donne"""
        print(f"Echauffement specifique des donnees {self.prefix}...")
        for i in range(5):
            try:
                self.make_timeline_request(self.prefix, i + 1)
            except:
                pass
            time.sleep(0.5)
        time.sleep(3)

    def run_posts_benchmark(self):
        print(f"\n--- BENCHMARK POSTS (PARAM={self.param_value}) ---")
        
        self.warmup_specific_prefix()
        
        # Ouvrir en mode append 'a' si le fichier existe déjà, sinon 'w'
        file_exists = os.path.exists('out/post.csv')
        mode = 'a' if file_exists else 'w'

        with open('out/post.csv', mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(CSV_HEADER) # Écrire l'en-tête seulement si le fichier est nouveau
            
            for run in range(1, NUM_RUNS + 1):
                print(f"Run {run}/{NUM_RUNS}. Concurrence: {CONCURRENCE} requêtes (Prefixe: {self.prefix}).")
                
                times = []
                failed_requests = 0
                
                # Concurrence FIXE de 50 requêtes
                user_ids_to_test = list(range(1, CONCURRENCE + 1))
                with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCE) as executor:
                    future_to_user = {
                        executor.submit(self.make_timeline_request, self.prefix, user_id): user_id 
                        for user_id in user_ids_to_test
                    }
                    
                    for future in concurrent.futures.as_completed(future_to_user):
                        response_time, success = future.result()
                        times.append(response_time)
                        if not success:
                            failed_requests += 1
                
                avg_time = statistics.mean(times) if times else 0
                
                avg_time_str = f"{avg_time:.2f}ms"
                failed_int = 1 if failed_requests > 0 else 0
                
                writer.writerow([self.param_value, avg_time_str, run, failed_int])
                csvfile.flush()
                
                print(f"Resultat: {avg_time_str}, Échecs: {failed_int}")
                if run < NUM_RUNS: time.sleep(5)
        
        print("BENCHMARK POSTS TERMINE pour cette configuration.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 PostsBenchmark.py <PARAM_VALUE> <PREFIX>")
        sys.exit(1)
        
    BASE_URL = os.environ.get("BASE_URL")
    if not BASE_URL:
        print("ERREUR: La variable d'environnement BASE_URL n'est pas définie.")
        sys.exit(1)
        
    param_value = int(sys.argv[1])
    prefix = sys.argv[2]
    
    benchmark = PostsBenchmark(BASE_URL, param_value, prefix)
    benchmark.run_posts_benchmark()
