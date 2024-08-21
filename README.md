# EpicEvent

## Description
EpicEvent est une application de gestion d'événements conçue pour faciliter le suivi et la coordination des clients, contrats et événements au sein de votre entreprise. L'application utilise une base de données SQL pour stocker et gérer les informations essentielles de manière sécurisée et efficace.

## Prérequis

### 1. Installation de Python
Assurez-vous que Python 3.7 ou une version supérieure est installé sur votre système.

**Vérification de la version de Python :**
```bash
python --version
```

### 2. Création d'un environnement virtuel
Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

**Création et activation de l'environnement virtuel :**

- Sur Windows :
```bash
python -m venv env
env\Scripts\activate
```

- Sur macOS/Linux :
```bash
python -m venv env
source env/bin/activate
```

### 3. Installation des dépendances

Toutes les dépendances nécessaires sont listées dans le fichier requirements.txt.

Installez les dépendances avec la commande suivante :
```bash
pip install -r requirements.txt
```

## Configuration de la base de données

### 1. Préparation de la base de données

Assurez-vous d'avoir un serveur SQL installé et opérationnel sur votre machine ou accessible depuis celle-ci. Ce projet est compatible avec les bases de données suivantes :

MySQL

**Création de la base de données :**
Créez une base de données vide nommée **epicevent** à l'aide de votre outil de gestion de base de données préféré.

### 2. Hachage du mot de passe avec Argon2

Pour des raisons de sécurité, les mots de passe des utilisateurs doivent être hachés avant d'être stockés dans la base de données.

Procédure pour hacher un mot de passe :
- Assurez-vous que l'environnement virtuel est activé et que les dépendances sont installées.
- Exécutez le script suivant en remplaçant votre_mot_de_passe par le mot de passe souhaité.

```bash
from argon2 import PasswordHasher

def hash_password(password):
    ph = PasswordHasher()
    return ph.hash(password)

if __name__ == "__main__":
    password = "votre_mot_de_passe"
    hashed_password = hash_password(password)
    print(f"Mot de passe haché : {hashed_password}")
```

Copiez le mot de passe haché généré.

### 3. Mise à jour du fichier Base_SQL.sql

Une fois que vous avez obtenu le mot de passe haché, vous devez l'insérer dans le fichier Base_SQL.sql.

Étapes :
- Ouvrez le fichier Base_SQL.sql avec un éditeur de texte.
- Remplacez 'VotreNom', 'VotreNom@domaine.com', 'MotDePasse'. (par le mot de passe haché que vous avez généré).
- Enregistrez et fermez le fichier.

### 4. Initialisation de la base de données

Après avoir mis à jour le fichier Base_SQL.sql, exécutez-le pour créer les tables et les données nécessaires dans la base de données.

```bash
mysql -u votre_utilisateur -p epicevent < Base_SQL.sql
```

```bash
psql -U votre_utilisateur -d epicevent -f Base_SQL.sql
```

## Démarrage de l'application

### 1. Configuration des variables d'environnement
Fichier `cle.py`
Ce fichier contient une clé spécifique utilisée pour l'intégration avec Sentry.
**Contenu du fichier `cle.py` :** CLE = "xxxxxxxxxxxxxxxxxxxxxxxx"
Créez ce fichier à la racine du projet.

Fichier `config.py`
Ce fichier contient les informations de connexion à la base de données. Les valeurs par défaut peuvent être remplacées par des variables d'environnement.


```bash
import os

DB_USER = os.getenv('DB_USER', 'mon_utilisateur')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mon_mot_de_passe')
DB_HOST = os.getenv('DB_HOST', 'mon_hote')
DB_NAME = os.getenv('DB_NAME', 'mon_nom_de_base_de_donnees')
```
Créez ce fichier a cette adresse : app\utils\config.py

### 2. Lancement de l'application

```bash
python main.py
```

Utilisation de l'application
- Connectez-vous avec les identifiants de l'utilisateur initial que vous avez configuré.
- Naviguez à travers les différentes sections pour gérer les clients, contrats et événements.
- Utilisez les fonctionnalités d'ajout, de modification et de suppression selon vos besoins.