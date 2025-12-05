#!/bin/bash

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Chemin vers le dossier racine (doit contenir massive-gcp et tinyinsta-benchmark)
ROOT_DIR=$(dirname $(dirname $(readlink -f "$0")))
SEED_SCRIPT="$ROOT_DIR/massive-gcp/seed.py"
BENCH_DIR="$ROOT_DIR/tinyinsta-benchmark"
OUT_DIR="$BENCH_DIR/out"

export GCLOUD_PROJECT="tinyinsta-benchmark-478021"

# URL de l'application déployée sur GCP (tinyinsta-benchmark)
export BASE_URL="https://tinyinsta-benchmark-478021.ew.r.appspot.com"

# Vérification des prérequis
if [ ! -f "$SEED_SCRIPT" ]; then
    echo "ERREUR: Script seed.py non trouvé à $SEED_SCRIPT. Vérifiez la structure."
    exit 1
fi

echo "Début de la suite de benchmark TinyInsta."
echo "URL de l'application: $BASE_URL"

# Préparation du répertoire de sortie
mkdir -p "$OUT_DIR"
rm -f "$OUT_DIR"/*.csv

# ==============================================================================
# NETTOYAGE INITIAL DES DONNÉES
# ==============================================================================
# echo -e "\n--- 🧹 Nettoyage initial des données existantes ---"
# python3 "$BENCH_DIR/delete_all_data.py"
# sleep 15 # Attendre la stabilisation après le nettoyage
# ==============================================================================
# ÉTAPE 1 : BENCHMARK SUR LA CHARGE (CONCURRENCE) -> conc.csv
# Données fixées : 1000 users, 50 posts/user (50k posts), 20 follows/user.
# ==============================================================================
echo -e "\n\n--- 🚀 1. BENCHMARK CONCURRENCE (conc.csv) ---"

# 1.1. SEEDING DE CONCURRENCE (Prefixe: bench)
echo "1.1. Génération des données de base (50k posts, 20 follows, prefix: bench)"
python3 "$SEED_SCRIPT" --users 1000 --posts 50000 --follows-min 20 --follows-max 20 --prefix bench
sleep 30 # Attendre l'indexation/stabilisation

# 1.2. EXÉCUTION DU BENCHMARK
echo "1.2. Exécution du benchmark de concurrence."
python3 "$BENCH_DIR/ConcurrencyBenchmark.py"

# ==============================================================================
# ÉTAPE 2 : BENCHMARK SUR LES FOLLOWEES (FANOUT) -> fanout.csv
# Concurrence fixée à 50. Posts fixés à 100/user (100k posts).
# Les scripts Python gèrent l'écriture séquentielle dans fanout.csv (APPEND).
# ==============================================================================
echo -e "\n\n--- 🤝 2. BENCHMARK FOLLOWEES (fanout.csv) ---"

# 2.1. PARAM = 10 Followees
echo "2.1. Génération des données (10 followees, 100k posts, prefix: follow10_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 10 --follows-max 10 --prefix follow10_
sleep 30
echo "2.2. Exécution pour PARAM=10."
python3 "$BENCH_DIR/FollowersBenchmark.py" 10 follow10_

# 2.3. PARAM = 50 Followees
echo "2.3. Génération des données (50 followees, 100k posts, prefix: follow50_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 50 --follows-max 50 --prefix follow50_
sleep 30
echo "2.4. Exécution pour PARAM=50."
python3 "$BENCH_DIR/FollowersBenchmark.py" 50 follow50_

# 2.5. PARAM = 100 Followees
echo "2.5. Génération des données (100 followees, 100k posts, prefix: follow100_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 100 --follows-max 100 --prefix follow100_
sleep 30
echo "2.6. Exécution pour PARAM=100."
python3 "$BENCH_DIR/FollowersBenchmark.py" 100 follow100_


# ==============================================================================
# ÉTAPE 3 : BENCHMARK SUR LES POSTS (TAILLE) -> post.csv
# Concurrence fixée à 50. Followees fixés à 20/user.
# ==============================================================================
echo -e "\n\n--- 📦 3. BENCHMARK POSTS (post.csv) ---"

# 3.1. PARAM = 10 Posts (10k posts)
echo "3.1. Génération des données (10 posts/user, 20 follows, prefix: post10_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 10000 --follows-min 20 --follows-max 20 --prefix post10_
sleep 30
echo "3.2. Exécution pour PARAM=10."
python3 "$BENCH_DIR/PostsBenchmark.py" 10 post10_

# 3.3. PARAM = 100 Posts (100k posts)
echo "3.3. Génération des données (100 posts/user, 20 follows, prefix: post100_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 20 --follows-max 20 --prefix post100_
sleep 30
echo "3.4. Exécution pour PARAM=100."
python3 "$BENCH_DIR/PostsBenchmark.py" 100 post100_

# 3.5. PARAM = 1000 Posts (1M posts)
echo "3.5. Génération des données (1000 posts/user, 20 follows, prefix: post1000_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 1000000 --follows-min 20 --follows-max 20 --prefix post1000_
sleep 60 # Pause plus longue pour 1M posts
echo "3.6. Exécution pour PARAM=1000."
python3 "$BENCH_DIR/PostsBenchmark.py" 1000 post1000_


# ==============================================================================
# ÉTAPE 4 : RENDU DES GRAPHIQUES
# ==============================================================================
echo -e "\n\n--- 🖼️ 4. GENERATION DES GRAPHIQUES ---"
python3 "$BENCH_DIR/CreatePlots.py"

echo -e "\n=================================================="
echo "SUITE DE BENCHMARK TERMINÉE. Vérifiez $OUT_DIR."
echo "=================================================="
