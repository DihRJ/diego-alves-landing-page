from flask import Blueprint, request, jsonify
from src.models.portfolio import PortfolioLink, db
from src.routes.auth import login_required
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

portfolio_bp = Blueprint('portfolio', __name__)

def extract_metadata(url):
    """Extrai metadados de uma URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrair título
        title = None
        if soup.find('meta', property='og:title'):
            title = soup.find('meta', property='og:title')['content']
        elif soup.find('title'):
            title = soup.find('title').text.strip()
        
        # Extrair descrição
        description = None
        if soup.find('meta', property='og:description'):
            description = soup.find('meta', property='og:description')['content']
        elif soup.find('meta', attrs={'name': 'description'}):
            description = soup.find('meta', attrs={'name': 'description'})['content']
        
        # Extrair imagem
        image_url = None
        if soup.find('meta', property='og:image'):
            image_url = soup.find('meta', property='og:image')['content']
            # Converter URL relativa para absoluta
            if image_url and not image_url.startswith('http'):
                image_url = urljoin(url, image_url)
        
        return {
            'title': title or 'Sem título',
            'description': description or 'Sem descrição',
            'image_url': image_url
        }
    except Exception as e:
        return {
            'title': 'Erro ao carregar',
            'description': f'Não foi possível carregar o conteúdo: {str(e)}',
            'image_url': None
        }

@portfolio_bp.route('/portfolio/links', methods=['GET'])
def get_portfolio_links():
    """Retorna todos os links ativos do portfólio"""
    links = PortfolioLink.query.filter_by(is_active=True).order_by(PortfolioLink.created_at.desc()).all()
    return jsonify([link.to_dict() for link in links])

@portfolio_bp.route('/portfolio/links', methods=['POST'])
@login_required
def add_portfolio_link():
    """Adiciona um novo link ao portfólio"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL é obrigatória'}), 400
    
    url = data['url']
    
    # Extrair metadados da URL
    metadata = extract_metadata(url)
    
    # Criar novo link
    new_link = PortfolioLink(
        title=data.get('title') or metadata['title'],
        url=url,
        description=data.get('description') or metadata['description'],
        image_url=data.get('image_url') or metadata['image_url'],
        pdf_url=data.get('pdf_url')  # Adicionar suporte ao PDF
    )
    
    try:
        db.session.add(new_link)
        db.session.commit()
        return jsonify(new_link.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolio/links/<int:link_id>', methods=['PUT'])
@login_required
def update_portfolio_link(link_id):
    """Atualiza um link do portfólio"""
    link = PortfolioLink.query.get_or_404(link_id)
    data = request.get_json()
    
    if 'title' in data:
        link.title = data['title']
    if 'url' in data:
        link.url = data['url']
    if 'description' in data:
        link.description = data['description']
    if 'image_url' in data:
        link.image_url = data['image_url']
    if 'pdf_url' in data:
        link.pdf_url = data['pdf_url']
    if 'is_active' in data:
        link.is_active = data['is_active']
    
    try:
        db.session.commit()
        return jsonify(link.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolio/links/<int:link_id>', methods=['DELETE'])
@login_required
def delete_portfolio_link(link_id):
    """Remove um link do portfólio"""
    link = PortfolioLink.query.get_or_404(link_id)
    
    try:
        db.session.delete(link)
        db.session.commit()
        return jsonify({'message': 'Link removido com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolio/admin/links', methods=['GET'])
@login_required
def get_all_portfolio_links():
    """Retorna todos os links (incluindo inativos) para administração"""
    links = PortfolioLink.query.order_by(PortfolioLink.created_at.desc()).all()
    return jsonify([link.to_dict() for link in links])
