# 🔧 Git Não Encontrado - Soluções

## ❌ Problema

O Git não está instalado ou não está no PATH do sistema.

## ✅ Solução 1: Instalar Git (Recomendado)

### Opção A: Via Winget (Mais Rápido)

```powershell
winget install --id Git.Git -e --source winget
```

### Opção B: Download Manual

1. Acesse: https://git-scm.com/download/win
2. Baixe e instale
3. Durante instalação, marque: **"Add Git to PATH"**
4. Reinicie o PowerShell

## ✅ Solução 2: Usar Git Bash (Se já tiver instalado)

Se você já tem Git instalado mas não está no PATH:

1. Abra **Git Bash** (procure no menu iniciar)
2. Execute:

```bash
cd /c/Users/fred/OneDrive/Documentos/Imprensa

git init
git add .
git commit -m "Sistema completo de devocionais - primeira versao"

# SUBSTITUA SEU_USUARIO
git remote add origin https://github.com/SEU_USUARIO/sistema-devocionais.git

git branch -M main
git push -u origin main
```

## ✅ Solução 3: Usar GitHub Desktop

1. Instale: https://desktop.github.com/
2. Abra GitHub Desktop
3. File → Add Local Repository
4. Selecione: `C:\Users\fred\OneDrive\Documentos\Imprensa`
5. Publish repository
6. Escolha nome: `sistema-devocionais`
7. Clique em "Publish repository"

## ✅ Solução 4: Adicionar Git ao PATH Manualmente

Se o Git já está instalado mas não no PATH:

1. Encontre onde está instalado (geralmente: `C:\Program Files\Git\cmd`)
2. Adicione ao PATH do sistema:
   - Windows → Configurações → Sistema → Variáveis de Ambiente
   - Editar PATH → Adicionar: `C:\Program Files\Git\cmd`
3. Reinicie o PowerShell

## 🎯 Após Instalar

Execute novamente:

```powershell
.\SCRIPT_GIT_POWERSHELL.ps1
```

---

**Recomendação: Use a Solução 1 (instalar via winget) ou Solução 3 (GitHub Desktop) - são as mais fáceis!** 🚀
