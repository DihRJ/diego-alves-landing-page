from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.routes.auth import login_required
import os
import uuid
from datetime import datetime

pdf_upload_bp = Blueprint('pdf_upload', __name__)

# Configurações de upload
UPLOAD_FOLDER = 'src/static/uploads/pdfs'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    """Cria a pasta de upload se não existir"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@pdf_upload_bp.route('/upload/pdf', methods=['POST'])
@login_required
def upload_pdf():
    """Upload de arquivo PDF"""
    create_upload_folder()
    
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Apenas arquivos PDF são permitidos'}), 400
    
    # Verificar tamanho do arquivo
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'Arquivo muito grande. Máximo 16MB'}), 400
    
    if file and allowed_file(file.filename):
        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        original_name = secure_filename(file.filename)
        filename = f"{timestamp}_{unique_id}_{original_name}"
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        try:
            file.save(file_path)
            
            # Retornar URL relativa para o arquivo
            pdf_url = f"/uploads/pdfs/{filename}"
            
            return jsonify({
                'message': 'PDF enviado com sucesso',
                'pdf_url': pdf_url,
                'filename': filename,
                'original_name': original_name
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Erro ao salvar arquivo: {str(e)}'}), 500
    
    return jsonify({'error': 'Erro no upload do arquivo'}), 400

@pdf_upload_bp.route('/uploads/pdfs/<filename>')
def serve_pdf(filename):
    """Serve arquivos PDF"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@pdf_upload_bp.route('/uploads/pdfs', methods=['GET'])
@login_required
def list_pdfs():
    """Lista todos os PDFs enviados"""
    create_upload_folder()
    
    try:
        files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_stat = os.stat(file_path)
                
                files.append({
                    'filename': filename,
                    'url': f"/uploads/pdfs/{filename}",
                    'size': file_stat.st_size,
                    'created_at': datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                })
        
        # Ordenar por data de criação (mais recente primeiro)
        files.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify(files), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao listar arquivos: {str(e)}'}), 500

@pdf_upload_bp.route('/uploads/pdfs/<filename>', methods=['DELETE'])
@login_required
def delete_pdf(filename):
    """Remove um arquivo PDF"""
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'PDF removido com sucesso'}), 200
        else:
            return jsonify({'error': 'Arquivo não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Erro ao remover arquivo: {str(e)}'}), 500

