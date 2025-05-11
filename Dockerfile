# Utilise une image officielle de Python
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt ./
COPY . .

# Installe les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose le port de Flask
EXPOSE 5000

# Démarre l'application Flask par défaut (mais on peut aussi lancer celery avec une autre commande dans docker-compose)
CMD ["python", "app.py"]
