from flask import Blueprint, request, render_template, redirect, url_for, Response
from utils.db import LearningDB

# create app
app = Blueprint('learning', __name__, template_folder='templates')
db = LearningDB()

@app.route('/')
def index():
    learning_list = db.getFormattedTable()
    return render_template('learning.html', learning_list=learning_list)

@app.route('/edit-entry', methods=['GET', 'POST'])
def edit_entry():
    if request.method == 'GET':
        new = False
        entry = None
        links = []
        if 'id' in request.args.keys():
            new = True
            entry, links = db.getEntry(request.args['id'])
            # update last viewed
            db.updateLastViewed(request.args['id'])
        else:
            entry = {'id': -1, 'artist': '', 'album': '', 'track': '', 'instrument': '', 'reason': ''}
        return render_template('edit_entry.html', new=new, entry=entry, links=links)
    else: # POST
        if 'delete' in request.form.keys():
            db.deleteEntry(request.form['id'])
        elif request.form['id'] == '-1':
            db.insertEntry(
                request.form['artist'], request.form['album'], request.form['track'], request.form['instrument'],
                request.form['reason'], '1' if 'backlog' in request.form else '0'
            )
        else:
            db.updateEntry(
                request.form['artist'], request.form['album'], request.form['track'], request.form['instrument'],
                request.form['reason'], '1' if 'backlog' in request.form else '0', request.form['id']
            )
        return redirect(url_for('root.learning.index'))
    
@app.route('/edit-link', methods=['GET', 'POST'])
def edit_link():
    if request.method == 'GET':
        new = False
        link = None
        if 'id' in request.args.keys():
            new = True
            link = db.getLink(request.args['id'])
        else:
            link = {'id': -1, 'type': '', 'url': '', 'description': '', 'learning_id': request.args['learning_id']}
        return render_template('edit_link.html', new=new, link=link)
    else: # POST
        if 'delete' in request.form.keys():
            db.deleteLink(request.form['id'])
        elif request.form['id'] == '-1':
            db.insertLink(
                request.form['type'], request.form['url'], request.form['description'], request.form['learning_id']
            )
        else:
            db.updateLink(
                request.form['type'], request.form['url'], request.form['description'], request.form['id']
            )
        return redirect(url_for('root.learning.index'))

@app.route('/viewed', methods=['POST'])
def viewed():
    db.updateLastViewed(request.form['id'])
    return Response(status=200)
