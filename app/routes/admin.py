"""
Admin routes for system administration.
"""

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils.database import db_instance
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    try:
        stats = {
            'total_users': db_instance.get_collection('users').count_documents({}),
            'total_disease_reports': db_instance.get_collection('disease_reports').count_documents({}),
            'total_predictions': db_instance.get_collection('yield_predictions').count_documents({}),
            'total_fertilizer_recs': db_instance.get_collection('fertilizer_recommendations').count_documents({}),
            'total_irrigation_schedules': db_instance.get_collection('irrigation_schedules').count_documents({}),
            'total_crop_recommendations': db_instance.get_collection('crop_recommendations').count_documents({}),
        }
    except Exception:
        stats = {k: 0 for k in [
            'total_users', 'total_disease_reports', 'total_predictions',
            'total_fertilizer_recs', 'total_irrigation_schedules', 'total_crop_recommendations'
        ]}

    return render_template('admin/dashboard.html', stats=stats)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    try:
        all_users = list(db_instance.get_collection('users').find().sort('created_at', -1))
        for u in all_users:
            u['_id'] = str(u['_id'])
    except Exception:
        all_users = []
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    try:
        disease_reports = list(
            db_instance.get_collection('disease_reports').find().sort('created_at', -1).limit(50)
        )
        for r in disease_reports:
            r['_id'] = str(r['_id'])
    except Exception:
        disease_reports = []
    return render_template('admin/reports.html', reports=disease_reports)
