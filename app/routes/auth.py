"""
Authentication routes for user registration, login, and profile management.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import bcrypt
from app.models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        farm_size = request.form.get('farm_size', 0)
        farm_location = request.form.get('farm_location', '').strip()
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', username=username, email=email, full_name=full_name)
        
        if User.find_by_username(username):
            flash('Username already taken.', 'danger')
            return render_template('register.html', username=username, email=email, full_name=full_name)
        
        if User.find_by_email(email):
            flash('Email already registered.', 'danger')
            return render_template('register.html', username=username, email=email, full_name=full_name)
        
        try:
            user = User(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                phone=phone,
                farm_size=float(farm_size) if farm_size else None,
                farm_location=farm_location
            )
            user.save()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('register.html', username=username, email=email, full_name=full_name)
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        user = User.find_by_username(username)
        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            session['user_id'] = user.id
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        farm_size = request.form.get('farm_size', 0)
        farm_location = request.form.get('farm_location', '').strip()
        
        update_data = {
            'full_name': full_name,
            'phone': phone,
            'address': address,
            'farm_size': float(farm_size) if farm_size else None,
            'farm_location': farm_location,
            'updated_at': datetime.utcnow()
        }
        
        current_user.update(update_data)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('profile.html', user=current_user)

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('auth.profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('auth.profile'))
    
    if len(new_password) < 8:
        flash('Password must be at least 8 characters.', 'danger')
        return redirect(url_for('auth.profile'))
    
    try:
        current_user.set_password(new_password)
        current_user.update({'updated_at': datetime.utcnow()})
        flash('Password changed successfully!', 'success')
    except Exception as e:
        flash(f'Failed to change password: {str(e)}', 'danger')
    
    return redirect(url_for('auth.profile'))

@auth_bp.route('/api/user-data')
@login_required
def get_user_data():
    return jsonify(current_user.get_profile_data())