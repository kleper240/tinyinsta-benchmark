import subprocess
import sys
import time

def seed_data_locally(users: int, posts: int, follows_min: int, follows_max: int, prefix: str):
    """Générer les données de test en utilisant le script seed.py local"""
    print(f"Génération des données: {users} users, {posts} posts, {follows_min}-{follows_max} follows")
    
    try:
        # Exécuter le script seed.py directement
        result = subprocess.run([
            sys.executable, 'seed.py',
            '--users', str(users),
            '--posts', str(posts),
            '--follows-min', str(follows_min),
            '--follows-max', str(follows_max),
            '--prefix', prefix
        ], capture_output=True, text=True, cwd='../massive-gcp')  # Aller dans le dossier massive-gcp
        
        if result.returncode == 0:
            print("Données générées avec succès")
            print(result.stdout)
        else:
            print(f"Erreur lors de la génération: {result.returncode}")
            print("STDERR:", result.stderr)
            print("STDOUT:", result.stdout)
            
    except Exception as e:
        print(f"Exception lors de la génération: {e}")

def generate_all_datasets():
    """Générer tous les jeux de données nécessaires"""
    
    # Données pour le benchmark de concurrence (fixes)
    print("=== Génération des données pour le benchmark de concurrence ===")
    seed_data_locally(users=1000, posts=50000, follows_min=20, follows_max=20, prefix="bench")
    
    # Attendre que les données soient indexées
    print("Attente de l'indexation des données...")
    time.sleep(30)
    
    # Données pour le benchmark des posts (vous pouvez adapter selon besoin)
    print("\n=== Génération des données pour le benchmark des posts ===")
    # Note: Vous devrez regénérer pour chaque configuration
    # seed_data_locally(users=100, posts=1000, follows_min=20, follows_max=20, prefix="bench_post_10")
    # seed_data_locally(users=100, posts=10000, follows_min=20, follows_max=20, prefix="bench_post_100")
    # seed_data_locally(users=100, posts=100000, follows_min=20, follows_max=20, prefix="bench_post_1000")

if __name__ == "__main__":
    generate_all_datasets()