# 🔐 Toolbox Pentest - Backend

Bienvenue dans le backend de la **Toolbox Pentest** 🛠️💻, une application automatisée pour les tests d'intrusion et la gestion des résultats. Ce backend fournit des fonctionnalités telles que l'exécution de scans de sécurité, la gestion des utilisateurs, et l'intégration avec des outils comme Nmap, Hydra, et bien d'autres.

## 🚀 Fonctionnalités

- **💻 Exécution de scans** : Lance des tests de sécurité sur des cibles à l'aide de Nmap, Hydra et autres outils.
- **🔒 Authentification** : Utilisation de JWT pour sécuriser les accès à l'API.
- **📊 Gestion des résultats** : Suivi des résultats des scans avec possibilité de génération de rapports.
- **📦 Notifications** : Système de notifications pour tenir l'utilisateur informé des résultats des scans.
- **⚙️ Connexion SSH** : Test de la connexion et exécution de commandes à distance via SSH.

## 📦 Installation

### Prérequis

1. Python 3.9+ installé sur votre machine.
2. PostgreSQL ou une autre base de données configurée.
3. Clé JWT pour sécuriser l'authentification.

### Installation des dépendances

Clonez ce dépôt et installez les dépendances via `pip` :
```bash
git clone https://github.com/selsabil92/toolbox-pentest.git
cd toolbox-pentest/backend
pip install -r requirements.txt
