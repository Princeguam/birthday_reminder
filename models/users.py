import db
from flask_login import LoginManager, UserMixin, login_user, login_required
from datetime import datetime, timezone



login_manager = LoginManager()

class User(db.Document,UserMixin):
    username = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    date_joined = db.DateTimeField(default=datetime.now(timezone.utc))

    meta = {"collection":"users"}
   
   
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.username = user_data['username']
