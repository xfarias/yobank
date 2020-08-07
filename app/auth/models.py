from app import db
from flask_login import UserMixin


# Definindo a base user
class User(UserMixin, db.Document):
    meta = {'collection': 'user'}
    username = db.StringField(max_length=30)
    password = db.StringField()
    own = db.FloatField(required=True)
    debt = db.FloatField(required=True)

  

