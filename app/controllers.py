from app import app, celery, db
from app.models import Paper, Task


def induce_network(file_path, source, target):
    """
    To speed up the whole process, this function induces the network to contain only relevant nodes eg. from source to target.
    This function might not be needed.
    """
    pass


def find_doi(line):
    flag = False
    for word in line.split(' '):
        if 'doi' is word.lower():
            flag = True
        elif flag:
            return word.replace("'", '').replace('"', '')
    return ''


def gather_network_data(file_path):
    """
    Gathers additional paper data for computing the extended intermediacy measure.
    """
    with open(file_path, 'r') as file:
        for line in file:
            if 'vertices' in line:
                continue
            elif 'arcs' in line:
                break
            else:
                doi = find_doi(line)
                paper = Paper(doi)
                paper.gather_data()
                db.session.add(paper)
        db.session.commit()
        db.session.close()


def compute_intermediacy(file_path, source, target):
    """
    Computes extended intermediacy and saves the results to db.
    """
    pass


@celery.task
def start_task(task_id):
    """
    Asynchronus task that combines all functions above.
    """

    import time
    time.sleep(5)  #TODO: remove
    task = db.session.query(Task).filter(Task.id==task_id).first()
    task.status = 'gathering'
    print(task)
    db.session.commit()
    induce_network(task.file_path, task.source, task.target)
    gather_network_data(task.file_path)

    time.sleep(5)   #TODO: remove
    task = db.session.query(Task).filter(Task.id==task_id).first()
    task.status = 'processing'
    print(task)
    db.session.commit()
    compute_intermediacy(task.file_path, task.source, task.target)
    
    time.sleep(5)  #TODO: remove
    task = db.session.query(Task).filter(Task.id==task_id).first()
    task.status = 'done'
    print(task)
    db.session.commit()
    db.session.close()
    return
