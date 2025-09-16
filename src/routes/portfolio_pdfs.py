from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from src.models.user import db
from src.routes.auth import login_required
import os
import uuid
from datetime import datetime

portfolio_pdfs_bp = Blueprint('portfolio_pdfs', __name__)

class PortfolioPDF(db.Model):
    __tablename__ = 'portfolio_pdfs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'filename': self.filename,
            'original_name': self.original_name,
            'size': self.size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'order_index': self.order_index,
            'url': f'/static/uploads/portfolio-pdfs/{self.filename}'
        }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def save_pdf_file(file):
    """Salva o arquivo PDF e retorna o nome do arquivo salvo"""
    if not file or not allowed_file(file.filename):
        raise ValueError("Arquivo deve ser um PDF")
    
    # Gerar nome único para o arquivo
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    
    # Criar diretório se não existir
    upload_dir = os.path.join(current_app.static_folder, 'uploads', 'portfolio-pdfs')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Salvar arquivo
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)
    
    return unique_filename

@portfolio_pdfs_bp.route('/portfolio/pdfs', methods=['GET'])
def get_portfolio_pdfs():
    """Listar PDFs do portfólio (público)"""
    try:
        pdfs = PortfolioPDF.query.filter_by(is_active=True).order_by(PortfolioPDF.order_index.asc(), PortfolioPDF.created_at.desc()).all()
        return jsonify([pdf.to_dict() for pdf in pdfs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_pdfs_bp.route('/portfolio/pdfs/admin', methods=['GET'])
@login_required
def get_portfolio_pdfs_admin():
    """Listar PDFs do portfólio (admin)"""
    try:
        pdfs = PortfolioPDF.query.order_by(PortfolioPDF.order_index.asc(), PortfolioPDF.created_at.desc()).all()
        return jsonify([pdf.to_dict() for pdf in pdfs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_pdfs_bp.route('/portfolio/pdfs', methods=['POST'])
@login_required
def add_portfolio_pdf():
    """Adicionar PDF ao portfólio"""
    try:
        # Validar dados
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if not title:
            return jsonify({'error': 'Título é obrigatório'}), 400
        
        # Validar arquivo
        if 'pdf' not in request.files:
            return jsonify({'error': 'Arquivo PDF é obrigatório'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verificar tamanho (16MB)
        file.seek(0, 2)  # Ir para o final do arquivo
        file_size = file.tell()
        file.seek(0)  # Voltar para o início
        
        if file_size > 16 * 1024 * 1024:  # 16MB
            return jsonify({'error': 'Arquivo muito grande. Máximo 16MB'}), 400
        
        # Salvar arquivo
        try:
            filename = save_pdf_file(file)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Obter próximo order_index
        max_order = db.session.query(db.func.max(PortfolioPDF.order_index)).scalar() or 0
        
        # Criar registro no banco
        pdf = PortfolioPDF(
            title=title,
            description=description if description else None,
            filename=filename,
            original_name=file.filename,
            size=file_size,
            order_index=max_order + 1
        )
        
        db.session.add(pdf)
        db.session.commit()
        
        return jsonify(pdf.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_pdfs_bp.route('/portfolio/pdfs/<int:pdf_id>', methods=['PUT'])
@login_required
def update_portfolio_pdf(pdf_id):
    """Atualizar PDF do portfólio"""
    try:
        pdf = PortfolioPDF.query.get_or_404(pdf_id)
        
        data = request.get_json()
        
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({'error': 'Título é obrigatório'}), 400
            pdf.title = title
        
        if 'description' in data:
            pdf.description = data['description'].strip() if data['description'] else None
        
        if 'is_active' in data:
            pdf.is_active = bool(data['is_active'])
        
        if 'order_index' in data:
            pdf.order_index = int(data['order_index'])
        
        db.session.commit()
        return jsonify(pdf.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_pdfs_bp.route('/portfolio/pdfs/<int:pdf_id>', methods=['DELETE'])
@login_required
def delete_portfolio_pdf(pdf_id):
    """Excluir PDF do portfólio"""
    try:
        pdf = PortfolioPDF.query.get_or_404(pdf_id)
        
        # Remover arquivo físico
        file_path = os.path.join(current_app.static_folder, 'uploads', 'portfolio-pdfs', pdf.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remover do banco
        db.session.delete(pdf)
        db.session.commit()
        
        return jsonify({'message': 'PDF removido com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_pdfs_bp.route('/portfolio/pdfs/<int:pdf_id>/toggle', methods=['POST'])
@login_required
def toggle_portfolio_pdf(pdf_id):
    """Ativar/desativar PDF do portfólio"""
    try:
        pdf = PortfolioPDF.query.get_or_404(pdf_id)
        pdf.is_active = not pdf.is_active
        db.session.commit()
        
        return jsonify(pdf.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

