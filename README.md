# ⚡ Application de l'Emploi du Temps Intelligent - IGEE

Cette application interactive a été développée spécifiquement pour l'**Institut National de l'Électronique et du Génie Électrique (IGEE - ex INElec, Boumerdès)**. Elle permet aux étudiants et aux enseignants de consulter l'emploi du temps de manière dynamique et visuelle pour les **16 sections** de l'institut.

## 🎨 Fonctionnalités Principales
- **Filtres Avancés :** Recherche rapide par Section (Groupe), par Enseignant ou par Salle de cours/Amphi.
- **Code Couleur Intelligent :** Distinction visuelle immédiate entre les cours (Vert), les TD (Bleu) et les TP en laboratoires (Jaune).
- **Suivi en Temps Réel 🚨 :** Détection automatique de l'heure actuelle avec mise en valeur de la séance en cours (en Rouge) pour savoir instantanément où vous devez vous rendre.

## 🚀 Comment lancer l'application en local
Si vous souhaitez exécuter cette application sur votre ordinateur, suivez ces étapes dans votre terminal :

1. **Installer les dépendances nécessaires :**
   ```bash
   pip install -r requirements.txt
   ```

2. **Lancer l'application avec Streamlit :**
   ```bash
   streamlit run app.py
   ```

## 📱 Installation sur Téléphone (Android / iOS)
L'application est configurée comme une **PWA (Progressive Web App)**. Pour l'installer sur votre écran d'accueil sans passer par les stores :
- **Sur Android (Chrome) :** Ouvrez le lien de l'application, cliquez sur les 3 points en haut à droite, puis sélectionnez **"Ajouter à l'écran d'accueil"**.
- **Sur iOS (Safari) :** Ouvrez le lien, cliquez sur l'icône de partage (flèche vers le haut), puis sélectionnez **"Sur l'écran d'accueil"**.
