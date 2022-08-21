import uuid
import pytz
from datetime import datetime
from flask import jsonify
from . import tasks
from . .model.db_model import Task, db
from sqlalchemy.sql.expression import func 

@tasks.route('/create/<task_name>', methods = ['POST'])
def create_task(task_name=None):
    try:
        task            = Task()
        task.slno       = 1 if db.session.query(func.max(Task.slno)).scalar() is None else \
                          db.session.query(func.max(Task.slno)).scalar() + 1 
        task.task_id    = str(uuid.uuid4())
        task.task_name  = task_name
        task.created_on = datetime.now(pytz.timezone('Asia/Kolkata'))

        db.session.add(task)
        db.session.commit()
        db.session.close()
        return jsonify(status=True, message= 'Task Created!', data= {}), 201
    except Exception as ex:
        db.session.rollback()
        db.session.close()
        print(ex)
        if 'UNIQUE constraint failed: task.task_name' in str(ex):
            return jsonify(status=False, message= 'Task With This Name Already Exists!', data= {}), 409  
        else:
            return jsonify(status=False, message= 'Internal Server Error!', data= {}), 500 