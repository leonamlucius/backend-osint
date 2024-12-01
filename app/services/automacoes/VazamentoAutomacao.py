# Configuração de logging
import logging

from app.db.database import SessionLocal
from app.services import UsuarioService, VazamentoService, EmailService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="scheduler.log",
    filemode="a",
)

# Função para gerenciar a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Função para gerar o HTML do e-mail com imagem
def gerar_mensagem_html(usuario_nome: str, vazamento_titulo: str, vazamento_data: str, vazamento_descricao: str,
                        vazamento_imagem_url: str):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Notificação de Vazamento</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }}
            .content {{
                margin: 20px 0;
                font-size: 16px;
                line-height: 1.6;
            }}
            .content a {{
                color: #4CAF50;
                text-decoration: none;
            }}
            .image-container {{
                text-align: center;
                margin: 20px 0;
            }}
            .image-container img {{
                width: 80%;
                max-width: 500px;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .footer {{
                text-align: center;
                font-size: 14px;
                color: #888888;
                margin-top: 30px;
            }}
            .button {{
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                text-align: center;
            }}
            .button:hover {{
                background-color: #45a049;
            }}
            .note {{
                font-size: 14px;
                color: #888888;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Alerta de Vazamento de Dados</h2>
            </div>
            <div class="content">
                <p>Olá {usuario_nome},</p>
                <p>Um novo vazamento foi identificado relacionado ao seu e-mail:</p>
                <p><strong>Título:</strong> {vazamento_titulo}</p>
                <p><strong>Data:</strong> {vazamento_data}</p>
                <p><strong>Descrição:</strong> {vazamento_descricao}</p>

                <!-- Exibe a imagem do vazamento -->
                <div class="image-container">
                    <img src="{vazamento_imagem_url}" alt="Imagem do Vazamento">
                </div>

                <p>Recomendamos que altere suas senhas imediatamente e esteja atento a possíveis fraudes.</p>
                <a href="#" class="button">Alterar Senha</a>
            </div>
            <div class="footer">
                <p>Atenciosamente,</p>
                <p><strong>Equipe de Segurança Start Cyber 2</strong></p>
                <p class="note">Se você não reconhece esse e-mail, por favor, ignore ou entre em contato conosco.</p>
            </div>
        </div>
    </body>
    </html>
    """


# Função principal da automação
async def automatizar_notificacao_vazamentos():
    logging.info("Iniciando a tarefa de notificação de vazamentos.")
    try:
        db = next(get_db())

        usuarios_com_notificacoes = UsuarioService.obter_lista_de_usuarios_com_notifacao_ativadas(db)
        if not usuarios_com_notificacoes:
            logging.info("Nenhum usuário com notificações ativas foi encontrado.")
            return

        for usuario in usuarios_com_notificacoes:
            vazamentos = await VazamentoService.obter_vazamentos_pelo_email_usuario_e_salva_no_db_sem_verificacao_local(
                db, usuario.email)

            if vazamentos:
                for vazamento in vazamentos:
                    vazamento_data = vazamento.data_vazamento

                    data_formatada = vazamento_data.strftime('%d/%m/%Y')

                    mensagem_html = gerar_mensagem_html(
                        usuario.nome, vazamento.titulo, data_formatada, vazamento.descricao, vazamento.image_uri
                    )

                    # Prepara o assunto
                    assunto = f"Novo vazamento detectado: {vazamento.titulo}"

                    # Envia o e-mail com o HTML
                    await EmailService.enviar_email(usuario.email, assunto, mensagem_html)
                    logging.info(f"E-mail enviado para {usuario.email} sobre o vazamento: {vazamento.titulo}")
            else:
                logging.info(f"Nenhum novo vazamento encontrado para o usuário: {usuario.email}")

    except Exception as e:
        logging.error(f"Erro durante a execução da automação: {e}")
