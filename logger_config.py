# Importa o módulo de logging para criar e configurar logs
import logging
# Importa o módulo os para manipulação de diretórios e arquivos
import os

# Função que configura o logger
def setup_logger():
    # Define o diretório onde os logs serão armazenados
    log_dir = "logs"
    
    # Se o diretório de logs não existir, cria ele
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Cria o logger com o nome 'FuriaBot'
    logger = logging.getLogger('FuriaBot')
    # Define o nível de log como INFO, ou seja, registra todas as mensagens de nível INFO e superior
    logger.setLevel(logging.INFO)

    # Define o formato padrão dos logs, incluindo data, nome do logger, nível e a mensagem do log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Cria um handler para salvar os logs em um arquivo
    file_handler = logging.FileHandler(os.path.join(log_dir, 'furia_bot.log'))
    # Define o formato dos logs que serão salvos no arquivo
    file_handler.setFormatter(formatter)
    # Define o nível de log do arquivo como INFO
    file_handler.setLevel(logging.INFO)

    # Cria um handler para exibir os logs no console
    console_handler = logging.StreamHandler()
    # Define o formato dos logs que serão exibidos no console
    console_handler.setFormatter(formatter)
    # Define o nível de log do console como INFO
    console_handler.setLevel(logging.INFO)

    # Adiciona ambos os handlers ao logger, para que os logs sejam registrados tanto no arquivo quanto no console
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Retorna o logger configurado
    return logger

# Cria uma instância global do logger configurado
logger = setup_logger()
