# 💻 Comandos Git para PowerShell (Windows)

## 🔧 Configuração Inicial (Primeira Vez)

Se ainda não configurou o Git:

```powershell
# Configurar nome
git config --global user.name "Seu Nome"

# Configurar email
git config --global user.email "seu@email.com"
```

## 📤 Enviar para GitHub

### Passo 1: Navegar para a Pasta

```powershell
cd "C:\Users\fred\OneDrive\Documentos\Imprensa"
```

### Passo 2: Verificar Status

```powershell
git status
```

Se aparecer "not a git repository", inicialize:

```powershell
git init
```

### Passo 3: Adicionar Arquivos

```powershell
# Adicionar todos os arquivos
git add .

# Ou adicionar arquivos específicos
git add backend/
git add database/
git add *.md
```

### Passo 4: Fazer Commit

```powershell
git commit -m "Sistema completo de devocionais - primeira versão"
```

### Passo 5: Adicionar Remote (GitHub)

**SUBSTITUA `SEU_USUARIO` pelo seu usuário do GitHub:**

```powershell
# HTTPS (mais fácil)
git remote add origin https://github.com/SEU_USUARIO/sistema-devocionais.git

# Ou SSH (se tiver configurado)
# git remote add origin git@github.com:SEU_USUARIO/sistema-devocionais.git
```

### Passo 6: Enviar para GitHub

```powershell
# Criar branch main
git branch -M main

# Enviar código
git push -u origin main
```

**Se pedir autenticação:**
- Use seu **Personal Access Token** do GitHub (não a senha)
- Ou configure SSH

## 🔄 Atualizar Código no GitHub

Quando fizer alterações:

```powershell
# Ver o que mudou
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

## 🔍 Comandos Úteis

```powershell
# Ver histórico
git log

# Ver diferenças
git diff

# Ver remotes configurados
git remote -v

# Mudar remote (se necessário)
git remote set-url origin https://github.com/SEU_USUARIO/novo-nome.git
```

## 🔐 Autenticação GitHub

### Opção 1: Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Marque: `repo` (acesso completo)
4. Copie o token
5. Use o token como senha quando pedir

### Opção 2: GitHub CLI

```powershell
# Instalar GitHub CLI
winget install GitHub.cli

# Fazer login
gh auth login
```

---

**Siga os passos na ordem!** 🚀
