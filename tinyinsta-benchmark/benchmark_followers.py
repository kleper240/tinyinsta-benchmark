import requests
import time
import csv
import concurrent.futures
import statistics

class FollowersBenchmark:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def make_timeline_request(self, prefix: str, user_id: int) -> tuple:
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
            print(f"Exception pour {prefix}{user_id}: {e}")
            return (time.time() - start_time) * 1000, False
    
    def run_followers_benchmark(self):
        print("=== BENCHMARK NOMBRE DE FOLLOWERS ===")
        
        configs = [
            ("bench_f10", 10, "10 followers par user"),
            ("bench_f50", 50, "50 followers par user"), 
            ("bench_f100", 100, "100 followers par user")
        ]
        
        with open('out/fanout.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['PARAM', 'AVG_TIME', 'RUN', 'FAILED'])
            
            for prefix, param_value, description in configs:
                print(f"\n--- {description} ---")
                
                for run in range(1, 4):
                    print(f"Run {run}/3...")
                    
                    times = []
                    failed_requests = 0
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                        future_to_user = {
                            executor.submit(self.make_timeline_request, prefix, user_id): user_id 
                            for user_id in range(1, 51)
                        }
                        
                        for future in concurrent.futures.as_completed(future_to_user):
                            response_time, success = future.result()
                            times.append(response_time)
                            if not success:
                                failed_requests += 1
                    
                    avg_time = statistics.mean(times) if times else 0
                    
                    writer.writerow([param_value, f"{avg_time:.2f}ms", run, failed_requests])
                    csvfile.flush()
                    
                    print(f"Résultat: {avg_time:.2f}ms, Échecs: {failed_requests}")
                    time.sleep(2)

if __name__ == "__main__":
    BASE_URL = "https://tinyinsta-benchmark-478021.ew.r.appspot.com"
    benchmark = FollowersBenchmark(BASE_URL)
    benchmark.run_followers_benchmark()
