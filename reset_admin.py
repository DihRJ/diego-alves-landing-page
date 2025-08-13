#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.admin import Admin
from src.main import app

def reset_admin():
    with app.app_context():
        # Remove todos os admins existentes
        Admin.query.delete()
        db.session.commit()
        
        # Cria novo admin
        admin = Admin(username='diego')
        admin.set_password('diego123')
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"Admin criado com sucesso!")
        print(f"Usuário: diego")
        print(f"Senha: diego123")

if __name__ == '__main__':
    reset_admin()

