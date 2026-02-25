"""
auth.py - Session helpers and role-based access decorators.
"""
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash


# ------------------------------------------------------------------ #
#  Password helpers
# ------------------------------------------------------------------ #

def hash_password(plain: str) -> str:
    return generate_password_hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return check_password_hash(hashed, plain)


# ------------------------------------------------------------------ #
#  Decorators
# ------------------------------------------------------------------ #

def login_required(f):
    """Redirect to /login if not logged in."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def role_required(*allowed_roles):
    """
    Restrict access to specific roles.
    Usage:  @role_required('Admin')
            @role_required('Admin', 'HR Staff')
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('role') not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('auth.dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator
