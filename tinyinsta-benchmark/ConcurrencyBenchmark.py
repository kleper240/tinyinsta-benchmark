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
CONC_CONFIGS = [1, 10, 20, 50, 100, 1000]
CONC_PREFIX = "bench" 
# ---------------------------

class ConcurrencyBenchmark:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        os.makedirs('out', exist_ok=True)
    
    def warmup_instance(self):
        """Echauffer l'instance avec le prefixe de concurrence."""
        print(f"Echauffement de l'instance en cours (Prefixe: {CONC_PREFIX})...")
        warmup_requests = 15
        
        for i in range(warmup_requests):
            try:
                requests.get(
                    f"{self.base_url}/api/timeline",
                    params={"user": f"{CONC_PREFIX}{i % 10 + 1}"},
                    timeout=30
                )
            except Exception:
                pass
            time.sleep(0.3)
        time.sleep(10)
    
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
    
    def run_concurrent_benchmark(self, num_concurrent: int, prefix: str) -> Tuple[float, int]:
        """Executer le benchmark avec un nombre d'utilisateurs simultanes (num_concurrent)."""
        print(f"Lancement du benchmark avec {num_concurrent} requêtes simultanées...")
        
        # Utiliser les IDs de 1 à num_concurrent
        user_ids_to_test = list(range(1, num_concurrent + 1))
        
        times = []
        failed_requests = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            future_to_user = {
                executor.submit(self.make_timeline_request, prefix, user_id): user_id 
                for user_id in user_ids_to_test
            }
            
            for future in concurrent.futures.as_completed(future_to_user):
                response_time, success = future.result()
                times.append(response_time)
                if not success:
                    failed_requests += 1
        
        avg_time = statistics.mean(times) if times else 0
        return avg_time, failed_requests
    
    def run_conc_benchmark_suite(self):
        """Executer la suite de tests de concurrence."""
        print("Génération de conc.csv")
        
        self.warmup_instance()
        
        with open('out/conc.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(CSV_HEADER)
            
            for concurrent_users in CONC_CONFIGS:
                print(f"\n--- PARAM: {concurrent_users} utilisateurs simultanés ---")
                
                for run in range(1, NUM_RUNS + 1):
                    print(f"Run {run}/{NUM_RUNS}...")
                    
                    avg_time, failed = self.run_concurrent_benchmark(concurrent_users, CONC_PREFIX)
                    
                    # Formatage et écriture CSV
                    avg_time_str = f"{avg_time:.2f}ms"
                    failed_int = 1 if failed > 0 else 0
                    writer.writerow([concurrent_users, avg_time_str, run, failed_int])
                    csvfile.flush()
                    
                    print(f"Resultat: {avg_time_str}, Échecs: {failed_int}")
                    
                    if run < NUM_RUNS: time.sleep(5)
        
        print("BENCHMARK DE CONCURRENCE TERMINE")

if __name__ == "__main__":
    BASE_URL = os.environ.get("BASE_URL")
    if not BASE_URL:
        print("ERREUR: La variable d'environnement BASE_URL n'est pas définie. Veuillez l'exporter dans le script Bash.")
        sys.exit(1)

    benchmark = ConcurrencyBenchmark(BASE_URL)
    benchmark.run_conc_benchmark_suite()
