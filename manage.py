from divvy import app,db
from flask.ext.script import Manager, prompt_bool, Server
from divvy.models import *
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)
server = Server(host='0.0.0.0', port=8000)
manager.add_command('runserver', server)

@manager.command
def initdb():
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