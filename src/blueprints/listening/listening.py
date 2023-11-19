import os
from flask import Blueprint, request, render_template, redirect, url_for
from utils.db import connection, ListeningDB

# create app
app = Blueprint('listening', __name__, template_folder='templates')
db = ListeningDB()

@app.route('/')
def index():
    list = db.getEntries()
    return render_template('listening.html', listening_list=list)
