from app import app, celery, db
from app.models import Paper


def induce_network(file_path, source, target):
    """
    To speed up the whole process, this function induces the network to contain only relevant nodes eg. from source to target.
    This function might not be needed.
    """
    pass


def gather_network_data():
    """
    Gathers additional paper data for computing the extended intermediacy measure.
    """
    pass


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
