from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(test_config=None):
    from flask_migrate import Migrate
    from flask_cors import CORS
    from config import Config
    from app.models import User, Board, Column, Task

    from .routes.board import board_bp
    from .routes.column import column_bp
    from .routes.task import task_bp
    from .routes.user import user_bp

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
    
    app.register_blueprint(board_bp, url_prefix = "/api/users")
    app.register_blueprint(column_bp, url_prefix = "/api")
    app.register_blueprint(task_bp, url_prefix = "/api")
    app.register_blueprint(user_bp, url_prefix = "/api")

    return app

