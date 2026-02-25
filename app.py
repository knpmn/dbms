"""
app.py - Flask application entry point.
"""
from flask import Flask, session, redirect, url_for
import config
from db import init_pool

# Import blueprints
from routes.auth_routes        import auth_bp
from routes.user_routes        import user_bp
from routes.role_routes        import role_bp
from routes.employee_routes    import employee_bp
from routes.department_routes  import dept_bp
from routes.position_routes    import pos_bp
from routes.attendance_routes  import att_bp
from routes.bonus_point_routes import bonus_bp
from routes.yearly_bonus_routes import yb_bp
from routes.penalty_routes     import penalty_bp
from routes.bp_routes          import bp_log_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    # Initialize Oracle connection pool
    with app.app_context():
        init_pool()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp,     url_prefix='/users')
    app.register_blueprint(role_bp,     url_prefix='/roles')
    app.register_blueprint(employee_bp, url_prefix='/employees')
    app.register_blueprint(dept_bp,     url_prefix='/departments')
    app.register_blueprint(pos_bp,      url_prefix='/positions')
    app.register_blueprint(att_bp,      url_prefix='/attendance')
    app.register_blueprint(bonus_bp,    url_prefix='/bonus-points')
    app.register_blueprint(yb_bp,       url_prefix='/yearly-bonus')
    app.register_blueprint(penalty_bp,  url_prefix='/penalties')
    app.register_blueprint(bp_log_bp,   url_prefix='/bp')

    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('auth.dashboard'))
        return redirect(url_for('auth.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
