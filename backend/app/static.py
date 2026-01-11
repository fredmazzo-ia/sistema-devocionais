"""
Servir frontend estático
"""
from fastapi import Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# Caminho para o frontend buildado
# Tenta vários caminhos possíveis
POSSIBLE_PATHS = [
    Path("/app/dist"),  # Docker (backend) - PRIMEIRO (produção)
    Path(__file__).parent.parent / "dist",  # Dentro do backend (local)
    Path(__file__).parent.parent.parent / "frontend" / "dist",  # Raiz do projeto (dev)
    Path("/app/frontend/dist"),  # Docker alternativo
]

FRONTEND_BUILD_PATH = None
for path in POSSIBLE_PATHS:
    if path.exists() and (path / "index.html").exists():
        FRONTEND_BUILD_PATH = path
        break


def setup_static_files(app):
    """
    Configura arquivos estáticos do frontend
    """
    if FRONTEND_BUILD_PATH:
        # Servir arquivos estáticos (JS, CSS, imagens, etc)
        assets_path = FRONTEND_BUILD_PATH / "assets"
        if assets_path.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")
        
        # Servir outros arquivos estáticos
        app.mount("/static", StaticFiles(directory=str(FRONTEND_BUILD_PATH)), name="static")
        
        # NÃO registrar rota catch-all aqui - será registrada DEPOIS dos routers
        # Isso evita interceptar rotas /api
        pass
    else:
        # Se não tiver build, manter endpoint raiz original
        pass

