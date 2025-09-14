from flask import Blueprint, request, jsonify
from src.models.user import db
from src.routes.auth import login_required
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

pdf_standalone_bp = Blueprint('pdf_standalone', __name__)

# Modelo para PDFs independentes
class StandalonePDF(db.Model):
    __tablename__ = 'standalone_pdfs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StandalonePDF {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'filename': self.filename,
            'original_name': self.original_name,
            'size': self.size,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@pdf_standalone_bp.route('/pdfs/standalone', methods=['GET'])
@login_required
def get_standalone_pdfs():
    """Retorna todos os PDFs independentes"""
    pdfs = StandalonePDF.query.order_by(StandalonePDF.created_at.desc()).all()
    return jsonify([pdf.to_dict() for pdf in pdfs])

@pdf_standalone_bp.route('/pdfs/standalone', methods=['POST'])
@login_required
def upload_standalone_pdf():
    """Upload de PDF independente com título e descrição"""
    if 'pdf' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['pdf']
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if not title:
        return jsonify({'error': 'Título é obrigatório'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Apenas arquivos PDF são permitidos'}), 400
    
    # Verificar tamanho do arquivo (16MB máximo)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > 16 * 1024 * 1024:  # 16MB
        return jsonify({'error': 'Arquivo muito grande. Máximo 16MB'}), 400
    
    try:
        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        original_name = secure_filename(file.filename)
        name_without_ext = os.path.splitext(original_name)[0]
        filename = f"{timestamp}_{unique_id}_{name_without_ext}.pdf"
        
        # Criar diretório se não existir
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'pdfs')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Salvar arquivo
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # Salvar no banco de dados
        new_pdf = StandalonePDF(
            title=title,
            description=description if description else None,
            filename=filename,
            original_name=original_name,
            size=file_size
        )
        
        db.session.add(new_pdf)
        db.session.commit()
        
        return jsonify(new_pdf.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao salvar arquivo: {str(e)}'}), 500

@pdf_standalone_bp.route('/pdfs/standalone/<int:pdf_id>', methods=['PUT'])
@login_required
def update_standalone_pdf(pdf_id):
    """Atualiza título e descrição de um PDF independente"""
    pdf = StandalonePDF.query.get_or_404(pdf_id)
    
    title = request.json.get('title', '').strip()
    description = request.json.get('description', '').strip()
    
    if not title:
        return jsonify({'error': 'Título é obrigatório'}), 400
    
    try:
        pdf.title = title
        pdf.description = description if description else None
        
        db.session.commit()
        return jsonify(pdf.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pdf_standalone_bp.route('/pdfs/standalone/<int:pdf_id>', methods=['DELETE'])
@login_required
def delete_standalone_pdf(pdf_id):
    """Remove um PDF independente"""
    pdf = StandalonePDF.query.get_or_404(pdf_id)
    
    try:
        # Remover arquivo físico
        file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'pdfs', pdf.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remover do banco de dados
        db.session.delete(pdf)
        db.session.commit()
        
        return jsonify({'message': 'PDF removido com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pdf_standalone_bp.route('/pdfs/standalone/<int:pdf_id>/download')
@login_required
def download_standalone_pdf(pdf_id):
    """Download de um PDF independente"""
    pdf = StandalonePDF.query.get_or_404(pdf_id)
    
    file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'pdfs', pdf.filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Arquivo não encontrado'}), 404
    
    from flask import send_file
    return send_file(file_path, as_attachment=True, download_name=pdf.original_name)

