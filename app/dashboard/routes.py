from . import dashboard_bp
from flask import render_template
import logging

@dashboard_bp.route('/tasks')
def show_tasks():
    return render_template('tasks.html',show_logout=True)