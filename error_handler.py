# Importa a classe Update da biblioteca do Telegram para lidar com atualizações
from telegram import Update
# Importa ContextTypes para tipagem do contexto de comandos
from telegram.ext import ContextTypes
# Importa o logger para registrar mensagens de erro
from logger_config import logger

# Função de tratamento de erros, chamada automaticamente quando ocorre um erro no bot
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Registra o erro detectado no log para análise posterior
    logger.error(f"Erro detectado: {context.error}")
    
    # Verifica se o update contém uma mensagem
    if isinstance(update, Update) and update.message:
        try:
            # Tenta responder ao usuário com uma mensagem de erro amigável
            await update.message.reply_text("Ocorreu um erro inesperado. Tente novamente mais tarde.")
        except Exception as e:
            # Caso ocorra um erro ao tentar enviar a mensagem, registra esse erro
            logger.error(f"Erro ao tentar responder com mensagem: {e}")
    else:
        # Se não for possível responder (por exemplo, se o update não contiver uma mensagem válida),
        # apenas registra o erro sem tentar responder ao usuário
        logger.error("Não foi possível responder ao usuário, pois não havia uma mensagem válida no update.")
