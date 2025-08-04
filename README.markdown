## Description
Ce projet est un script Python qui scrape les informations de livres depuis un site web telles que : l'URL, l'UPC, le titre, le prix, le stock, la description, la catégorie, l'évaluation, et les images associées. Les données de chaque catégorie sont enregistrées dans un fichier CSV (`nom_de_category.csv`), et les images sont téléchargées dans un dossier `images/`. Le script utilise les bibliothèques tierces `requests` et `beautifulsoup4`. Le script fonctionne exclusivement avec "https://books.toscrape.com/".

Ce projet implémente un pipeline ETL (Extract, Transform, Load) :
- **Extract** : Récupération des données via des requêtes HTTP et parsing HTML.
- **Transform** : Nettoyage et formatage des données (par exemple, extraction des prix, du stock, et des et des évaluations).
- **Load** : Sauvegarde des données dans des fichiers CSV et des images dans un dossier.

## Prérequis
Pour exécuter ce projet, vous devez avoir les outils suivants installés :
- **Python** : Version 3.8 ou supérieure.
- **Git** : Outil de contrôle de version pour cloner le dépaôt.
- **Terminal** : Un terminal comme Command Prompt (Windows), Terminal (macOS), ou un shell Linux.

### Installation de Python
- **Windows** :
  1. Téléchargez Python 3.8 ou supérieur depuis [https://www.python.org/downloads]
  2. Exécutez l'installateur et cochez l'option **"Add Python to PATH"** avant de cliquer sur "Install Now".

- **macOS** :
  1. Téléchargez Python depuis [https://www.python.org/downloads]
  2. Vérifiez avec `python3 --version` et `pip3 --version`.
- **Linux** :
  1. Installez Python avec votre gestionnaire de paquets, par exemple `sudo apt install python3 python3-pip` (Ubuntu).
  2. Vérifiez avec `python3 --version` et `pip3 --version`.

### Installation de Git
- **Windows** :
  1. Téléchargez Git depuis [https://git-scm.com/download/win]
  2. Exécutez l'installateur et acceptez les options par défaut.

- **macOS** :
  1. Installez Git depuis [https://git-scm.com/download/mac]
  2. Vérifiez avec `git --version`.
- **Linux** :
  1. Installez Git avec votre gestionnaire de paquets, par exemple `sudo apt install git` (Ubuntu).
  2. Vérifiez avec `git --version`.

## Installer, configurer et exécuter le projet
Une fois les prérequis complétés, nous pouvons passer à la configuration du script.

### 1. Cloner le dépôt Github en local
Ouvrez votre terminal de commande, déplacer-vous avec "cd" dans le dossier dans lequel vous souhaitez stocker le projet et tapez :
```bash
git clone https://github.com/redaa91ab/Books-online-scraper
cd Books-online-scraper
```

### 2. Créer un environnement virtuel
Créez un environnement virtuel nommé `.venv`, toujours dans le dossier du projet :
```bash
python -m venv .venv
```

### 3. Activer l'environnement virtuel
Activez l'environnement virtuel pour utiliser une version isolée de Python et des bibliothèques :
- Sur Windows :
```bash
  .venv\Scripts\activate
```

- Sur macOS/Linux :
```bash
  source .venv/bin/activate
```

Une fois activé, votre invite de commande affichera `(.venv)` pour indiquer que vous êtes dans l'environnement virtuel.

### 4. Installer les dépendances
Installez les bibliothèques nécessaires listées dans `requirements.txt` :
```bash
pip install -r requirements.txt
```
Le fichier `requirements.txt` contient :
```
requests==2.32.4
beautifulsoup4==4.13.4
```
Cela installe `requests`, `beautifulsoup4`, et leurs dépendances.

### 5. Exécuter le script
Exécutez le script principal pour scraper les données et télécharger les images :
```bash
python script.py
```

### Résultats
- Les données extraites sont enregistrées dans `nom_de_category.csv` avec un fichier par catégorie.
- Les images téléchargées sont stockées dans le dossier `images/`, et chaque image dans le sous dossier correspondant à la catégorie du livre.

## Structure du dépôt
- `script.py` : Le script principal de scraping.
- `requirements.txt` : Liste des dépendances nécessaires.
- `README.md` : Ce fichier, expliquant l'installation et l'exécution.
- `.gitignore` : Exclut l'environnement virtuel (`.venv/`), les fichiers CSV (`*.csv`), les images (`images/`), et les fichiers temporaires (`__pycache__/`, `desktop.ini`).

## Auteur
Réda Abdi pour le projet "Utilisez les bases de Python pour l'analyse de marché" dans la formation "Développeur d'applications python" de OpenClassrooms.