import pytz
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    __tablename__  = "task"

    slno           = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id        = db.Column(db.String, nullable=False)
    task_name      = db.Column(db.String, nullable=False, unique=True)
    task_status    = db.Column(db.String, default='P', nullable=False)
    created_on     = db.Column(db.DateTime(timezone=True), default=datetime.now(tz=pytz.timezone('Asia/Kolkata')), nullable=False)
    updated_at     = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (db.CheckConstraint(task_status.in_(['R', 'S', 'P'])),)