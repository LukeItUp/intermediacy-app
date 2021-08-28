from app import app, celery, db
from app.models import Paper, Task


def find_doi(line):
    flag = False
    for word in line.split(' '):
        if 'doi' == word.lower():
            flag = True
        elif flag:
            return word.replace("'", '').replace('"', '')
    return ''


def gather_network_data(file_path):
    file_name = '.'.join(file_path.split('.')[:-1])
    output_file = open(f'{file_name}-extended.net', 'w')
    node_flag = False
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if 'vertices' in line:
                node_flag = True
            elif 'arcs' in line:
                node_flag = False
            if node_flag:
                doi = find_doi(line)
                paper = db.session.query(Paper).filter(Paper.doi == doi).first()
                if paper is None:
                    paper = Paper(doi)
                    paper.gather_data()
                    db.session.add(paper)
                line = f'{line} title "{paper.title}" year {paper.year} ms_id {paper.ms_id} fields {paper.get_fields()}'
                db.session.commit()
                db.session.close()
            output_file.write(line + '\n')
    output_file.close()


def compute_intermediacy(file_path, source, target):
    """
    Computes extended intermediacy and saves the results to db.
    """
    file_name = '.'.join(file_path.split('.')[:-1])
    command = f'java -jar {file_name}-extended.net "{source}" "{target}" > {file_name}-results.json'
    # TODO: run java code
    pass


@celery.task
def start_task(task_id):
    """
    Asynchronus task that combines all functions above.
    """
    task = db.session.query(Task).filter(Task.id==task_id).first()
    task.status = 'gathering'
    print(task)
    db.session.commit()
    gather_network_data(task.file_path)

    task = db.session.query(Task).filter(Task.id==task_id).first()
    task.status = 'processing'
    print(task)
    db.session.commit()
    compute_intermediacy(task.file_path, task.source, task.target)
    
    task = db.session.query(Task).filter(Task.id==task_id).first()
    task.status = 'done'
    print(task)
    db.session.commit()
    db.session.close()
    return
