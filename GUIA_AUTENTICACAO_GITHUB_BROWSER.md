# 🔐 Guia: Autenticação GitHub via Navegador

## ✅ Status Atual

**Deploy concluído!** ✅

O commit `7629843` com todas as correções já está no GitHub:
- https://github.com/fredmazzo-ia/sistema-devocionais

## 🚀 Próximos Passos no EasyPanel

1. Acesse o EasyPanel
2. Vá no seu projeto `devocionais-api`
3. Clique em **"Redeploy"** ou **"Deploy"**
4. O EasyPanel vai buscar automaticamente as mudanças do GitHub

---

## 🔐 Autenticação via Navegador (Para Futuros Deploys)

### Opção 1: GitHub CLI (Recomendado)

#### Instalar GitHub CLI

```powershell
# Via winget (requer confirmação interativa)
winget install --id GitHub.cli

# OU baixar manualmente:
# https://cli.github.com/
```

#### Autenticar via Browser

```powershell
# Fazer login (abre navegador automaticamente)
gh auth login

# Escolher:
# - GitHub.com
# - HTTPS
# - Yes (autenticar Git)
# - Login via web browser
```

#### Usar após autenticação

```powershell
# Agora pode fazer push normalmente
git push origin main
```

---

### Opção 2: Personal Access Token (Mais Simples)

#### Criar Token no GitHub

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token (classic)"**
3. Configure:
   - **Note**: "Devocional Deploy"
   - **Expiration**: 90 days (ou No expiration)
   - **Scopes**: Marque `repo` (todos os repositórios)
4. Clique em **"Generate token"**
5. **Copie o token** (só aparece uma vez!)

#### Usar o Token

Quando fizer `git push`, o Git vai pedir:
- **Username**: `fredmazzo-ia`
- **Password**: Cole o token (não sua senha!)

O Windows pode salvar automaticamente na primeira vez.

---

### Opção 3: Git Credential Manager (Já Instalado)

O Git for Windows já vem com Git Credential Manager. Ele pode abrir o navegador automaticamente.

#### Configurar

```powershell
# Verificar se está instalado
git config --global credential.helper manager

# Tentar push (pode abrir navegador)
git push origin main
```

Se não abrir automaticamente, use uma das opções acima.

---

## 📝 Comandos Rápidos para Deploy

```powershell
# 1. Verificar mudanças
git status

# 2. Adicionar arquivos modificados
git add .

# 3. Fazer commit
git commit -m "feat: Descrição das mudanças"

# 4. Fazer push (vai pedir autenticação na primeira vez)
git push origin main

# 5. No EasyPanel: Clicar em "Redeploy"
```

---

## ✅ Verificar Deploy

Após o push, verifique no GitHub:
- https://github.com/fredmazzo-ia/sistema-devocionais/commits/main

O commit mais recente deve aparecer lá.

---

## 🔧 Troubleshooting

### Erro: "Authentication failed"

**Solução**: Use Personal Access Token em vez de senha.

### Erro: "credential-manager-core is not a git command"

**Solução**: 
```powershell
git config --global credential.helper manager
```

### Não abre navegador automaticamente

**Solução**: Use GitHub CLI (`gh auth login`) ou Personal Access Token.

---

## 📚 Referências

- GitHub CLI: https://cli.github.com/
- Personal Access Tokens: https://github.com/settings/tokens
- Git Credential Manager: https://github.com/git-ecosystem/git-credential-manager
