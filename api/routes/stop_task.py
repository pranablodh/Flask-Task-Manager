import pytz
from datetime import datetime
from flask import jsonify
from . import tasks
from . .model.db_model import Task, db

@tasks.route('/stop/<task_name>', methods = ['DELETE'])
def stop_task(task_name=None):
    try:
        res = db.session.query(Task.task_status).filter(Task.task_name == task_name).scalar()
        if res is None:
            return jsonify(status=False, message= 'No Task Found With This Name!', data= {}), 404
        if res == 'S':
            return jsonify(status=False, message= 'Task is Already Stopped!', data= {}), 409
        if res == 'P':
            return jsonify(status=False, message= 'Task Not Started Yet!', data= {}), 409
    
        db.session.query(Task).filter(Task.task_name == task_name).update({'task_status':'S',
        "updated_at":datetime.now(pytz.timezone('Asia/Kolkata'))})

        db.session.commit()
        db.session.close()
        return jsonify(status=True, message= 'Task Stopped!', data= {}), 200 
    except Exception as ex:
        db.session.close()
        print(ex)
        return jsonify(status=False, message= 'Internal Server Error!', data= {}), 500 