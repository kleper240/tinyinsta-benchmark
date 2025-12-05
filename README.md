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
Exemple de contenu :
```csv
PARAM,AVG_TIME,RUN,FAILED
1,1457.25ms,1,0
1,131.68ms,2,0
1,85.35ms,3,0
10,500.02ms,1,0
...
1000,2692.96ms,3,0
```

**Interprétation** :  
- `PARAM` : Nombre d'utilisateurs simultanés.  
- `AVG_TIME` : Temps moyen de réponse en millisecondes.  
- `RUN` : Numéro de l'exécution (1, 2, 3).  
- `FAILED` : Nombre de requêtes échouées (0 = succès).  

**Observations** :  
- Variance importante à faible charge (cold start).  
- Performance stable entre 10-100 utilisateurs.  
- Dégradation à 1000 utilisateurs simultanés.  
- Aucun échec sur l'ensemble des tests.

### Fichier `post.csv` - Benchmark Posts
Exemple de contenu :
```csv
PARAM,AVG_TIME,RUN,FAILED
10,3191.36ms,1,0
10,890.74ms,2,0
10,822.45ms,3,0
100,286.93ms,1,0
...
1000,261.09ms,3,0
```

**Interprétation** :  
- `PARAM` : Nombre de posts par utilisateur.  
- Résultat contre-intuitif : plus de posts = meilleures performances.  
- Problème d'optimisation avec petits datasets.

### Fichier `fanout.csv` - Benchmark Followers
Exemple de contenu :
```csv
PARAM,AVG_TIME,RUN,FAILED
10,2347.20ms,1,0
10,314.74ms,2,0
10,270.34ms,3,0
50,3314.85ms,1,0
...
100,3628.96ms,3,0
```

**Interprétation** :  
- `PARAM` : Nombre de followers par utilisateur.  
- Croissance linéaire du temps avec le nombre de followers.  
- Impact important sur les performances.

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
- **Robustesse** : 0 échec sur 18+ configurations testées.  
- **Scalabilité** : Bonne performance jusqu'à 100 utilisateurs simultanés.  
- **Gestion des données** : Excellente avec volumes importants.

### Points d'Amélioration
- **Cold start** : Variance importante à faible charge.  
- **Optimisation fanout** : Impact linéaire des followers.  
- **Petits datasets** : Performance anormale avec peu de données.

### Recommandations
- Implémenter un cache pour les timelines fréquentes.  
- Limiter le nombre maximum de followers par utilisateur.  
- Pré-chauffer l'application avant utilisation.

## Auteur
- **Étudiant** : Marius Mabulu  
- **Projet** : DONNÉES MASSIVES ET CLOUD - BENCHMARK  
- **Date** : Novembre 2025  
- **Dépôt Git** : https://github.com/kleper240/tinyinsta-benchmark  
- **Dernière exécution** : 17 novembre 2025  

**Pour toute question** : Consulter le code source et les commentaires dans les scripts Python.
