# Importação dos módulos necessários
from telegram.ext import Application, CommandHandler, CallbackQueryHandler  # Componentes principais do bot
from bot_commands import start, help_command, proximojogo, ultimoresultado, elenco, noticia, links_command, ultimasnoticias, info_command, cancel_command, titulos
from bot_callbacks import button_handler, noticia_callback  # Handlers para botões interativos
from logger_config import logger  # Sistema de logs
from error_handler import error_handler  # Handler de erros
from keys import BOT_TOKEN  # Token do bot

def main():
    # Inicializa o bot com o token
    application = Application.builder().token(BOT_TOKEN).build()  # Inicia o bot com o token obtido em keys.py
    
    # Registra todos os handlers de comando
    application.add_handler(CommandHandler("start", start))  # Comando '/start' chama a função 'start'
    application.add_handler(CommandHandler("help", help_command))  # Comando '/help' em inglês chama a função 'help_command'
    application.add_handler(CommandHandler("ajuda", help_command))  # Comando '/ajuda' em português chama a função 'help_command'
    application.add_handler(CommandHandler("links", links_command))  # Comando '/links' exibe links úteis
    application.add_handler(CommandHandler("ultimasnoticias", ultimasnoticias))  # Comando '/ultimasnoticias' exibe as últimas 2 notícias
    application.add_handler(CommandHandler("cancelar", cancel_command))  # Comando '/cancelar' cancela inscrição de notícias
    application.add_handler(CommandHandler("informacoes", info_command))  # Comando '/informacoes' exibe opções sobre o time
    application.add_handler(CommandHandler("titulos", titulos))  # Comando '/titulos' exibe os títulos conquistados
    application.add_handler(CommandHandler("proximojogo", proximojogo))  # Comando '/proximojogo' exibe info sobre o próximo jogo
    application.add_handler(CommandHandler("ultimoresultado", ultimoresultado))  # Comando '/ultimoresultado' exibe o último resultado
    application.add_handler(CommandHandler("elenco", elenco))  # Comando '/elenco' exibe a lista de jogadores
    application.add_handler(CommandHandler("noticia", noticia))  # Comando '/noticia' envia notícias sobre o time
    # Handlers para callbacks de botões
    application.add_handler(CallbackQueryHandler(noticia_callback, pattern="^noticia_"))  # Callbacks para interações de notícias (com 'noticia_' no início)
    application.add_handler(CallbackQueryHandler(button_handler))  # Callbacks gerais para outras interações de botões
    # Registra o handler de erros
    application.add_error_handler(error_handler)  # Registra o handler de erros para lidar com exceções
    # Inicia o bot
    print("Bot iniciado. Pressione Ctrl+C para parar.")  # Mensagem indicando que o bot foi iniciado
    application.run_polling()  # Inicia o polling, ouvindo por mensagens e interações do usuário

# Ponto de entrada do programa
if __name__ == "__main__":
    main()  # Chama a função main para iniciar o bot
