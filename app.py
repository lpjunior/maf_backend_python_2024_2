from flask import Flask
from configurations.database import db
from controllers.task_controller import task_blueprint
from urllib.parse import quote
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)
app.register_blueprint(task_blueprint)

print(os.getenv('DB_NAME'))

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

password = quote(password)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)