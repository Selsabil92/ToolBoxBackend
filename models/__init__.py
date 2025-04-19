from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Si l'erreur persiste, essaye d'importer comme suit :
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)
