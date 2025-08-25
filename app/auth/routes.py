from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm
from app.models import User, ActivityLog
from app import db
from app.utils.rate_limiter import auth_rate_limit

def log_activity(action, details=None, status='success', error_message=None):
    """Helper function to log user activities"""
    try:
        log_entry = ActivityLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            action=action,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            status=status,
            error_message=error_message
        )
        db.session.add(log_entry)
        db.session.commit()
        
        current_app.logger.info(
            f'User activity: {action}',
            extra={
                'event': 'user_activity',
                'action': action,
                'user_id': current_user.id if current_user.is_authenticated else None,
                'ip': request.remote_addr,
                'status': status
            }
        )
    except Exception as e:
        current_app.logger.error(f'Failed to log activity: {str(e)}', extra={'event': 'logging_error'})

@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_rate_limit()
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            log_activity('login_failed', 
                        details={'username': form.username.data},
                        status='failed',
                        error_message='Invalid credentials')
            return render_template('auth/login.html', form=form)
        
        if not user.is_active:
            flash('Your account has been deactivated. Please contact support.', 'error')
            log_activity('login_failed',
                        details={'username': form.username.data},
                        status='failed',
                        error_message='Account deactivated')
            return render_template('auth/login.html', form=form)
        
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        log_activity('login_success', details={'username': user.username})
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.dashboard')
        
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
@auth_rate_limit()
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if this will be the first user
            user_count = User.query.count()
            is_first_user = (user_count == 0)
            
            user = User(
                username=form.username.data,
                email=form.email.data,
                is_admin=is_first_user  # First user becomes admin
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            current_app.logger.info(
                f'New user registered: {user.username} (Admin: {is_first_user})',
                extra={
                    'event': 'user_registration',
                    'username': user.username,
                    'email': user.email,
                    'is_admin': is_first_user,
                    'ip': request.remote_addr
                }
            )
            
            if is_first_user:
                flash('Registration successful! You are the first user and have been granted admin privileges. Please log in.', 'success')
            else:
                flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f'Registration failed: {str(e)}',
                extra={
                    'event': 'registration_error',
                    'username': form.username.data,
                    'error': str(e)
                }
            )
            flash('Registration failed. Please try again.', 'error')
    
    # Check if this would be the first user
    user_count = User.query.count()
    is_first_user = (user_count == 0)
    
    return render_template('auth/register.html', form=form, is_first_user=is_first_user)

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    username = current_user.username
    log_activity('logout', details={'username': username})
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
@auth_rate_limit()
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html', form=form)
        
        try:
            current_user.set_password(form.new_password.data)
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            
            log_activity('password_change', details={'username': current_user.username})
            flash('Your password has been changed successfully.', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f'Password change failed: {str(e)}',
                extra={'event': 'password_change_error', 'user_id': current_user.id}
            )
            flash('Password change failed. Please try again.', 'error')
    
    return render_template('auth/change_password.html', form=form)