import os
from flask import Flask, Blueprint, render_template
from blueprints.listening.listening import app as listening_app
from blueprints.learning.learning import app as learning_app

# register blueprints to a root blueprint
root = Blueprint('root', __name__, template_folder='templates')
root.register_blueprint(listening_app, url_prefix='/listening')
root.register_blueprint(learning_app, url_prefix='/learning')

@root.route('/')
def index():
    return render_template('index.html')

# create main app and register root blueprint to url_prefix
app = Flask(__name__)
app.register_blueprint(root, url_prefix=os.environ['URL_PREFIX'])
