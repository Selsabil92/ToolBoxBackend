🛠️ ToolBoxPentest - Backend API
ToolBoxPentest est un backend API développé en Python avec Flask. Il constitue le cœur d’une boîte à outils offensive destinée aux tests d’intrusion (pentest). Ce backend permet de lancer, enregistrer et centraliser différents types de scans de sécurité réseau ou applicatif, tout en intégrant des services d’analyse et de réponse automatisée.

🚀 Fonctionnalités
•	Lancement de scans automatisés : Hydra, OpenVAS, Nmap, etc.
•	 Récupération et enregistrement des résultats
•	Gestion des utilisateurs et authentification sécurisée
•	Intégration à une base de données PostgreSQL
•	Architecture modulaire : séparation claire des services, routes, modèles
•	 Migrations de base de données avec Alembic
•	 Déploiement via Docker / Docker Compose

🧪 Technologies utilisées
![Technologies utilisées](https://raw.githubusercontent.com/Selsabil92/ToolBoxBackend/main/assets/technologies.png)

📁 Structure du projet
ToolBoxBackend/
├── app/
│   ├── routes/           # Fichiers de routing API
│   ├── services/         # Logique métier : scans, analyse, etc.
│   ├── models/           # Définition des modèles de données
│   ├── schemas/          # Schémas de validation
│   └── app.py            # Point d’entrée Flask
├── alembic/              # Répertoire des migrations
├── Dockerfile            # Image backend
├── docker-compose.yml    # Orchestration backend + base de données
├── requirements.txt      # Dépendances Python
├── .env.example          # Exemple de fichier de configuration
└── README.md             # Documentation du projet

⚙️ Installation

 1. Cloner le projet
git clone https://github.com/Selsabil92/ToolBoxBackend.git
cd ToolBoxBackend
 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
3. Installer les dépendances
bash
CopierModifier
pip install -r requirements.txt
 4. Configurer les variables d’environnement
Créer un fichier .env à la racine du projet avec :
DATABASE_URL=postgresql://postgres:ToolBoxPentest@localhost:5432/toolbox
SECRET_KEY=ToolBoxPentestSecure
 5. Appliquer les migrations de base de données
alembic upgrade head
6. Lancer l'application
python app.py
🐳 Utilisation avec Docker (optionnel)
Si vous préférez utiliser Docker :
docker-compose up --build
Cela lancera le backend Flask ainsi que la base PostgreSQL définie dans docker-compose.yml.

👩‍💻 Auteur
Projet développé par PentestOPS dans le cadre du mastère Cybersécurité - Sup de Vinci (2025).

