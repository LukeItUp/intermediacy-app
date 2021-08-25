from app import app, db
from app.models import Paper, Task
from app import controllers
import flask
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

@app.route('/task', methods=['POST'])
def add_task():
    '''
    Adds new task and accepts file from user.
    '''

    return flask.make_response({'message': 'ok'}, 200)


@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id=None):
    if task_id is None:
        return flask.make_response({'message': 'not found'}, 404) 
    task = db.session.query(Task).filter(Task.task_id==task_id).first()
    if task is None:
        return flask.make_response({'message': 'not found'}, 404) 
    return flask.make_response({'message': 'ok', 'task': task.to_json()}, 200)