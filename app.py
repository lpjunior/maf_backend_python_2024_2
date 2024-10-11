import os.path
from configurations.database import db
from controllers.task_controller import task_blueprint
from flask import Flask

app = Flask(__name__)
app.register_blueprint(task_blueprint)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir , "task.db")}'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)