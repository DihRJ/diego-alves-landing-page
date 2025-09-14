# 🚀 Instruções para Deploy - Funcionalidade PDF

## 📋 Alterações Realizadas

As seguintes modificações foram feitas no seu projeto para implementar o upload de PDFs:

### Arquivos Novos:
- `src/routes/pdf_upload.py` - Sistema de upload de PDFs
- `src/static/uploads/pdfs/` - Pasta para armazenar PDFs

### Arquivos Modificados:
- `src/main.py` - Adicionada nova blueprint
- `src/routes/portfolio.py` - Suporte ao campo pdf_url
- `src/static/admin.html` - Interface administrativa atualizada

## 🔄 Como Fazer o Deploy

### 1. Commit das Alterações
```bash
# No diretório do projeto
git add .
git commit -m "feat: Implementar upload de PDFs no portfólio

- Adicionar sistema de upload de PDFs na área administrativa
- Criar rotas para gerenciamento de PDFs
- Atualizar interface administrativa com funcionalidade de PDF
- Integrar PDFs com links do portfólio
- Adicionar validações de segurança para uploads"
```

### 2. Push para GitHub
```bash
git push origin main
```

### 3. Deploy Automático no Render
- O Render detectará automaticamente as alterações
- O deploy será feito automaticamente
- Aguarde alguns minutos para conclusão

## ✅ Verificações Pós-Deploy

### 1. Testar Login
- Acesse: `https://seu-app.onrender.com/admin.html`
- Faça login com: `diego` / `diego123`

### 2. Testar Upload de PDF
- Na seção "Gerenciar PDFs"
- Selecione um arquivo PDF
- Clique em "Enviar PDF"
- Verifique se aparece na lista

### 3. Testar Associação ao Portfólio
- Na seção "Gerenciar Portfólio"
- Crie um novo link
- Selecione um PDF no dropdown
- Verifique se o PDF aparece associado

## 🔧 Configurações Importantes

### Pasta de Upload
A pasta `src/static/uploads/pdfs/` será criada automaticamente no primeiro upload.

### Limites
- Tamanho máximo: 16MB por PDF
- Tipos aceitos: Apenas arquivos .pdf
- Armazenamento: Local no servidor

### URLs dos PDFs
Os PDFs ficam acessíveis em:
`https://seu-app.onrender.com/api/uploads/pdfs/nome-do-arquivo.pdf`

## 🛡️ Segurança

- ✅ Upload apenas para usuários autenticados
- ✅ Validação de tipo de arquivo
- ✅ Nomes únicos para evitar conflitos
- ✅ Limite de tamanho configurado

## 📱 Interface Atualizada

A nova interface administrativa inclui:
- 📄 Seção dedicada para gerenciar PDFs
- 🔗 Integração com links do portfólio
- 👁️ Visualização de PDFs
- 🗑️ Exclusão de PDFs não utilizados

## 🆘 Solução de Problemas

### Se o upload não funcionar:
1. Verifique se está logado
2. Confirme que o arquivo é PDF
3. Verifique o tamanho (máx. 16MB)

### Se os PDFs não aparecerem:
1. Aguarde alguns segundos após upload
2. Recarregue a página
3. Verifique o console do navegador

### Se houver erro 500:
1. Verifique os logs no Render
2. Confirme que todas as dependências estão instaladas
3. Verifique se a pasta de upload foi criada

## 📞 Suporte

Todas as funcionalidades foram testadas e estão funcionando corretamente. Em caso de dúvidas, verifique os logs do servidor ou entre em contato.

