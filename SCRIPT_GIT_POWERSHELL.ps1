# Script para enviar codigo para GitHub
# Execute este script no PowerShell

# Navegar para a pasta do projeto
Set-Location "C:\Users\fred\OneDrive\Documentos\Imprensa"

Write-Host "Pasta do projeto: $(Get-Location)" -ForegroundColor Green

# Verificar se git esta instalado
try {
    $gitVersion = git --version
    Write-Host "Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git nao esta instalado ou nao esta no PATH" -ForegroundColor Red
    Write-Host "Instale o Git de: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Verificar se ja e um repositorio git
if (Test-Path .git) {
    Write-Host "Repositorio Git ja inicializado" -ForegroundColor Green
} else {
    Write-Host "Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
}

# Verificar status
Write-Host ""
Write-Host "Status do repositorio:" -ForegroundColor Cyan
git status

# Adicionar todos os arquivos
Write-Host ""
Write-Host "Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Fazer commit
Write-Host "Fazendo commit..." -ForegroundColor Yellow
git commit -m "Sistema completo de devocionais - primeira versao

- Servico robusto de envio via Evolution API
- Integracao com n8n via webhook
- Personalizacao automatica (saudacao + nome)
- Rate limiting e protecoes contra bloqueio
- Sistema de contexto historico
- PostgreSQL com schema completo
- Scheduler automatico
- Endpoints de API completos"

# Verificar se ja tem remote
$remote = git remote get-url origin 2>$null
if ($remote) {
    Write-Host "Remote ja configurado: $remote" -ForegroundColor Green
    Write-Host ""
    Write-Host "Enviando para GitHub..." -ForegroundColor Yellow
    git branch -M main
    git push -u origin main
} else {
    Write-Host ""
    Write-Host "Remote nao configurado!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para configurar, execute:" -ForegroundColor Cyan
    Write-Host "  git remote add origin https://github.com/SEU_USUARIO/sistema-devocionais.git" -ForegroundColor White
    Write-Host ""
    Write-Host "Depois execute:" -ForegroundColor Cyan
    Write-Host "  git branch -M main" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "Concluido!" -ForegroundColor Green
