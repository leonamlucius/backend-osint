import aiosmtplib
import logging
from email.message import EmailMessage


logging.basicConfig(level=logging.ERROR, filename='error.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "felix.rodrigoing65@gmail.com"
SMTP_PASSWORD = "unwx kffu jrtf fnys"


async def enviar_email(destinatario: str, assunto: str, mensagem: str):
    email = EmailMessage()
    email["From"] = SMTP_USERNAME
    email["To"] = destinatario
    email["Subject"] = assunto
    email.set_content(mensagem)


    try:
        await aiosmtplib.send(
            email,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            start_tls=True
        )
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")



