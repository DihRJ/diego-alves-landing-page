# 🌐 Landing Page - Diego Alves

Landing page profissional para Diego Alves, Secretário de Segurança & Gestão Pública, com sistema de portfólio administrativo.

## 🚀 **Deploy Rápido**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

**Veja o guia completo:** [DEPLOY_RENDER.md](./DEPLOY_RENDER.md)

## ✨ **Funcionalidades**

### **Landing Page**
- ✅ Design moderno e responsivo
- ✅ Foto profissional e informações atualizadas
- ✅ 5 botões de contato direto:
  - WhatsApp (+5522998076235)
  - E-mail (dih.al@hotmail.com)
  - Portfólio dinâmico
  - Instagram (@diegoalvesspa)
  - LinkedIn (diego-alves-amaral)
- ✅ Seção de credibilidade (8.6K seguidores, 83.3K visualizações)
- ✅ Informações SESORP São Pedro da Aldeia/RJ

### **Sistema Administrativo**
- ✅ Login seguro com usuário e senha
- ✅ Gerenciamento de links do portfólio
- ✅ Extração automática de metadados (título, descrição, imagem)
- ✅ Ativar/desativar links
- ✅ Interface intuitiva e responsiva

## 🛠 **Tecnologias**

### **Frontend**
- React 18
- Tailwind CSS
- Lucide Icons
- React Router

### **Backend**
- Flask 3.1
- SQLAlchemy
- Flask-CORS
- SQLite

### **Deploy**
- Render (recomendado)
- Gunicorn
- SSL automático

## 🔐 **Credenciais Padrão**

- **Usuário:** `diego`
- **Senha:** `diego123`

⚠️ **Importante:** Altere a senha após o primeiro acesso!

## 📁 **Estrutura do Projeto**

```
├── src/
│   ├── main.py              # Aplicação Flask principal
│   ├── models/              # Modelos do banco de dados
│   │   ├── user.py         # Configuração SQLAlchemy
│   │   ├── admin.py        # Modelo de administrador
│   │   └── portfolio.py    # Modelo de links do portfólio
│   ├── routes/             # Rotas da API
│   │   ├── auth.py         # Autenticação
│   │   ├── portfolio.py    # Gerenciamento de portfólio
│   │   └── user.py         # Usuários
│   └── static/             # Frontend (React build)
├── requirements.txt        # Dependências Python
├── render.yaml            # Configuração Render
├── Procfile              # Comando de inicialização
└── .gitignore           # Arquivos ignorados
```

## 🚀 **Deploy Local (Desenvolvimento)**

### **Pré-requisitos**
- Python 3.11+
- pip

### **Instalação**
```bash
# Clonar repositório
git clone https://github.com/SEU_USUARIO/diego-alves-landing-page.git
cd diego-alves-landing-page

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python src/main.py
```

### **Acessar**
- **Landing Page:** http://localhost:5000
- **Admin:** http://localhost:5000/login

## 📱 **URLs de Produção**

Após o deploy no Render:
- **Landing Page:** `https://SEU-APP.onrender.com`
- **Login Admin:** `https://SEU-APP.onrender.com/login`
- **API:** `https://SEU-APP.onrender.com/api/`

## 🔧 **Configuração**

### **Variáveis de Ambiente**
```bash
FLASK_ENV=production
PYTHON_VERSION=3.11.0
```

### **Banco de Dados**
- **Desenvolvimento:** SQLite local
- **Produção:** SQLite no Render (persistente)

## 📊 **API Endpoints**

### **Autenticação**
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/check` - Verificar autenticação

### **Portfólio**
- `GET /api/portfolio/links` - Listar links públicos
- `GET /api/portfolio/admin/links` - Listar todos (admin)
- `POST /api/portfolio/links` - Adicionar link (admin)
- `PUT /api/portfolio/links/:id` - Editar link (admin)
- `DELETE /api/portfolio/links/:id` - Deletar link (admin)

## 🔒 **Segurança**

- ✅ Senhas criptografadas (Werkzeug)
- ✅ Sessões seguras
- ✅ CORS configurado
- ✅ Proteção de rotas administrativas
- ✅ SSL/HTTPS automático (Render)

## 📈 **Performance**

- ✅ Frontend otimizado (React build)
- ✅ Imagens comprimidas
- ✅ CSS minificado
- ✅ Carregamento rápido (<2s)

## 🐛 **Solução de Problemas**

### **Erro 500**
- Verifique logs no Render dashboard
- Confirme que todas as dependências estão instaladas

### **Login não funciona**
- Verifique credenciais: `diego` / `diego123`
- Aguarde inicialização completa do banco

### **Links não carregam**
- Verifique conexão com internet
- Teste URLs manualmente

## 🔄 **Atualizações**

Para atualizar o site:
1. Modifique os arquivos necessários
2. Commit e push para GitHub
3. Render fará deploy automático

## 📞 **Contato**

- **WhatsApp:** +5522998076235
- **E-mail:** dih.al@hotmail.com
- **Instagram:** @diegoalvesspa
- **LinkedIn:** diego-alves-amaral

## 📄 **Licença**

Este projeto é de uso pessoal para Diego Alves.

---

**Desenvolvido com ❤️ para transformação digital na gestão pública**

