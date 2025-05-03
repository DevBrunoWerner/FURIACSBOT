# FURIA CS Bot

**FURIA CS Bot** é um bot interativo desenvolvido para fornecer informações em tempo real sobre o time de eSports de Counter-Strike FURIA. O bot foi criado para ser utilizado em plataformas como Telegram, permitindo que os usuários se mantenham informados de maneira personalizada, com atualizações periódicas, interações dinâmicas e controle de preferências.

### Links Importantes

- [Documentação Completa](https://github.com/DevBrunoWerner/FURIACSBOT/tree/b525288c3727e5ff2234a425ae969b38fe43446f/Documenta%C3%A7%C3%A3o)

- [Landing Page](https://681278ca3b4a9.site123.me/)
  
- [Acesse o bot no Telegram](https://t.me/furiac5_bot) 
 
- [Vídeo demo](https://youtu.be/lP32k0X8f0A)

### Funcionalidades

- **Interações dinâmicas**: Comandos como `/start`, `/ajuda`, `/noticia` para facilitar o acesso a informações e interações com o bot.
- **Notícias periódicas**: Envio automático de notícias sobre o time FURIA com base nas preferências do usuário, garantindo que você nunca perca uma atualização importante.
- **Controle de preferências**: Permite que o usuário se inscreva ou cancele a inscrição para o recebimento de notificações de maneira fácil e rápida.
- **Escalabilidade**: A arquitetura modular e flexível permite a expansão do bot para incluir novas funcionalidades e interações.

### Tecnologias Usadas

- **Python**: Linguagem principal utilizada para desenvolver o bot.
- **python-telegram-bot**: Biblioteca essencial para a integração com a API do Telegram e o gerenciamento de interações com os usuários.
- **APIs externas**: Uso da NEWSAPI para buscar e fornecer notícias atualizadas sobre o time FURIA.
- **JSON**: Armazenamento das preferências dos usuários de forma eficiente e simples.

### Como Usar

1. **Iniciar o Bot**: Envie o comando `/start` no Telegram para começar a interagir com o bot.
2. **Comandos disponíveis**: Utilize comandos como `/informações` e `/noticia` para obter informações detalhadas sobre o time.
3. **Personalizar Preferências**: Escolha se deseja ou não receber notificações periódicas de notícias sobre a FURIA, com a facilidade de se inscrever ou cancelar com um simples comando.

### Arquitetura

O **FURIA CS Bot** foi desenvolvido com uma arquitetura modular para garantir a facilidade de manutenção, escalabilidade e flexibilidade:

- **Camada de Interface**: Gerencia a comunicação com os usuários no Telegram.
- **Camada de Lógica de Aplicação**: Processa comandos do usuário e lida com as interações.
- **Camada de Integração**: Conecta-se à API de Notícias para obter as últimas atualizações sobre o time FURIA.
- **Camada de Persistência**: Armazena as preferências dos usuários de forma simples e eficaz utilizando arquivos JSON.
- **Job Scheduler**: Envia automaticamente as notícias de acordo com as preferências do usuário.

### Testes

O bot foi rigorosamente testado para garantir a funcionalidade esperada. Testes unitários cobriram aspectos como o armazenamento das preferências do usuário, o recebimento de notícias e o processamento dos comandos. Além disso, testes de integração asseguram que o fluxo completo de comunicação entre o usuário, o bot e as APIs externas esteja funcionando corretamente.

### Considerações Finais

O **FURIA CS Bot** foi projetado com escalabilidade e flexibilidade em mente. Embora o sistema utilize arquivos JSON para armazenar as preferências dos usuários em sua versão inicial, é altamente recomendada a migração para um banco de dados mais robusto em ambientes de produção com maior volume de usuários. O projeto continua em desenvolvimento e aprimoramento constante.


