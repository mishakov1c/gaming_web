import os
basedir = os.path.dirname(__file__)

MAIN_PAGE = 'http://127.0.0.1:5000/'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SECRET_KEY = 'IHi6hf284efdwiqJKNpo4KFkqdpkm8m1v'

SQLALCHEMY_TRACK_MODIFICATIONS = False