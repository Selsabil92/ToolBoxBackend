from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from routes.scan import scan_bp
    app.register_blueprint(scan_bp, url_prefix="/scan")

    return app
