from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    done = db.Column(db.Boolean,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    # Relationship (optional, helps with easier access in Python)
    user = db.relationship('User',backref='tasks',lazy=True)

    def to_dict(self):
        """Convert Model instance into dictionary for JSON responses."""
        return {
            'id':self.id,
            'title':self.title,
            'done':self.done,
            'user_id':self.user_id
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    password_hash = db.Column(db.String(200),nullable=False)

    def set_password(self,password):
        """Hashed the password before storing"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        """Verifies the password"""
        return check_password_hash(self.password_hash,password)

class BlackListedToken(db.Model):
    __tablename__ = 'blacklisted_tokens'

    id = db.Column(db.Integer,primary_key=True)
    token = db.Column(db.String(500),nullable=False,unique=True)
    blacklisted_on = db.Column(db.DateTime(timezone=True),default=datetime.now)