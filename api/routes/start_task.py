import pytz
from datetime import datetime
from flask import jsonify
from . import tasks
from . .model.db_model import Task, db
from sqlalchemy.sql.expression import func 

@tasks.route('/start/<task_name>', methods = ['PUT'])
def start_task(task_name=None):
    try:
        res = db.session.query(Task.task_status).filter(Task.task_name == task_name).scalar()
        if res is None:
            return jsonify(status=False, message= 'No Task Found With This Name!', data= {}), 404
        if res == 'R':
            return jsonify(status=False, message= 'Task is Already Running!', data= {}), 409

        count = db.session.query(func.count(Task.task_id)).filter(Task.task_status == 'R').scalar()
        if count >= 10:
            db.session.query(Task).filter(Task.task_id == db.session.query(Task.task_id)
            .filter(Task.task_status == 'R').order_by(Task.updated_at.asc()).limit(1).scalar())\
            .update({'task_status':'S'})
    
        db.session.query(Task).filter(Task.task_name == task_name).update({'task_status':'R',
        "updated_at":datetime.now(pytz.timezone('Asia/Kolkata'))})

        db.session.commit()
        db.session.close()
        return jsonify(status=True, message= 'Task Started!', data= {}), 200 
    except Exception as ex:
        db.session.close()
        print(ex)
        return jsonify(status=False, message= 'Internal Server Error!', data= {}), 500 