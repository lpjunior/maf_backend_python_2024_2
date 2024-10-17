from flask import Flask
from configurations.database import db
from configurations.sql_commands import create_table_tasks, create_table_users, create_root_user
from controllers.task_controller import task_blueprint
from controllers.user_controller import user_blueprint
from dotenv import load_dotenv
from urllib.parse import quote
import os

# Carregar as variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Registra os blueprints
app.register_blueprint(task_blueprint)
app.register_blueprint(user_blueprint)

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

password = quote(password)

# COnfigura a string de conexão com o banco de daados PostgreSQL (via Supabase)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

if __name__ == '__main__':
    create_table_tasks(app, db)
    create_table_users(app, db)
    create_root_user(app, db)
    app.run(debug=True)