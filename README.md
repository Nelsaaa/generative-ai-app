

# IA Générative

Ce projet utilise Flask pour le backend et React pour le frontend afin de générer des histoires et des images à l'aide de l'API OpenAI.

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.7 ou supérieur
- Node.js (avec npm) version 14 ou supérieur
- Git

## Configuration du Projet

### 1. Cloner le dépôt

Clonez le dépôt GitHub sur votre machine locale en utilisant la commande suivante :

```sh
git clone https://github.com/votre-utilisateur/votre-repo.git
cd votre-repo
```

### 2. Configuration du Backend (Flask)

#### Créer et activer un environnement virtuel

```sh
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
```

#### Installer les dépendances

```sh
pip install -r requirements.txt
```

#### Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet et ajoutez les variables suivantes :

```
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```

Remplacez `your_secret_key` par une clé secrète pour Flask et `your_openai_api_key` par votre clé API OpenAI.

#### Exécuter le serveur Flask

```sh
flask run
```

### 3. Configuration du Frontend (React)

#### Naviguer vers le dossier du frontend

```sh
cd frontend
```

#### Installer les dépendances

```sh
npm install
```

#### Démarrer le serveur de développement

```sh
npm start
```

### 4. Accéder à l'application

Ouvrez votre navigateur et accédez à `http://localhost:3000` pour utiliser l'application React. Le backend Flask sera disponible sur `http://127.0.0.1:5000`.

## Contribution

Pour contribuer au projet, suivez les étapes ci-dessous :

### 1. Créer une nouvelle branche

Avant de commencer à travailler sur une nouvelle fonctionnalité ou à corriger un bug, créez une nouvelle branche :

```sh
git checkout -b nom-de-votre-branche
```

### 2. Faire des commits

Ajoutez et validez vos modifications avec des messages de commit clairs et concis :

```sh
git add .
git commit -m "Description des modifications"
```

### 3. Pousser vos modifications

Poussez vos modifications sur votre branche distante :

```sh
git push origin nom-de-votre-branche
```

### 4. Créer une Pull Request

Allez sur GitHub, trouvez votre dépôt, et créez une Pull Request pour que vos modifications soient revues et fusionnées dans la branche principale.

## Déploiement

Pour déployer l'application, suivez les instructions spécifiques de votre service d'hébergement. Assurez-vous que les variables d'environnement nécessaires sont configurées dans votre environnement de production.

## Ressources Utiles

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation React](https://reactjs.org/)
- [API OpenAI](https://beta.openai.com/docs/)

---

Avec ce guide, vos collaborateurs devraient pouvoir configurer et lancer le projet sur leur machine, ainsi que contribuer efficacement en utilisant Git.