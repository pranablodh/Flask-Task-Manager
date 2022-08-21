from flask import Blueprint
tasks = Blueprint('task', __name__, url_prefix='/task')

from .create_task import *
from .list_task import *
from .start_task import *
from .stop_task import *