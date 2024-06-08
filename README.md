
# Guide pour lancer le projet sur VS Code

## Étapes à suivre :

1. **Cloner le dépôt depuis GitHub :**
   - Ouvrez votre terminal.
   - Utilisez la commande `git clone` suivie de l'URL du dépôt GitHub pour cloner le projet localement.
     ```sh
     git clone https://github.com/Nelsaaa/generative-ai-app.git
     ```

2. **Accéder au répertoire du projet :**
   - Utilisez la commande `cd` pour accéder au répertoire du projet cloné.
     ```sh
     cd generative-ai-app
     ```

3. **Installer les dépendances du projet :**
   - Assurez-vous d'avoir Python et Node.js installés sur votre machine.
   - Utilisez les commandes suivantes pour installer les dépendances Python et Node.js :
     ```sh
     # Installation des dépendances Python
     pip install -r requirements.txt

     # Installation des dépendances Node.js
     npm install
     ```

4. **Ouvrir le projet dans VS Code :**
   - Utilisez la commande suivante pour ouvrir le projet dans VS Code :
     ```sh
     code .
     ```

5. **Lancer le serveur Flask :**
   - Dans VS Code, ouvrez le fichier `app.py`.
   - Utilisez le menu ou la commande pour exécuter le fichier `app.py`.
   - Alternativement, vous pouvez exécuter le serveur Flask à partir du terminal avec la commande suivante :
     ```sh
     python app.py
     ```

6. **Lancer l'application front-end :**
   - Ouvrez un nouveau terminal dans VS Code.
   - Utilisez la commande suivante pour démarrer l'application front-end :
     ```sh
     npm start
     ```

7. **Accéder à l'application :**
   - Ouvrez votre navigateur web et accédez à l'URL suivante :
     ```
     http://localhost:3000
     ```

---

Ce guide devrait aider votre collaborateur à démarrer le projet sur VS Code. N'hésitez pas à le personnaliser ou à ajouter des détails supplémentaires selon les besoins spécifiques de votre projet.