#!/bin/bash

# ==============================================================================
# CONFIGURATION ET PRÉREQUIS
# ==============================================================================
# Chemin vers le dossier racine (doit contenir massive-gcp et tinyinsta-benchmark)
ROOT_DIR=$(dirname $(dirname $(readlink -f "$0")))
SEED_SCRIPT="$ROOT_DIR/massive-gcp/seed.py"
BENCH_DIR="$ROOT_DIR/tinyinsta-benchmark"
OUT_DIR="$BENCH_DIR/out"
VENV_DIR="$BENCH_DIR/.venv" # Dossier pour l'environnement virtuel

# Variables d'environnement de l'application déployée sur GCP
export GCLOUD_PROJECT="tinyinsta-benchmark-478021"
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
# 1. PRÉPARATION DE L'ENVIRONNEMENT PYTHON (FIX ARCHITECTURE MAC)
# ==============================================================================

# Vérifie l'architecture du système d'exploitation
OS_TYPE=$(uname -s)
ARCH_TYPE=$(uname -m)

if [ "$OS_TYPE" == "Darwin" ] && [ "$ARCH_TYPE" == "arm64" ]; then
    echo -e "\n--- 🍎 Détection: Mac Apple Silicon (ARM64) ---"
    echo "Création/Mise à jour d'un environnement virtuel pour assurer la compatibilité."

    # Désactiver l'environnement virtuel si déjà actif
    if type deactivate > /dev/null 2>&1; then
        deactivate
    fi

    # Supprimer et recréer l'environnement virtuel pour forcer la compilation ARM64
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
    
    # Activation de l'environnement
    source "$VENV_DIR/bin/activate"
    
    # Installation des dépendances
    echo "Installation des dépendances (pandas, numpy, matplotlib, requests) dans l'environnement virtuel."
    pip install --upgrade pip
    pip install pandas numpy matplotlib requests
    
    # Vérification si l'installation a réussi
    if [ $? -ne 0 ]; then
        echo "ERREUR: L'installation des paquets Python a échoué. Arrêt du script."
        exit 1
    fi

else
    echo -e "\n--- 💻 Détection: Architecture standard ($OS_TYPE/$ARCH_TYPE) ---"
    echo "Tentative d'activation d'un environnement virtuel local ou utilisation de python3 système."
    # Si un venv est présent, l'activer par défaut pour la propreté
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        echo "Environnement virtuel local activé."
    fi
fi

# ==============================================================================
# NETTOYAGE INITIAL DES DONNÉES (Optionnel)
# ==============================================================================
# echo -e "\n--- 🧹 Nettoyage initial des données existantes ---"
# python3 "$BENCH_DIR/delete_all_data.py"
# sleep 15 

# ==============================================================================
# ÉTAPE 2 : BENCHMARK SUR LA CHARGE (CONCURRENCE) -> conc.csv
# ==============================================================================
echo -e "\n\n--- 🚀 2. BENCHMARK CONCURRENCE (conc.csv) ---"

# 2.1. SEEDING DE CONCURRENCE (Prefixe: bench)
echo "2.1. Génération des données de base (50k posts, 20 follows, prefix: bench)"
python3 "$SEED_SCRIPT" --users 1000 --posts 50000 --follows-min 20 --follows-max 20 --prefix bench
sleep 30 

# 2.2. EXÉCUTION DU BENCHMARK
echo "2.2. Exécution du benchmark de concurrence."
python3 "$BENCH_DIR/ConcurrencyBenchmark.py"

# ==============================================================================
# ÉTAPE 3 : BENCHMARK SUR LES FOLLOWEES (FANOUT) -> fanout.csv
# ==============================================================================
echo -e "\n\n--- 🤝 3. BENCHMARK FOLLOWEES (fanout.csv) ---"

# 3.1. PARAM = 10 Followees
echo "3.1. Génération des données (10 followees, 100k posts, prefix: follow10_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 10 --follows-max 10 --prefix follow10_
sleep 30
echo "3.2. Exécution pour PARAM=10."
python3 "$BENCH_DIR/FollowersBenchmark.py" 10 follow10_

# 3.3. PARAM = 50 Followees
echo "3.3. Génération des données (50 followees, 100k posts, prefix: follow50_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 50 --follows-max 50 --prefix follow50_
sleep 30
echo "3.4. Exécution pour PARAM=50."
python3 "$BENCH_DIR/FollowersBenchmark.py" 50 follow50_

# 3.5. PARAM = 100 Followees
echo "3.5. Génération des données (100 followees, 100k posts, prefix: follow100_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 100 --follows-max 100 --prefix follow100_
sleep 30
echo "3.6. Exécution pour PARAM=100."
python3 "$BENCH_DIR/FollowersBenchmark.py" 100 follow100_


# ==============================================================================
# ÉTAPE 4 : BENCHMARK SUR LES POSTS (TAILLE) -> post.csv
# ==============================================================================
echo -e "\n\n--- 📦 4. BENCHMARK POSTS (post.csv) ---"

# 4.1. PARAM = 10 Posts (10k posts)
echo "4.1. Génération des données (10 posts/user, 20 follows, prefix: post10_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 10000 --follows-min 20 --follows-max 20 --prefix post10_
sleep 30
echo "4.2. Exécution pour PARAM=10."
python3 "$BENCH_DIR/PostsBenchmark.py" 10 post10_

# 4.3. PARAM = 100 Posts (100k posts)
echo "4.3. Génération des données (100 posts/user, 20 follows, prefix: post100_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 100000 --follows-min 20 --follows-max 20 --prefix post100_
sleep 30
echo "4.4. Exécution pour PARAM=100."
python3 "$BENCH_DIR/PostsBenchmark.py" 100 post100_

# 4.5. PARAM = 1000 Posts (1M posts)
echo "4.5. Génération des données (1000 posts/user, 20 follows, prefix: post1000_)"
python3 "$SEED_SCRIPT" --users 1000 --posts 1000000 --follows-min 20 --follows-max 20 --prefix post1000_
sleep 60 # Pause plus longue pour 1M posts
echo "4.6. Exécution pour PARAM=1000."
python3 "$BENCH_DIR/PostsBenchmark.py" 1000 post1000_
BENCH_EXIT_CODE=$? # <-- Capture du code de retour du dernier benchmark

# ==============================================================================
# ÉTAPE 5 : RENDU DES GRAPHIQUES ET NETTOYAGE
# ==============================================================================
echo -e "\n\n--- 🖼️ 5. GENERATION DES GRAPHIQUES ---"

if [ $BENCH_EXIT_CODE -eq 0 ]; then
    # Exécuter la création des graphiques pendant que le VENV est actif
    python3 "$BENCH_DIR/CreatePlots.py"
    
    if [ $? -eq 0 ]; then
        echo -e "\n=================================================="
        echo "SUITE DE BENCHMARK TERMINÉE. Graphiques générés dans $OUT_DIR."
        echo "=================================================="
    else
        echo -e "\nERREUR: La génération des graphiques a échoué (CreatePlots.py)."
        echo "Vérifiez que les fichiers CSV existent et sont valides."
        echo "=================================================="
    fi
else
    echo -e "\nERREUR: L'exécution du dernier benchmark a échoué. Les graphiques ne seront pas générés."
    echo "=================================================="
fi


# Désactiver l'environnement virtuel si nous l'avons activé
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
    echo -e "\nEnvironnement virtuel désactivé."
fi