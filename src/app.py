from config.config import create_app
from config.database import init_db
from routes.admin_bp import admin_bp
from routes.user_bp import user_bp

app = create_app()
init_db(app)

app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)