﻿from flask import Flask

from configurations.sql_commands import create_table_tasks, create_table_users, create_root_user
from configurations.database import db
from controllers.task_controller import task_blueprint
from urllib.parse import quote
import os
from dotenv import load_dotenv

from controllers.user_controller import user_blueprint

# Carregar variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)

app.register_blueprint(task_blueprint)
app.register_blueprint(user_blueprint)

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

password = quote(password)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

if __name__ == '__main__':
    create_table_tasks(app, db)
    create_table_users(app, db)
    create_root_user(app, db)
    app.run(debug=True)