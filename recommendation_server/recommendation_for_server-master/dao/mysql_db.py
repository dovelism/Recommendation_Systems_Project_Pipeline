from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

class Mysql(object):
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:950313@localhost:3306/initial_data')
        self._DBSession = sessionmaker(bind=self.engine)

