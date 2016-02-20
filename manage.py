from divvy import app,db
from flask.ext.script import Manager, prompt_bool
from models import *
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)

@manager.command
def createdb():
    if prompt_bool(
        "Create database"):
        db.create_all()
    print 'Initialized the database'
    
@manager.command
def dropdb():
    if prompt_bool(
        "Drop db and lose all your data"):
        db.drop_all()
    print 'Dropped the database'
    
if __name__ == '__main__':
    manager.run()