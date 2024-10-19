from flask import Blueprint, url_for, redirect

app_blueprint = Blueprint('app', __name__)

@app_blueprint.route("/")
def index():
    return redirect(url_for('user.login'))