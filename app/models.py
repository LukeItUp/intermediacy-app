
from app import app, db
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column, Integer, String, Text, BigInteger, LargeBinary
import requests
import json
import string
import random


Base = declarative_base()
#engine = create_engine('postgresql+psycopg2://postgres@0.0.0.0:5431/postgres', connect_args={'options': '-csearch_path=crawldb'})

class Paper(Base):
    __tablename__ = 'paper'
    id = Column('id', Integer, primary_key=True)
    ms_id = Column('ms_id', Integer)
    doi = Column('doi', String)
    title = Column('title', String)
    authors = Column('authors', String)
    year = Column('year', Integer)
    fields = Column('fields', String)

    def __init__(self, doi):
        self.doi = doi

    def __str__(self):
        return f'<Paper id={self.id} doi={self.doi}>'
    
    def __repr__(self):
        return self.__str__()

    def set_fields(self, data):
        fields_json = dict()
        data = [x['FN'] for x in data['entities'][0]['F']]
        fields_json['data'] = data
        self.fields = json.dumps(fields_json)

    def get_fields(self):
        if self.fields is None:
            return []
        return json.loads(self.fields)['data']

    def set_authors(self, data):
        authors_json = dict()
        data = [x['AuN'].title() for x in data['entities'][0]['AA']]
        authors_json['data'] = data
        self.authors = json.dumps(authors_json)

    def get_authors(self):
        if self.authors is None:
            return []
        return json.loads(self.authors)['data']

    def gather_data(self):
        query = f"expr=DOI='{self.doi}'&attributes=Id,Ti,AA.AuN,Y,F.FN"
        resp = requests.get(f'https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?{query}&subscription-key={app.config["SUB_KEY"]}')
        data = json.loads(resp.text)
        
        if 'entities' not in data or len(data['entities']) == 0:
            self.ms_id = -1
            return
                
        self.ms_id = int(data['entities'][0]['Id'])
        self.title = str(data['entities'][0]['Ti']).capitalize()
        self.year = str(data['entities'][0]['Y'])
        self.set_fields(data)
        self.set_authors(data)
    
    def to_json(self):
        j = {
            "doi": self.doi,
            "ms_id": self.ms_id,
            "title": self.title,
            "authors": self.get_authors(),
            "year": self.year,
            "fields": self.get_fields()
        }
        return j


class Task(Base):
    '''
    Task status:
        - accepted: Task has been accepted and is ready to gather paper attributes
        - gathering: Task is gathering additional paper attributes
        - processing: Extended intermediacy of the network is being calculated
        - done: Task is finished and results are ready 
    '''
    __tablename__ = 'task'
    id = Column('id', Integer, primary_key=True)
    task_id = Column('task_id', String)
    task_name = Column('task_name', String)
    file_path = Column('file_path', String)
    source = Column('source', String)
    target = Column('target', String)
    status = Column('status', String)
    results = Column('results', String)

    def __init__(self, task_name, file_path, source, target):
        self.task_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.task_name = task_name
        self.file_path = file_path
        self.source = source
        self.target = target
        self.status = 'accepted'
        self.results = None

    def __str__(self):
        return f'<Task task_id={self.task_id} file={self.file_path} status={self.status}>'
    
    def __repr__(self):
        return self.__str__()

    def to_json(self):
        results = None
        if self.results is not None:
            f = open(self.results, 'r')
            results = json.load(f)
            f.close()
        j = {
            'id': self.id,
            'task_id': self.task_id,
            'task_name': self.task_name,
            'file_path': self.file_path,
            'source': self.source,
            'target': self.target,
            'status': self.status,
            'results': results
        }
        return j