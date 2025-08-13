# 🚀 Guia de Deploy no Render - Landing Page Diego Alves

## 📋 **Pré-requisitos**

1. **Conta no GitHub** (gratuita)
2. **Conta no Render** (gratuita) - https://render.com
3. **Arquivos do projeto** (fornecidos neste pacote)

## 📁 **Estrutura dos Arquivos**

```
diego-alves-render-deploy/
├── src/
│   ├── main.py                 # Aplicação Flask principal
│   ├── models/                 # Modelos do banco de dados
│   ├── routes/                 # Rotas da API
│   └── static/                 # Arquivos do frontend (React build)
├── requirements.txt            # Dependências Python
├── render.yaml                 # Configuração do Render
├── Procfile                    # Comando de inicialização
├── .gitignore                  # Arquivos a ignorar no Git
├── init_db.py                  # Script de inicialização do banco
└── DEPLOY_RENDER.md           # Este guia
```

## 🔧 **Passo 1: Preparar o Repositório GitHub**

### 1.1 Criar Repositório
1. Acesse https://github.com
2. Clique em "New repository"
3. Nome: `diego-alves-landing-page`
4. Marque como **Público** ou **Privado**
5. Clique em "Create repository"

### 1.2 Fazer Upload dos Arquivos
**Opção A - Via Interface Web:**
1. Na página do repositório, clique em "uploading an existing file"
2. Arraste todos os arquivos desta pasta
3. Commit message: "Initial commit - Landing page completa"
4. Clique em "Commit changes"

**Opção B - Via Git (se tiver instalado):**
```bash
git init
git add .
git commit -m "Initial commit - Landing page completa"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/diego-alves-landing-page.git
git push -u origin main
```

## 🌐 **Passo 2: Deploy no Render**

### 2.1 Criar Conta no Render
1. Acesse https://render.com
2. Clique em "Get Started for Free"
3. Conecte com sua conta GitHub

### 2.2 Criar Web Service
1. No dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório `diego-alves-landing-page`

### 2.3 Configurar o Deploy
**Configurações obrigatórias:**
- **Name:** `diego-alves-landing`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn --bind 0.0.0.0:$PORT src.main:app`
- **Plan:** `Free` (gratuito)

### 2.4 Variáveis de Ambiente (Opcional)
- `FLASK_ENV`: `production`
- `PYTHON_VERSION`: `3.11.0`

### 2.5 Finalizar Deploy
1. Clique em "Create Web Service"
2. Aguarde o build (5-10 minutos)
3. Sua aplicação estará disponível em: `https://SEU-APP.onrender.com`

## ✅ **Passo 3: Verificar Funcionamento**

### 3.1 Testar Landing Page
1. Acesse a URL fornecida pelo Render
2. Verifique se a landing page carrega corretamente
3. Teste todos os botões de contato

### 3.2 Testar Área Administrativa
1. Clique no ícone ⚙️ na landing page
2. Faça login com:
   - **Usuário:** `diego`
   - **Senha:** `diego123`
3. Teste adicionar/editar links no portfólio

## 🔧 **Configurações Importantes**

### Credenciais Administrativas
- **Usuário:** `diego`
- **Senha:** `diego123`
- **Alterar:** Acesse a área admin e mude a senha

### Banco de Dados
- **Tipo:** SQLite (incluído)
- **Localização:** Automática no Render
- **Backup:** Automático pelo Render

### SSL/HTTPS
- **Automático:** Render fornece SSL gratuito
- **Certificado:** Renovação automática

## 🚨 **Solução de Problemas**

### Build Falha
1. Verifique se todos os arquivos foram enviados
2. Confirme que `requirements.txt` está presente
3. Verifique logs no dashboard do Render

### Aplicação Não Carrega
1. Verifique o Start Command: `gunicorn --bind 0.0.0.0:$PORT src.main:app`
2. Confirme que `src/main.py` existe
3. Verifique logs de runtime

### Login Não Funciona
1. Aguarde alguns minutos após o deploy
2. Tente acessar `/api/auth/check` para verificar API
3. Use as credenciais: `diego` / `diego123`

## 📱 **Pós-Deploy**

### Atualizar Instagram
1. Copie a URL do Render
2. Substitua o link do Linktree no Instagram
3. Teste o redirecionamento

### Monitoramento
- **Uptime:** Render monitora automaticamente
- **Logs:** Disponíveis no dashboard
- **Métricas:** Gratuitas no plano Free

## 🔄 **Atualizações Futuras**

### Para Atualizar o Site:
1. Faça alterações nos arquivos locais
2. Commit e push para o GitHub
3. Render fará deploy automático

### Para Adicionar Funcionalidades:
1. Modifique os arquivos necessários
2. Teste localmente (opcional)
3. Push para GitHub
4. Deploy automático no Render

## 💡 **Dicas Importantes**

1. **Plano Gratuito:** 750 horas/mês (suficiente para uso pessoal)
2. **Sleep Mode:** App "dorme" após 15min sem uso (normal no plano gratuito)
3. **Custom Domain:** Disponível nos planos pagos
4. **Backup:** Faça backup regular do código no GitHub

## 📞 **Suporte**

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** Para problemas específicos do código
- **Render Support:** Para problemas de infraestrutura

---

**🎉 Parabéns! Sua landing page estará no ar em poucos minutos!**

Lembre-se de testar todas as funcionalidades após o deploy e atualizar o link no seu Instagram.

