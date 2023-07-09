
from flask import Flask
from routes.main import main_bp
from routes.auth import check_bp
from models import Student , user_table 
from commands import create_tables
from extensions import db
from extensions import login_manager
def create_app(config_file = "settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.login_view = 'check.login'
    @login_manager.user_loader
    def load_user(user_id):
        return user_table.query.get(user_id)
    login_manager.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(check_bp)
    # ...
    return app
