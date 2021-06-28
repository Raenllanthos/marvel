from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default="")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default="", unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, username, id="", password="", token="", g_auth_verify = False):
        self.id = self.set_id()
        self.email = email
        self.username = username
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User: {self.username} has been added to the database"

class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    power = db.Column(db.String, nullable = False)
    is_a_hero = db.Column(db.Boolean, nullable = False)
    comics_appeared_in = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(200), nullable = False)
    back_story = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    owner = db.Column(db.String, db.ForeignKey("user.token"), nullable = False)
    
    def __init__(self, name, power, is_a_hero, comics_appeared_in, description, back_story, owner, id=""):
        self.name = name
        self.power = power
        self.is_a_hero = is_a_hero
        self.comics_appeared_in = comics_appeared_in
        self.description = description
        self.back_story = back_story
        self.owner = owner
        self.id = self.set_id()

    def __repr__(self):
        return f"Hero/Villain: {self.name} has been added!"
    
    def set_id(self):
        return (secrets.token_urlsafe())

# Creation of API Schema via the Marshmallow Object
class HeroSchema(ma.Schema):
    class Meta:
        fields = ["id", "name", "power", "is_a_hero", "comics_appeared_in", "description", "back_story"]

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)