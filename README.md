# DONNÉES MASSIVES ET CLOUD - BENCHMARK TINYINSTA

## 🎯 Objectif
Benchmark complet de l'application TinyInsta pour analyser les performances sous différentes charges de concurrence et tailles de données.

## 📱 Application Déployée
URL : https://tinyinsta-benchmark-478021.ew.r.appspot.com

## 📊 Résultats du Benchmark

### 🔥 Performance en fonction de la concurrence
![Performance Concurrence](tinyinsta-benchmark/out/conc.png)

### 📝 Performance en fonction du nombre de posts
![Performance Posts](tinyinsta-benchmark/out/post.png)

### 👥 Performance en fonction du nombre de followers
![Performance Followers](tinyinsta-benchmark/out/fanout.png)

## 🛠️ GUIDE COMPLET D'EXÉCUTION

### 📁 Structure du Projet

```
tinyinsta-benchmark/
├── benchmark.py              # Benchmark principal - concurrence
├── benchmark_posts.py        # Benchmark variation posts
├── benchmark_followers.py    # Benchmark variation followers  
├── create_plots_fixed.py     # Génération des graphiques
├── generate_data.py          # Génération données (optionnel)
├── README.md                 # Documentation
└── out/                      # Résultats
    ├── conc.csv              # Données benchmark concurrence
    ├── post.csv              # Données benchmark posts
    ├── fanout.csv            # Données benchmark followers
    ├── conc.png              # Graphique concurrence
    ├── post.png              # Graphique posts
    └── fanout.png            # Graphique followers
```

### 🚀 PROCÉDURE D'EXÉCUTION COMPLÈTE

#### ÉTAPE 1 : PRÉPARATION DE L'ENVIRONNEMENT

```bash
# Se connecter à Cloud Shell et cloner le projet
git clone https://github.com/kleper240/tinyinsta-benchmark.git
cd tinyinsta-benchmark
```

```bash
# Installer les dépendances Python
pip3 install requests pandas matplotlib concurrent.futures
```

**📝 Explication :**

* `git clone` : Récupère le code depuis GitHub
* `pip3 install` : Installe les librairies pour les requêtes HTTP, l'analyse de données et la visualisation

#### ÉTAPE 2 : GÉNÉRATION DES DONNÉES DE TEST

```bash
# Aller dans le dossier de l'application
cd ~/massive-gcp

# 1. Données pour le benchmark de CONCURRENCE
python3 seed.py --users 1000 --posts 50000 --follows-min 20 --follows-max 20 --prefix bench
sleep 30

# 2. Données pour le benchmark des POSTS
python3 seed.py --users 100 --posts 1000 --follows-min 20 --follows-max 20 --prefix post10_
python3 seed.py --users 100 --posts 10000 --follows-min 20 --follows-max 20 --prefix post100_  
python3 seed.py --users 100 --posts 100000 --follows-min 20 --follows-max 20 --prefix post1000_
sleep 30

# 3. Données pour le benchmark des FOLLOWERS
python3 seed.py --users 100 --posts 100 --follows-min 10 --follows-max 10 --prefix follow10_
python3 seed.py --users 100 --posts 100 --follows-min 50 --follows-max 50 --prefix follow50_
python3 seed.py --users 100 --posts 100 --follows-min 100 --follows-max 100 --prefix follow100_
sleep 30
```

**📝 Explication des paramètres :**

* `--users X` : Crée X utilisateurs (user1, user2, ...)
* `--posts Y` : Crée Y posts au total répartis aléatoirement
* `--follows-min/max Z` : Chaque user suit entre Z et Z autres users
* `--prefix P` : Préfixe pour les noms d'utilisateurs
* `sleep 30` : Attend l'indexation des données dans Datastore

#### ÉTAPE 3 : EXÉCUTION DES BENCHMARKS

```bash
# Retourner dans le dossier benchmark
cd ~/tinyinsta-benchmark

# 1. BENCHMARK DE CONCURRENCE
python3 benchmark.py
# → Génère out/conc.csv

# 2. BENCHMARK NOMBRE DE POSTS  
python3 benchmark_posts.py
# → Génère out/post.csv

# 3. BENCHMARK NOMBRE DE FOLLOWERS
python3 benchmark_followers.py
# → Génère out/fanout.csv
```

**📝 Ce que font les scripts :**

* Envoient des requêtes HTTP concurrentes à l'application
* Mesurent les temps de réponse pour `/api/timeline?user=XXX`
* Testent différentes configurations (concurrence, taille données)
* Génèrent les fichiers CSV avec les résultats

#### ÉTAPE 4 : GÉNÉRATION DES GRAPHIQUES

```bash
# Créer les visualisations à partir des données CSV
python3 create_plots_fixed.py
# → Génère out/conc.png, out/post.png, out/fanout.png
```

**📝 Explication :**

* Lit les fichiers CSV avec pandas
* Calcule moyennes et écarts-types
* Crée des graphiques barres avec matplotlib
* Affiche la variance entre les 3 runs

## 📊 ANALYSE DES RÉSULTATS

### 🔍 Fichier conc.csv - Benchmark Concurrence

```csv
PARAM,AVG_TIME,RUN,FAILED
1,1457.25ms,1,0
1,131.68ms,2,0
1,85.35ms,3,0
10,500.02ms,1,0
...
1000,2692.96ms,3,0
```

**📊 Interprétation :**

* `PARAM` : Nombre d'utilisateurs simultanés
* `AVG_TIME` : Temps moyen de réponse en millisecondes
* `RUN` : Numéro de l'exécution (1, 2, 3)
* `FAILED` : Nombre de requêtes échouées (0 = succès)

**📈 Observations :**

* Variance importante à faible charge (cold start)
* Performance stable entre 10-100 utilisateurs
* Dégradation à 1000 utilisateurs simultanés
* Aucun échec sur l'ensemble des tests

### 🔍 Fichier post.csv - Benchmark Posts

```csv
PARAM,AVG_TIME,RUN,FAILED
10,3191.36ms,1,0
10,890.74ms,2,0
10,822.45ms,3,0
100,286.93ms,1,0
...
1000,261.09ms,3,0
```

**📊 Interprétation :**

* `PARAM` : Nombre de posts par utilisateur
* Résultat contre-intuitif : plus de posts = meilleures performances
* Problème d'optimisation avec petits datasets

### 🔍 Fichier fanout.csv - Benchmark Followers

```csv
PARAM,AVG_TIME,RUN,FAILED
10,2347.20ms,1,0
10,314.74ms,2,0
10,270.34ms,3,0
50,3314.85ms,1,0
...
100,3628.96ms,3,0
```

**📊 Interprétation :**

* `PARAM` : Nombre de followers par utilisateur
* Croissance linéaire du temps avec le nombre de followers
* Impact important sur les performances

## 🎯 COMMANDES DE VÉRIFICATION

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

## 📈 CONCLUSIONS TECHNIQUES

### ✅ Points Forts
* Robustesse : 0 échec sur 18+ configurations testées
* Scalabilité : Bonne performance jusqu'à 100 utilisateurs simultanés
* Gestion données : Excellente avec volumes importants

### ⚠️ Points d'Amélioration
* Cold start : Variance importante à faible charge
* Optimisation fanout : Impact linéaire des followers
* Petits datasets : Performance anormale avec peu de données

### 🎯 Recommandations
* Implémenter un cache pour les timelines fréquentes
* Limiter le nombre maximum de followers par utilisateur
* Pré-chauffer l'application avant utilisation

## 👨‍💻 Auteur
* **Étudiant** : Marius Mabulu
* **Projet** : DONNÉES MASSIVES ET CLOUD - BENCHMARK
* **Date** : Novembre 2024
* **Dépôt Git** : https://github.com/kleper240/tinyinsta-benchmark

**Dernière exécution** : $(date)

**📞 Pour toute question** : Consulter le code source et les commentaires dans les scripts Python.
