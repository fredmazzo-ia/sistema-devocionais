"""
Rotas para controle de monitoramento
"""
from fastapi import APIRouter, HTTPException
from app.scheduler import monitor_news, scheduler_running

router = APIRouter()


@router.post("/start")
async def start_monitoring():
    """Inicia monitoramento manual"""
    try:
        monitor_news()
        return {"message": "Monitoramento executado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar monitoramento: {str(e)}")


@router.get("/status")
async def get_monitoring_status():
    """Obtém status do monitoramento"""
    return {
        "running": scheduler_running,
        "message": "Monitoramento ativo" if scheduler_running else "Monitoramento inativo"
    }

