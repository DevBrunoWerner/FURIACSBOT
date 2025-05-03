# Importação dos módulos necessários
from telegram.ext import ContextTypes  # Importa a classe ContextTypes para tipagem dos contextos em handlers
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update  # Importa componentes de botões e mensagens
from telegram import ReplyKeyboardMarkup, KeyboardButton  # Importa componentes de botões de teclado normal
from bot_callbacks import noticia_callback, salvar_preferencia, buscar_noticias_furia  # Importa funções de callback e para salvar preferências
from keys import NEWS_API_KEY  # Importa a chave da API de notícias
import requests  # Para realizar as requisições HTTP
from datetime import datetime, timedelta  # Para trabalhar com datas e horários
from logger_config import logger  # Sistema de logs


# Função que responde com a mensagem de boas-vindas
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Bem-vindo ao bot da FURIA! 🔥\n\n"
        "Aqui você pode acompanhar as últimas notícias, resultados e informações sobre o time de CS da FURIA.\n\n"
        "Use os comandos disponíveis do lado da caixa de texto para interagir com o bot, ou digite /help \n\n")

# Função que envia uma lista de comandos disponíveis
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
🤖 Comandos disponíveis:
/start - Inicia o bot.
/links - Envia links úteis sobre a FURIA. 
/proximojogo - Exibe informações sobre o próximo jogo.
/ultimoresultado - Mostra o resultado do último jogo.
/elenco - Lista o elenco atual da FURIA.
/informacoes - Mostra opções de informações sobre o time.
/titulos - Mostra os títulos conquistados pela FURIA.
/noticia - Envia uma notícia e pergunta se você quer receber notícias diárias.
/cancelar - Cancela a assinatura de notícias
/ultimasnoticias - Envia duas últimas notícias sobre a FURIA.
/help ou /ajuda - Mostra esta mensagem de ajuda.

- As notícias são enviadas diariamente.
- Você pode cancelar a assinatura a qualquer momento usando o comando /cancelar.

Use os botões do menu para navegar facilmente! 🔥
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Função que responde com a informação de que o próximo jogo não foi definido
async def proximojogo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("O próximo jogo da FURIA não foi definido ainda. Fique ligado! nas redes sociais. Use o comando /links para ver as redes sociais da FURIA.")

# Função que envia informações sobre o último resultado da FURIA
async def ultimoresultado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("A FURIA perdeu para a The MongolZ por 2x0 no último jogo.")

# Função que envia o elenco atual da FURIA
async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Elenco atual:\nTitulares: MOLODOY, YEKINDAR, FalleN, KSCERATO e yuurih.\n \nReservas: skullz e chelo\n \nFonte: https://draft5.gg/equipe/330-FURIA")

async def titulos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Títulos conquistados:\n\n 1º - ESL Pro League season 12 NA \n 2º - Esports Championship Series Season 7 Finals \n 3º-4º - IEM Season XVII - Dallas \n 3º-4º - IEM Rio 2024 \n 3º-4º - ESL Pro League Season 15 \n 3º-4º - ESL Pro League Season 13 \n 3º-4º - ESL One: Cologne 2020 Online NA \n 3º-4º - DreamHack Masters Dallas 2019")

# Função que envia uma notícia e pergunta se o usuário quer receber atualizações diárias
async def noticia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    noticias = buscar_noticias_furia()  # Chama a função que busca as notícias sobre a FURIA
    
    if noticias and "articles" in noticias:  # Verifica se a resposta contém notícias
        artigo = noticias["articles"][0]  # Pega a primeira notícia
        titulo = artigo.get("title", "Título não encontrado")  # Pega o título da notícia
        descricao = artigo.get("description", "Descrição não encontrada")  # Pega a descrição da notícia
        link = artigo.get("url", "Link não encontrado")  # Pega o link da notícia
        imagem = artigo.get("urlToImage")  # Pega a imagem, se houver
        
        # Criação da legenda da notícia com formatação Markdown
        legenda = f"📰 *{titulo}*\n{descricao}\n[Leia mais]({link})"

        try:
            if imagem:
                # Envia a notícia com a imagem, caso haja
                await update.message.reply_photo(photo=imagem, caption=legenda, parse_mode="Markdown")
            else:
                # Envia a notícia sem imagem
                await update.message.reply_text(legenda, parse_mode="Markdown")
            
            # Pergunta ao usuário se ele quer receber notícias diárias
            await update.message.reply_text(
                "Você gostaria de receber notícias diárias sobre a FURIA?",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Sim", callback_data="noticia_sim")],
                    [InlineKeyboardButton("Não", callback_data="noticia_nao")]
                ])
            )
        except Exception as e:
            logger.error(f"Erro ao enviar a notícia: {e}")  # Loga o erro em caso de falha ao enviar a notícia
            await update.message.reply_text("Houve um erro ao tentar enviar a notícia. Tente novamente mais tarde.")
    else:
        await update.message.reply_text("Não foi possível buscar as notícias no momento. Tente novamente mais tarde.")

# Função que envia as duas últimas notícias sobre a FURIA
async def ultimasnoticias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    noticias = buscar_noticias_furia()  # Chama a função para buscar as notícias
    
    if noticias and "articles" in noticias:  # Verifica se há notícias na resposta
        try:
            # Envia as duas primeiras notícias
            for artigo in noticias["articles"][:2]:
                titulo = artigo.get("title", "Título não encontrado")
                descricao = artigo.get("description", "Descrição não encontrada")
                link = artigo.get("url", "Link não encontrado")
                imagem = artigo.get("urlToImage")
                
                legenda = f"📰 *{titulo}*\n{descricao}\n[Leia mais]({link})"

                # Envia a notícia com ou sem imagem, dependendo da disponibilidade
                if imagem:
                    await update.message.reply_photo(photo=imagem, caption=legenda, parse_mode="Markdown")
                else:
                    await update.message.reply_text(legenda, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Erro ao enviar as notícias: {e}")  # Loga o erro em caso de falha
            await update.message.reply_text("Houve um erro ao tentar enviar as notícias. Tente novamente mais tarde.")
    else:
        await update.message.reply_text("Não foi possível buscar as notícias no momento. Tente novamente mais tarde.")

# Função que envia links úteis sobre a FURIA
async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """Aqui estão os principais links oficiais da FURIA Esports:

    Site oficial: https://www.furia.gg

    Twitter/X:  https://x.com/FURIA

    Instagram: https://www.instagram.com/furiagg

    Facebook: https://www.facebook.com/furiagg

    YouTube: https://www.youtube.com/c/FURIAggCS

Esses canais oferecem informações sobre os times, jogadores, competições e novidades da organização.""")
    
# Função que exibe um menu com opções de infos sobre o time
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard_informacoes = [
        [InlineKeyboardButton("Formação", callback_data="formacao")],
        [InlineKeyboardButton("Último Resultado", callback_data="ultimoresultado")],
        [InlineKeyboardButton("Próxima Partida", callback_data="proximojogo")],
        [InlineKeyboardButton("Títulos", callback_data="titulos")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_informacoes)
    await update.message.reply_text("Escolha uma opção sobre o time:", reply_markup=reply_markup)

# Função que cancela a assinatura de notícias do usuário
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    salvar_preferencia(chat_id, False)  # Chama a função para salvar a preferência de não receber notícias
    await update.message.reply_text("Assinatura de notícias cancelada. Você não receberá mais atualizações diárias.")
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal() # Remove o job agendado para envio de notícias periódicas