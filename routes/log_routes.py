from flask import Blueprint, jsonify
from models import Activity_Log

log_bp = Blueprint('log', __name__)

@log_bp.route('/admin/activity-log', methods=['GET'])
def get_activity_log():
    logs = Activity_Log.query.all()
    return jsonify([{'log_id': log.log_id, 'action': log.Action, 'timestamp': log.Timestamp} for log in logs])
