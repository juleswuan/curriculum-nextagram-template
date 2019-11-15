from braintree import BraintreeGateway, Configuration, Environment
import config
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from models.base_model import db
from models.user import User
import os


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.new"
login_manager.login_message = "Please log in before proceeding."
login_manager.login_message_category = "warning"

gateway = BraintreeGateway(Configuration(
        Environment.Sandbox,
        merchant_id=os.getenv("MERCHANT_ID"),
        public_key=os.getenv("PUBLIC_KEY"),
        private_key=os.getenv("PRIVATE_KEY")
    ))

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)
