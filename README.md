
ToolBoxPentest est un backend API développé en Python avec Flask. Il sert de socle à une boîte à outils offensive pour les tests d'intrusion (pentest).
Ce backend est conçu pour exécuter, enregistrer et centraliser différents types de scans de sécurité réseau ou applicatif, tout en intégrant des services d'analyse et de réponse automatisée.

Fonctionnalités : 
Lancement de scans automatisés (Hydra, OpenVAS, Nmap, etc.)
Récupération et stockage des résultats de scan
Gestion des utilisateurs et authentification
Intégration à une base de données PostgreSQL
Architecture modulaire : services, routes, modèles bien séparés
Migrations gérées avec Alembic
Déploiement via Docker / Docker Compose

Technologies utilisées
Langage : Python 3.11
Framework web : Flask
ORM : SQLAlchemy
Base de données : PostgreSQL
Migrations : Alembic
Sécurité : gestion de mots de passe hashés, utilisation de JWT (si implémentée)
Conteneurisation : Docker, Docker Compose
Outils intégrables : Nmap, Hydra, OpenVAS, ZAP, etc.
Structure modulaire pour la scalabilité et l'intégration facile de nouveaux outils

Structure du projet: 

Installation

Cloner le projet :
  git clone https://github.com/Selsabil92/ToolBoxBackend.git
  cd ToolBoxBackend

Configurer l’environnement virtuel :
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows

Installer les dépendances :

  pip install -r requirements.txt

Configurer les variables d’environnement :

Créer un fichier .env à la racine avec :

  DATABASE_URL=postgresql://postgres:ToolBoxPentest@localhost:5432/toolbox
  SECRET_KEY=ToolBoxPentestSecure

Appliquer les migrations :
  alembic upgrade head

Lancer l'application :
  python app.py

Utilisation via Docker (optionnel) : 
  docker-compose up --build

Auteur
Projet développé par PentestOPS dans le cadre du mastère Cybersécurité - Sup de Vinci (2025)






