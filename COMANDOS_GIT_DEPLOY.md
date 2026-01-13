# 🚀 Comandos Git para Deploy

## ⚙️ 1. Configurar Git (Primeira Vez)

Se ainda não configurou, execute:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

**OU** apenas para este repositório:

```bash
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

## 📦 2. Fazer Commit e Push

Os arquivos já estão adicionados. Agora execute:

```bash
# Fazer commit
git commit -m "feat: Implementação sistema multi-instância Evolution API com vCard e notificações n8n"

# Fazer push
git push origin main
```

## 🔐 3. Se Pedir Login

Se o Git pedir credenciais:

### **Opção A: Personal Access Token (Recomendado)**

1. Vá em: https://github.com/settings/tokens
2. Clique em **Generate new token (classic)**
3. Dê um nome (ex: "Devocional Deploy")
4. Selecione escopos: `repo` (todos)
5. Clique em **Generate token**
6. **Copie o token** (só aparece uma vez!)
7. Quando pedir senha, cole o token

### **Opção B: GitHub CLI**

```bash
# Instalar GitHub CLI (se não tiver)
# Windows: winget install GitHub.cli

# Fazer login
gh auth login

# Depois fazer push normalmente
git push origin main
```

### **Opção C: Credential Manager**

O Windows pode salvar suas credenciais automaticamente na primeira vez.

## ✅ 4. Verificar Push

Depois do push, verifique no GitHub:

```
https://github.com/fredmazzo-ia/sistema-devocionais
```

## 🚀 5. Deploy no EasyPanel

Depois do push:

1. Acesse o EasyPanel
2. Vá no seu projeto
3. Clique em **Deploy** ou **Redeploy**
4. O EasyPanel vai buscar as mudanças do GitHub automaticamente

---

**Resumo dos Comandos:**

```bash
# 1. Configurar (se necessário)
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"

# 2. Commit (arquivos já estão adicionados)
git commit -m "feat: Implementação sistema multi-instância Evolution API com vCard e notificações n8n"

# 3. Push
git push origin main
```

