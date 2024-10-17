from models.user_model import User
from configurations.database import db

class UserRepository:
    
    @staticmethod
    def create_user(username, password):
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def list_users():
        return User.query.all()
    
    @staticmethod
    def deactivate_user(user_id):
        user = UserRepository.find_by_id(user_id)
        if user:
            user.active = False
            db.session.commit()