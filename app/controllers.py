from app import app, celery, db
from app.models import Paper


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
def task(file_path, source, target):
    """
    Asynchronus task that combines all functions above.
    """
    print("this is async")
    import sys
    sys.stdout.flush()
    pass
