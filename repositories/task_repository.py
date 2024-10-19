from configurations.database import db
from sqlalchemy import text

from models.task_model import Task
from models.user_model import User


class TaskRepository:
    @staticmethod
    def get_all_tasks(user_id):
        query = text("SELECT * FROM tasks WHERE user_id = :user_id")
        result = db.session.execute(query, {'user_id': user_id})
        return result.fetchall()
    
    @staticmethod
    def add_task(conteudo, user_id, prioridade="Média"):
        query = text("""
            INSERT INTO tasks (conteudo, completa, prioridade, user_id)
            VALUES (:conteudo, :completa, :prioridade, :user_id)
        """)
        
        db.session.execute(query, {
            'conteudo': conteudo,
            'completa': False,
            'prioridade': prioridade,
            'user_id': user_id
        })
        
        db.session.commit()
        
    @staticmethod
    def complete_task(tarefa_id):
        print(f'>>>>>>>> {tarefa_id}')
        query = text("UPDATE tasks SET completa = TRUE WHERE id = :id")
        db.session.execute(query, {'id': tarefa_id})
        db.session.commit()
        
    @staticmethod
    def delete_task(tarefa_id):
        query = text("DELETE FROM tasks WHERE id = :id")
        db.session.execute(query, {'id': tarefa_id})
        db.session.commit()
        
        
    @staticmethod
    def get_tasks_with_users():
        return db.session.query(Task, User).join(User, Task.user_id == User.id).all()