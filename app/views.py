from app import app, db
from app.models import Paper, Task
from app import controllers
import flask
from werkzeug.utils import secure_filename
import os
import random
import string

#from sqlalchemy import create_engine

# ---------- views ----------
def generate_filename(file_name):
    extension = file_name.split('.')[-1]
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(20)) + '.' + extension


@app.route('/task', methods=['POST'])
def test_upload2():
    # check if the post request has the file part
    file = flask.request.files['file']
    task_name = flask.request.form.get('task_name', 'My task')
    source = flask.request.form.get('source', 'ERROR')
    target = flask.request.form.get('target', 'ERROR')

    if file.filename == '':
        resp = flask.jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file: # and allowed_file(file.filename):
        new_random_name = generate_filename(file.filename)
        new_path = os.path.join(app.config['APP_MEDIA'], secure_filename(new_random_name))
        file.save(new_path)
        # add new task 
        task = Task(task_name, new_path, source, target)
        db.session.add(task)
        db.session.commit()
        # start task
        out = task.to_json()
        controllers.start_task.apply_async(args=[task.id], countdown=5)
        db.session.close()  
        return flask.make_response({'message': 'ok', 'task': out}, 200)

    return flask.make_response({'message': 'something went wrong'}, 200)


@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id=None):
    if task_id is None:
        return flask.make_response({'message': 'not found'}, 404) 
    task = db.session.query(Task).filter(Task.task_id==task_id).first()
    if task is None:
        return flask.make_response({'message': 'not found'}, 404)
    return flask.make_response({'message': 'ok', 'task': task.to_json()}, 200)