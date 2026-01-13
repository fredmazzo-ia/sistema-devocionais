# 📤 Instruções para Enviar ao GitHub

## 🎯 Opção 1: Executar Script Automático (Recomendado)

1. Abra **PowerShell** como Administrador
2. Navegue até a pasta:
   ```powershell
   cd "C:\Users\fred\OneDrive\Documentos\Imprensa"
   ```
3. Execute o script:
   ```powershell
   .\SCRIPT_GIT_POWERSHELL.ps1
   ```

Se der erro de política de execução:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\SCRIPT_GIT_POWERSHELL.ps1
```

## 🎯 Opção 2: Comandos Manuais

### 1. Criar Repositório no GitHub Primeiro

1. Acesse: https://github.com/new
2. Nome: `sistema-devocionais`
3. Clique em "Create repository"
4. **NÃO** marque "Initialize with README"

### 2. Executar no PowerShell

```powershell
# Navegar para a pasta
cd "C:\Users\fred\OneDrive\Documentos\Imprensa"

# Inicializar git (se necessário)
git init

# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Sistema completo de devocionais - primeira versão"

# Adicionar remote (SUBSTITUA SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/sistema-devocionais.git

# Enviar para GitHub
git branch -M main
git push -u origin main
```

## 🔐 Se Pedir Autenticação

### Opção A: Personal Access Token (Recomendado)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Marque: `repo` (acesso completo)
4. Copie o token
5. Use o token como **senha** quando pedir

### Opção B: GitHub CLI

```powershell
# Instalar GitHub CLI
winget install GitHub.cli

# Fazer login
gh auth login
```

## ✅ Verificar

Após enviar, acesse:
```
https://github.com/SEU_USUARIO/sistema-devocionais
```

Todos os arquivos devem estar lá!

---

**Execute o script ou os comandos acima!** 🚀
