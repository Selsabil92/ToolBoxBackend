🛠️ ToolBoxPentest - Backend API
ToolBoxPentest** est une API backend développée en **Python (Flask)**. Elle constitue le cœur d’une **boîte à outils offensive** destinée aux tests d’intrusion (pentest). Ce backend permet de **lancer, enregistrer et centraliser** différents types de scans réseau et applicatif, tout en intégrant des **services d’analyse et de réponse automatisée**.


🚀 Fonctionnalités

- Lancement de scans automatisés : **Hydra**, **OpenVAS**, **Nmap**, etc.
- Récupération et enregistrement des résultats de scan
- Gestion des utilisateurs avec authentification sécurisée (JWT)
- Architecture modulaire (routes, services, modèles bien séparés)
- Intégration à une base de données **PostgreSQL**
- Migrations de base de données avec **Alembic**
- Déploiement simplifié via **Docker / Docker Compose**

🧪 Technologies utilisées  

<img src="https://i.ibb.co/Kxw95RbJ/Techno.webp" alt="Technologies utilisées" width="500"/>

📁 Structure du projet
ToolBoxBackend/
├── app/
│ ├── routes/ # Fichiers de routing de l'API (ex: /scan/nmap, /auth/login)
│ ├── services/ # Logique métier : exécution de scans, analyse, etc.
│ ├── models/ # Modèles SQLAlchemy pour la BDD
│ └── app.py # Point d’entrée principal (serveur Flask)
│
├── alembic/ # Répertoire de gestion des migrations
├── Dockerfile # Image Docker du backend
├── docker-compose.yml # Orchestration backend + base PostgreSQL
├── requirements.txt # Liste des dépendances Python
├── .env.example # Exemple de configuration (.env)
└── README.md # Documentation du projet

⚙️ Installation

 1. Cloner le projet
git clone https://github.com/Selsabil92/ToolBoxBackend.git
cd ToolBoxBackend

 3. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

4. Installer les dépendances
pip install -r requirements.txt

5. Configurer les variables d’environnement
Créer un fichier .env à la racine du projet avec :
DATABASE_URL=postgresql://postgres:ToolBoxPentest@localhost:5432/toolbox
SECRET_KEY=ToolBoxPentestSecure
 
 6. Appliquer les migrations de base de données
alembic upgrade head

7. Lancer l'application
python app.py

🐳 Utilisation avec Docker (optionnel)
Si vous préférez utiliser Docker :
docker-compose up --build
Cela lancera le backend Flask ainsi que la base PostgreSQL définie dans docker-compose.yml.

🧭 Frontend associé
Une interface React est disponible pour interagir avec l’API :
https://github.com/YohannGHub/frontend1.git

👩‍💻 Auteur
Projet développé par PentestOPS(Selsabil GUENNOUNI, Lucas FOURRAGE, Yohann MATHURINE) dans le cadre du mastère Cybersécurité - Sup de Vinci (2025).
**Ce projet m’a permis de renforcer mes compétences en cybersécurité offensive, d’approfondir ma maîtrise de l’automatisation des tâches et d’adopter une approche rigoureuse en matière de sécurité des systèmes.**

📄 Licence
Ce projet est publié sous la licence MIT.
Usage libre à des fins personnelles, éducatives ou professionnelles.
