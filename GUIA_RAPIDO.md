# Guia de Inicialização Rápida

Este guia ajudará você a configurar e executar o InterPessoal-Bot em seu ambiente local.

## Pré-requisitos

- Python 3.8 ou superior
- Conta Google Cloud com acesso à API Gemini
- Chave de API do Google Gemini

## Instalação

1. Clone este repositório:

   ```
   git clone https://github.com/felipefahl/imersao-alura-inter-pessoal-bot.git
   ```

2. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

3. Configure sua chave de API:

   ```
   # Copie o arquivo de exemplo
   cp .env.example .env

   # Edite o arquivo .env e adicione sua chave de API do Google Gemini
   # GOOGLE_API_KEY=sua_chave_api_aqui
   ```

## Executando o Projeto

1. Inicie o servidor Flask:

   ```
   python src/app.py
   ```

2. Abra seu navegador e acesse:

   ```
   http://localhost:5000
   ```

3. Agora você pode interagir com o InterPessoal-Bot!

## Obtendo uma Chave de API do Google Gemini

1. Acesse o [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada e adicione ao seu arquivo `.env`

## Uso do Chatbot

Consulte o arquivo `exemplos_de_uso.md` para exemplos de interações com o chatbot.

## Personalização

Você pode personalizar o comportamento do chatbot editando o prompt do sistema no arquivo `src/prompt_engineering.py`. O método `create_system_prompt()` contém as instruções que definem como o chatbot deve se comportar.
