import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
import logging
from respostas import respostas
from datetime import datetime, timedelta, date
from keys import NEWS_API_KEY 


# Configuração do logger para registrar erros ou eventos
logger = logging.getLogger(__name__)

# Função que busca as notícias sobre a FURIA através da API de notícias
def buscar_noticias_furia():
    try:
        # Construção da URL da API para buscar notícias sobre a FURIA
        hoje = datetime.now().date()
        duas_semanas_atras = hoje - timedelta(days=14)
        url = f"https://newsapi.org/v2/everything?q=FURIA&language=pt&from={duas_semanas_atras.strftime('%Y-%m-%d')}&to={hoje.strftime('%Y-%m-%d')}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        
        response = requests.get(url)  # Faz a requisição à API
        response.raise_for_status()  # Lança exceção se a resposta não for ok
        return response.json()  # Retorna os dados no formato JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar notícias: {e}")  # Loga o erro em caso de falha na requisição
        return None  # Retorna None em caso de erro


# Função para salvar a preferência do usuário em um arquivo JSON
def salvar_preferencia(chat_id, recebe_noticias):
    # Chama a função 'carregar_preferencias' para carregar as preferências existentes no arquivo
    preferencias = carregar_preferencias()
    # Atualiza ou adiciona a preferência do usuário, usando o chat_id como chave
    preferencias[chat_id] = recebe_noticias
    # Abre o arquivo 'preferencias.json' no modo escrita
    with open("preferencias.json", "w") as file:
        # Salva o dicionário de preferências atualizado no arquivo JSON
        json.dump(preferencias, file)

# Função para carregar as preferências de um arquivo
def carregar_preferencias():
    try:
        # Tenta abrir e ler o arquivo 'preferencias.json'
        with open("preferencias.json", "r") as file:
            # Retorna o conteúdo do arquivo como um dicionário
            return json.load(file)
    except FileNotFoundError:
        # Se o arquivo não for encontrado, retorna um dicionário vazio
        return {}

# Função que é chamada quando o usuário interage com um botão de callback (como "Sim" ou "Não")
async def noticia_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtém a consulta de callback (dados do botão pressionado)
    query = update.callback_query
    # Responde à consulta para remover o ícone de "carregando"
    await query.answer()

    # Obtém o ID do chat (conversa do usuário)
    chat_id = query.message.chat_id

    # Verifica qual botão foi pressionado
    if query.data == "noticia_sim":
        # Se "Sim", o usuário quer receber notícias, então salvamos a preferência como True
        salvar_preferencia(chat_id, True)
        context.job_queue.run_repeating(
            enviar_noticia_periodica,
            interval=30,  # Intervalo de teste (intervalo de 24 horas )
            # interval=86400,   Intervalo de 24 horas.
            first=0,
            chat_id=chat_id,
            name=str(chat_id)
        )
    elif query.data == "noticia_nao":
        # Se "Não", o usuário não quer receber notícias, então salvamos a preferência como False
        salvar_preferencia(chat_id, False)

    # Busca a resposta associada ao botão pressionado no dicionário 'respostas'
    resposta = respostas.get(query.data)
    if resposta:
        try:
            # Tenta editar a mensagem original com a resposta apropriada
            await query.edit_message_text(resposta)
        except Exception as e:
            # Se houver um erro ao tentar editar a mensagem, registra o erro no logger
            logger.error(f"Erro ao editar a mensagem: {e}")
            # Responde ao usuário com uma mensagem de erro
            await query.message.reply_text("Houve um erro ao processar sua escolha, tente novamente mais tarde.")
    else:
        # Se não houver resposta para o tipo de dados do botão, informa que a opção é inválida
        await query.edit_message_text("Opção inválida.")

# Função que trata outros botões ou interações com o bot
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtém a consulta de callback (dados do botão pressionado)
    query = update.callback_query
    # Responde à consulta para remover o ícone de "carregando"
    await query.answer()

    # Busca a resposta associada ao botão pressionado no dicionário 'respostas'
    resposta = respostas.get(query.data)
    if resposta:
        # Se houver uma resposta válida, edita a mensagem original com a resposta
        await query.edit_message_text(resposta)
    else:
        # Se a opção for inválida, informa ao usuário que a opção escolhida não é válida
        await query.edit_message_text("Opção inválida.")
async def enviar_noticia_periodica(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    preferencias = carregar_preferencias()
    if not preferencias.get(str(chat_id), False):  # respeita a config do JSON
        return

    noticias = buscar_noticias_furia()
    if noticias and "articles" in noticias:
        artigo = noticias["articles"][0]
        titulo = artigo.get("title", "Sem título")
        descricao = artigo.get("description", "")
        link = artigo.get("url", "")
        mensagem = f"📰 *{titulo}*\n{descricao}\n[Leia mais]({link})"

        try:
            await context.bot.send_message(chat_id=chat_id, text=mensagem, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Erro ao enviar notícia periódica: {e}")