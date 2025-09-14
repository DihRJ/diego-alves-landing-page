import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.portfolio import PortfolioLink
from src.models.admin import Admin
from src.routes.user import user_bp
from src.routes.portfolio import portfolio_bp
from src.routes.auth import auth_bp
from src.routes.pdf_upload import pdf_upload_bp
from src.routes.pdf_standalone import pdf_standalone_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
CORS(app, supports_credentials=True)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(portfolio_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(pdf_upload_bp, url_prefix='/api')
app.register_blueprint(pdf_standalone_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    
    # Cria admin padrão se não existir
    existing_admin = Admin.query.first()
    if not existing_admin:
        admin = Admin(username='diego')
        admin.set_password('diego123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin criado: diego / diego123")

@app.route('/admin')
def admin_panel():
    """Rota específica para o painel administrativo"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return "index.html not found", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
