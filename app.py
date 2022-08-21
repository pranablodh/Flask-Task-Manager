import atexit
from flask import Flask, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from api.routes import tasks
from api.model.db_model import *
from api.scheduler.queue_flush import *

app = Flask(__name__)
app.register_blueprint(tasks)
CORS(app, resources={r"/task/*": {"expose_headers": "*"}})
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
db.init_app(app)
with app.app_context():
    db.create_all()  

scheduler = BackgroundScheduler()
scheduler.add_job(func=clear_queue, trigger="interval", seconds=5)
scheduler.start()     
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def ping():
   return jsonify(status=True, message= 'Endpoint Running!', data= {}), 200

@app.errorhandler(405)
def method_not_allowed(e):
   return jsonify(status=False, message= 'The method is not allowed for the requested URL!', data= {}), 405

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0', debug=True)