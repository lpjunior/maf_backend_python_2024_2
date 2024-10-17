from sqlalchemy import text
from models.user_model import User

# Função para criar a tabela tasks usando SQL no lugar da função db.create_all()
def create_table_tasks(app, db):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        conteudo VARCHAR(200) NOT NULL,
        completa BOOLEAN DEFAULT FALSE,
        prioridade VARCHAR(50) NOT NULL DEFAULT 'Média'
    );
    
    ALTER TABLE tasks ADD COLUMN IF NOT EXISTS user_id INTEGER NOT NULL REFERENCES users(id);
       
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.table_constraints
             WHERE constraint_type = 'FOREIGN KEY'
             AND table_name = 'tasks'
             AND constraint_name = 'fk_user_id'     
        ) THEN
            ALTER TABLE tasks ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
        END IF;
    END $$;
    ''' 
    
    with app.app_context():
        db.session.execute(text(create_table_sql))
        db.session.commit()
        print("Tabela 'tasks' criada com sucesso!")


# Função para criar a tabela users
def create_table_users(app, db):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(80) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE
    );
    ALTER TABLE users ADD COLUMN IF NOT EXISTS active BOOLEAN DEFAULT TRUE;
    '''

    with app.app_context():
        db.session.execute(text(create_table_sql))
        db.session.commit()
        print("Tabela 'users' criada com sucesso!")

# Função para criar o usuário root
def create_root_user(app, db):
    with app.app_context():
        
        # Verificando se o usuário root existe
        root_user = User.query.filter_by(username="root").first()

        if not root_user:
            root_user = User(username="root", is_admin=True)
            root_user.set_password("root@123")
            db.session.add(root_user)
            db.session.commit()
            print("Usuário 'root' criado com sucesso!")
        else:
            print("Usuário 'root' já existe!")