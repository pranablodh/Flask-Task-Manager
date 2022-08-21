from flask import jsonify
from . import tasks
from . .model.db_model import Task, db
from sqlalchemy.sql.expression import func 

@tasks.route('/list', methods = ['GET'])
def list_task():
	try:
		res = db.session.query(Task.task_id, Task.task_name, Task.task_status, Task.created_on, Task.updated_at).all()
		if len(res) == 0:
			return jsonify(status=False, message= 'No Task Found!', data= {}), 404
		else:
			res = [dict(r) for r in res]
			results = []
			for r in res:
				result = {}
				result['task_name'] = r['task_name']
				result['task_id']   = r['task_id']

				if r['task_status'].lower() == 'R'.lower():
					result['started_at'] = r['updated_at'].strftime("%d-%m-%Y %H:%M:%S")
					result['task_status'] = 'RUNNING'
				elif r['task_status'].lower() == 'S'.lower():
					result['finished_at'] = r['updated_at'].strftime("%d-%m-%Y %H:%M:%S")
					result['task_status'] = 'STOPPED'
				else:
					result['created_on'] = r['created_on'].strftime("%d-%m-%Y %H:%M:%S")
					result['task_status'] = 'PENDING'
				results.append(result)
			return jsonify(status=True, message= 'Task Found!', data= {'task_list':results}), 200
	except Exception as ex:
		db.session.close()
		print(ex)
		return jsonify(status=False, message= 'Internal Server Error!', data= {}), 500 