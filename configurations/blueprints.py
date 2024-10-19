from controllers.app_controller import app_blueprint
from controllers.task_controller import task_blueprint
from controllers.user_controller import user_blueprint

def register_blueprints(app):
    app.register_blueprint(task_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(app_blueprint)