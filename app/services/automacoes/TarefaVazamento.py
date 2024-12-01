import logging

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.services.automacoes.VazamentoAutomacao import automatizar_notificacao_vazamentos

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="scheduler.log",
    filemode="a",
)

# Função para iniciar o agendador
def iniciar_agendador():
    brt = pytz.timezone("America/Sao_Paulo")
    scheduler = AsyncIOScheduler()
    trigger = CronTrigger(day_of_week="sun", hour=20, minute=20, timezone=brt)  # Todo domingo às 20:00
    scheduler.add_job(automatizar_notificacao_vazamentos, trigger)
    scheduler.start()
    logging.info("Agendador iniciado. Próxima execução programada para domingo às 20:00.")
    return scheduler
