# DONNÉES MASSIVES ET CLOUD - BENCHMARK TINYINSTA

## Objectif
Benchmark complet de l'application TinyInsta pour analyser les performances sous différentes charges de concurrence et tailles de données.

## Application Déployée
- **URL** : https://tinyinsta-benchmark-478021.ew.r.appspot.com

## Guide Complet d'Exécution

### Structure du Projet
```
tinyinsta-benchmark/
├── ConcurrencyBenchmark.py      # Benchmark principal - concurrence
├── PostsBenchmark.py            # Benchmark variation posts
├── FollowersBenchmark.py        # Benchmark variation followers
├── CreatePlots.py               # Génération des graphiques
├── delete_data.py               # Suppression des données
├── run_benchmark_suite.sh       # Automatisation : génération données, benchmarks (concurrence, posts, followers) et graphiques
├── README.md                    # Documentation
└── out/                         # Résultats
    ├── conc.csv                 # Données benchmark concurrence
    ├── post.csv                 # Données benchmark posts
    ├── fanout.csv               # Données benchmark followers
    ├── conc.png                 # Graphique concurrence
    ├── post.png                 # Graphique posts
    └── fanout.png               # Graphique followers
```

### Procédure d'Exécution Complète

#### Étape 1 : Préparation de l'Environnement
1. **Cloner les projets nécessaires**  
   Ouvrez Cloud Shell (ou une machine avec Git et Python installés) et exécutez :
   ```bash
   git clone https://github.com/momo54/massive-gcp.git
   git clone https://github.com/kleper240/tinyinsta-benchmark.git
   ```

2. **Créer le dossier de sortie**  
   ```bash
   mkdir -p tinyinsta-benchmark/out
   ```

3. **Naviguer dans le dossier du projet**  
   ```bash
   cd tinyinsta-benchmark
   ```

4. **Installer les dépendances Python**  
   ```bash
   pip3 install requests pandas matplotlib concurrent.futures
   ```

**Explication** :  
- `git clone` récupère le code depuis GitHub.  
- `pip3 install` installe les librairies pour les requêtes HTTP, l'analyse de données et la visualisation.

#### Étape 2 : Lancement de la Suite de Benchmarks
1. **Rendre le script Bash exécutable**  
   ```bash
   chmod +x run_benchmark_suite.sh
   ```

2. **Lancer le benchmark complet**  
   ```bash
   ./run_benchmark_suite.sh
   ```

**Ce que fait le script** :  
- Génère les données via `seed.py` (dans `massive-gcp/`).  
- Exécute les benchmarks : concurrence (`ConcurrencyBenchmark.py`), posts (`PostsBenchmark.py`), followers (`FollowersBenchmark.py`).  
- Envoie des requêtes HTTP concurrentes à `/api/timeline?user=XXX`.  
- Mesure les temps de réponse et teste différentes configurations.  
- Génère les fichiers CSV dans `out/`.  

Tout est automatisé. Le script nettoie les anciens résultats et réinitialise la base de données.

#### Étape 3 : Génération des Graphiques (Automatique)
Les graphiques sont générés automatiquement à la fin du script via `CreatePlots.py`.  
Si besoin de les régénérer manuellement :  
```bash
python3 CreatePlots.py
```  
→ Génère `out/conc.png`, `out/post.png`, `out/fanout.png`.

**Explication** :  
- Lit les fichiers CSV avec Pandas.  
- Calcule moyennes et écarts-types.  
- Crée des graphiques en barres avec Matplotlib.  
- Affiche la variance entre les 3 runs.

## Analyse des Résultats

### Fichier `conc.csv` - Benchmark Concurrence
Contenu complet :
```csv
PARAM,AVG_TIME,RUN,FAILED
1,153.24ms,1,0
1,140.82ms,2,0
1,129.56ms,3,0
10,426.58ms,1,0
10,326.88ms,2,0
10,245.17ms,3,0
20,394.87ms,1,0
20,336.30ms,2,0
20,363.09ms,3,0
50,482.58ms,1,0
50,356.28ms,2,0
50,363.21ms,3,0
100,520.83ms,1,0
100,510.03ms,2,0
100,487.78ms,3,0
1000,2725.09ms,1,0
1000,1417.71ms,2,0
1000,1449.23ms,3,0
```

**Interprétation** :  
- `PARAM` : Nombre d'utilisateurs simultanés.  
- `AVG_TIME` : Temps moyen de réponse en millisecondes.  
- `RUN` : Numéro de l'exécution (1, 2, 3).  
- `FAILED` : Nombre de requêtes échouées (0 = succès).  

**Moyennes par niveau de concurrence** (calculées sur 3 runs) :  
| PARAM | Moyenne (ms) |  
|-------|--------------|  
| 1     | 141.21      |  
| 10    | 332.88      |  
| 20    | 364.75      |  
| 50    | 400.69      |  
| 100   | 506.21      |  
| 1000  | 1864.01     |  

**Observations** :  
- Les temps de réponse augmentent progressivement avec le niveau de concurrence, indiquant une scalabilité raisonnable jusqu'à 100 utilisateurs simultanés.  
- Stabilité relative entre 20 et 100 utilisateurs (augmentation modérée de ~40 %).  
- Dégradation significative à 1000 utilisateurs (x4 par rapport à 100), probablement due à la saturation des ressources Cloud Run.  
- Variance notable à faible charge (cold starts), mais performances plus consistantes à charge élevée.  
- Aucune erreur (FAILED = 0 partout), confirmant la robustesse de l'application.

### Fichier `post.csv` - Benchmark Posts
Contenu partiel (en attente du run à 1000 posts/utilisateur pour 1M posts total) :
```csv
PARAM,AVG_TIME,RUN,FAILED
10,833.43ms,1,0
10,404.88ms,2,0
10,346.01ms,3,0
100,1477.90ms,1,0
100,406.37ms,2,0
100,312.65ms,3,0
```

**Interprétation** :  
- `PARAM` : Nombre de posts par utilisateur (10 → 10k posts total ; 100 → 100k posts total).  
- `AVG_TIME` : Temps moyen de réponse en millisecondes.  
- `RUN` : Numéro de l'exécution (1, 2, 3).  
- `FAILED` : Nombre de requêtes échouées (0 = succès).  

**Moyennes par niveau de posts** (calculées sur 3 runs) :  
| PARAM | Moyenne (ms) |  
|-------|--------------|  
| 10    | 528.11      |  
| 100   | 732.31      |  

**Observations (préliminaires)** :  
- Les temps de réponse augmentent avec la taille du dataset (de 10k à 100k posts), ce qui est attendu en raison du volume de données à charger dans Firestore.  
- Variance élevée au premier run (cold start), mais stabilisation rapide aux runs suivants.  
- Résultat contre-intuitif potentiel : performances légèrement meilleures avec datasets plus grands une fois "chaud" (à confirmer avec le run 1M).  
- Aucune erreur observée.  
- **Note** : Analyse complète en attente du run à 1000 posts/utilisateur (1M posts total).

### Fichier `fanout.csv` - Benchmark Followers
Contenu complet :
```csv
PARAM,AVG_TIME,RUN,FAILED
10,1446.10ms,1,0
10,451.47ms,2,0
10,371.43ms,3,0
50,7332.64ms,1,0
50,5092.80ms,2,0
50,5237.97ms,3,0
100,12156.92ms,1,0
100,10600.65ms,2,0
100,6335.95ms,3,0
```

**Interprétation** :  
- `PARAM` : Nombre de followees par utilisateur (impact sur le fanout lors de la génération de la timeline).  
- `AVG_TIME` : Temps moyen de réponse en millisecondes.  
- `RUN` : Numéro de l'exécution (1, 2, 3).  
- `FAILED` : Nombre de requêtes échouées (0 = succès).  

**Moyennes par niveau de followees** (calculées sur 3 runs) :  
| PARAM | Moyenne (ms) |  
|-------|--------------|  
| 10    | 756.33      |  
| 50    | 5887.80     |  
| 100   | 9697.84     |  

**Observations** :  
- Croissance quasi-linéaire du temps de réponse avec le nombre de followees : x8 entre 10 et 50, puis +65 % jusqu'à 100.  
- Impact majeur du fanout sur les performances, car chaque timeline doit agréger plus de posts de sources multiples.  
- Variance importante au premier run (cold start), mais convergence aux runs suivants.  
- Aucune erreur, mais temps élevés à 100 followees (>9s en moyenne) indiquent un besoin d'optimisation (ex. : pagination ou cache).  

## Résultats du Benchmark

### Performance en Fonction de la Concurrence
![Performance Concurrence](tinyinsta-benchmark/out/conc.png)

### Performance en Fonction du Nombre de Posts
![Performance Posts](tinyinsta-benchmark/out/post.png)

### Performance en Fonction du Nombre de Followers
![Performance Followers](tinyinsta-benchmark/out/fanout.png)

## Commandes de Vérification
```bash
# Vérifier que l'application répond
curl "https://tinyinsta-benchmark-478021.ew.r.appspot.com/api/timeline?user=bench1"

# Vérifier les fichiers générés
ls -la out/

# Afficher les résultats
head out/conc.csv
head out/post.csv
head out/fanout.csv

# Vérifier les graphiques
ls -la out/*.png
```

## Conclusions Techniques

### Points Forts
- **Robustesse** : 0 échec sur l'ensemble des tests (18+ configurations).  
- **Scalabilité en concurrence** : Excellente jusqu'à 100 utilisateurs simultanés (temps <500 ms).  
- **Gestion des données** : Stable même avec datasets volumineux (préliminaire pour posts).

### Points d'Amélioration
- **Cold starts** : Variance élevée à faible charge et premier run ; implémenter un warm-up.  
- **Fanout** : Impact linéaire critique (x12 entre 10 et 100 followees) ; optimiser avec cache ou sharding.  
- **Datasets intermédiaires** : Temps plus longs pour petits/moyens volumes (à confirmer avec 1M posts) ; investiguer les queries Firestore.

### Recommandations
- Ajouter un cache Redis/Memcached pour les timelines statiques.  
- Limiter le fanout max par utilisateur (ex. : 50 followees).  
- Utiliser des indexes Firestore optimisés et pagination pour les gros datasets.  
- Pré-chauffer l'instance Cloud Run pour réduire les latences initiales.

## Auteur
- **Étudiant** : Marius Mabulu  
- **Projet** : DONNÉES MASSIVES ET CLOUD - BENCHMARK  
- **Date** : Décembre 2025  
- **Dépôt Git** : https://github.com/kleper240/tinyinsta-benchmark  
- **Dernière exécution** : 6 décembre 2025  

**Pour toute question** : Consulter le code source et les commentaires dans les scripts Python.
