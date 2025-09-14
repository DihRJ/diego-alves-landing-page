#!/usr/bin/env python3
"""
Script para inicializar o banco de dados no Render
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.admin import Admin
from src.routes.pdf_standalone import StandalonePDF
from src.main import app

def init_database():
    """Inicializa o banco de dados e cria o usuário admin"""
    with app.app_context():
        # Cria todas as tabelas
        db.create_all()
        
        # Verifica se já existe um admin
        existing_admin = Admin.query.first()
        if not existing_admin:
            # Cria admin padrão
            admin = Admin(username='diego')
            admin.set_password('diego123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Banco de dados inicializado com sucesso!")
            print("✅ Usuário admin criado: diego / diego123")
        else:
            print("✅ Banco de dados já inicializado!")

if __name__ == '__main__':
    init_database()

