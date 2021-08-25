from app import app, db
from app.models import Paper
from app import controllers
import flask
#from sqlalchemy import create_engine


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