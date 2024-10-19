from flask import Flask
from configurations.blueprints import register_blueprints
from configurations.database import db
from configurations.config import Config
from configurations.sql_commands import create_table_tasks, create_table_users, create_root_user

app = Flask(__name__)

# Carrega as configurações da classe config
app.config.from_object(Config)

# Inicializar a conexão com o banco de dados
db.init_app(app)

# Registra os blueprints
register_blueprints(app)

if __name__ == '__main__':
    create_table_tasks(app, db)
    create_table_users(app, db)
    create_root_user(app, db)
    app.run(debug=Config.DEBUG)