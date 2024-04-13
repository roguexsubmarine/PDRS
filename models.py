from datetime import datetime
from app import db
from flask_login import UserMixin,LoginManager

'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),unique=True, nullable=False)
    email= db.Column(db.String(120),unique=True, nullable=False)
    password=db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return f"User('{self.name}','{self.email}')"
    

