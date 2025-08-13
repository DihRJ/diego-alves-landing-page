from flask import Blueprint, request, jsonify, session
from src.models.admin import Admin, db
from datetime import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({'error': 'Login necessário'}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login do administrador"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400
    
    username = data['username']
    password = data['password']
    
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and admin.check_password(password):
        session['admin_id'] = admin.id
        admin.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'admin': admin.to_dict()
        })
    else:
        return jsonify({'error': 'Usuário ou senha incorretos'}), 401

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout do administrador"""
    session.pop('admin_id', None)
    return jsonify({'message': 'Logout realizado com sucesso'})

@auth_bp.route('/auth/check', methods=['GET'])
def check_auth():
    """Verifica se o usuário está logado"""
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        if admin:
            return jsonify({
                'authenticated': True,
                'admin': admin.to_dict()
            })
    
    return jsonify({'authenticated': False}), 401

@auth_bp.route('/auth/create-admin', methods=['POST'])
def create_admin():
    """Cria um administrador (apenas para setup inicial)"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400
    
    # Verifica se já existe um admin
    existing_admin = Admin.query.first()
    if existing_admin:
        return jsonify({'error': 'Administrador já existe'}), 400
    
    username = data['username']
    password = data['password']
    
    admin = Admin(username=username)
    admin.set_password(password)
    
    try:
        db.session.add(admin)
        db.session.commit()
        return jsonify({
            'message': 'Administrador criado com sucesso',
            'admin': admin.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
