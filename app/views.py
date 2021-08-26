from app import app, db
from app.models import Paper, Task
from app import controllers
import flask
from werkzeug.utils import secure_filename
import os
import random
import string

#from sqlalchemy import create_engine

# ---------- test views ----------

@app.route('/test_download', methods=['GET'])
def test_download():
    test_doi = ["10.1016/J.PHYSA.2011.12.021",
                "10.1016/J.JOI.2015.11.007",
                "10.1016/J.KNOSYS.2014.07.007"]

    for doi in test_doi:
        paper = Paper(doi)
        paper.gather_data()
        db.session.add(paper)
    db.session.commit()
    db.session.close()
    return flask.make_response({'message': 'ok'}, 200)


@app.route('/show', methods=['GET'])
def get_test():
    results = db.session.query(Paper).filter(Paper.ms_id!=None).all()
    results = [x.to_json() for x in results]
    db.session.close()
    controllers.task.apply_async(args=[None, None, None], countdown=0)
    return flask.make_response({'message': 'ok', 'results': results}, 200)


@app.route('/test_task', methods=['GET'])
def test_task():
    task = Task('path/to/file', 'source', 'target')
    db.session.add(task)
    db.session.commit()
    db.session.close()
    return flask.make_response({'message': 'ok'}, 200)


@app.route('/any_tasks', methods=['GET'])
def any_tasks():
    task = db.session.query(Task).first()
    db.session.close()
    out = {
        'id': task.id,
        'task_id': task.task_id,
        'file_path': task.file_path,
        'source': task.source,
        'target': task.target
    }
    return flask.make_response({'message': 'ok', 'task': out}, 200)


# ---------- views ----------
def generate_filename(file_name):
    extension = file_name.split('.')[-1]
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(20)) + '.' + extension


@app.route('/task', methods=['POST'])
def add_task():
    '''
    Adds new task and accepts file from user.
    '''
    current_chunk = int(flask.request.form.get('current_chunk', None))
    chunk_count = int(flask.request.form.get('chunk_count', None))
    chunk_offset = int(flask.request.form.get('chunk_byte_offset', None))
    total_file_size = int(flask.request.form.get('total_file_size', None))

    source = flask.request.form.get('source', None)
    target = flask.request.form.get('target', None)

    file_name = flask.request.files.get('file_name', 'tmp.net')
    file_content = flask.request.files.get('file', None)

    file_path = os.path.join(app.config['APP_MEDIA'], secure_filename(file_name))

    if os.path.exists(file_path) and current_chunk == 0:
        os.remove(file_path)

    append_write = 'ab' if os.path.exists(file_name) else 'wb'
    with open(file_path, append_write) as f:
        f.seek(chunk_offset)
        f.write(file_content.stream.read())

    if current_chunk != chunk_count:
        return flask.make_response(jsonify({'message': 'ok',
                                            'file_name': file_name,
                                            'current_chunk': current_chunk,
                                            'total_chunks': total_chunks}), 200)
    else:  # finish upload
        if os.path.getsize(file_path) != total_file_size: # something is wrong with uploaded file
            os.remove(file_path)
            return flask.make_response({'message': 'size mismatch'}, 500)
        else:
            new_random_name = generate_filename(file_name)
            new_path = os.path.join(app.config['APP_MEDIA'], secure_filename(new_random_name))
            os.rename(file_path, new_path)
            # add new task 
            task = Task(new_path, source, target)
            db.session.add(task)
            db.session.commit()
            db.session.close()
            # TODO: start task

    return flask.make_response({'message': 'ok'}, 200)


@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id=None):
    if task_id is None:
        return flask.make_response({'message': 'not found'}, 404) 
    task = db.session.query(Task).filter(Task.task_id==task_id).first()
    if task is None:
        return flask.make_response({'message': 'not found'}, 404)
    return flask.make_response({'message': 'ok', 'task': task.to_json()}, 200)