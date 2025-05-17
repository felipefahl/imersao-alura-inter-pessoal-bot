from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai
from prompt_engineering import create_system_prompt, process_user_input
import time
import logging
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, GoogleAPIError

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a API do Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Configurações do modelo
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Configurações para lidar com limites de taxa
MAX_RETRIES = 3
INITIAL_BACKOFF = 2  # segundos

# Inicializar o modelo Gemini
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Criar um histórico de conversas inicial com o prompt do sistema
system_prompt = create_system_prompt()
chat_session = model.start_chat(history=[
    {"role": "user", "parts": ["Você é um assistente especializado em desenvolvimento de habilidades interpessoais."]},
    {"role": "model", "parts": [system_prompt]}
])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    
    if not user_input:
        return jsonify({"response": "Por favor, digite uma mensagem."})
    
    # Processar a entrada do usuário e adicionar contexto específico
    processed_input = process_user_input(user_input)
      # Obter resposta do modelo com tentativas e backoff exponencial
    retries = 0
    backoff = INITIAL_BACKOFF
    
    while retries < MAX_RETRIES:
        try:
            response = chat_session.send_message(processed_input)
            
            # Processar o texto da resposta para garantir formatação adequada
            formatted_response = process_response_text(response.text)
            
            return jsonify({"response": formatted_response})
        except ResourceExhausted as e:
            logger.warning(f"Limite de taxa atingido: {e}")
            error_msg = "Limite de requisições atingido. "
            
            if "GenerateContentInputTokensPerModelPerMinute" in str(e):
                error_msg += "Você excedeu o limite de tokens de entrada por minuto. "
            
            if retries < MAX_RETRIES - 1:
                error_msg += f"Tentando novamente em {backoff} segundos."
                logger.info(f"Tentativa {retries+1}/{MAX_RETRIES}. Aguardando {backoff} segundos.")
                time.sleep(backoff)
                backoff *= 2  # Backoff exponencial
                retries += 1
            else:
                error_msg += "Por favor, tente novamente em alguns instantes."
                return jsonify({"response": error_msg, "error": True}), 429
        
        except (ServiceUnavailable, GoogleAPIError) as e:
            logger.error(f"Erro na API do Google Gemini: {e}")
            return jsonify({
                "response": "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde.",
                "error": True
            }), 500
    
    # Se todas as tentativas falharem
    return jsonify({
        "response": "Não foi possível completar sua requisição após várias tentativas. Por favor, tente novamente mais tarde.",
        "error": True
    }), 429

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    global chat_session
    try:
        chat_session = model.start_chat(history=[
            {"role": "user", "parts": ["Você é um assistente especializado em desenvolvimento de habilidades interpessoais."]},
            {"role": "model", "parts": [system_prompt]}
        ])
        return jsonify({"response": "Conversa reiniciada com sucesso!"})
    except ResourceExhausted as e:
        logger.warning(f"Limite de taxa atingido durante reinicialização: {e}")
        return jsonify({
            "response": "Não foi possível reiniciar a conversa devido a limites de API. Por favor, tente novamente em alguns instantes.",
            "error": True
        }), 429
    except (ServiceUnavailable, GoogleAPIError) as e:
        logger.error(f"Erro na API do Google Gemini durante reinicialização: {e}")
        return jsonify({
            "response": "Desculpe, ocorreu um erro ao reiniciar a conversa. Por favor, tente novamente mais tarde.",
            "error": True
        }), 500

def process_response_text(text):
    """
    Processa o texto da resposta para garantir formatação adequada.
    
    Args:
        text (str): Texto da resposta do modelo
    
    Returns:
        str: Texto processado com formatação adequada
    """
    if not text:
        return ""
    
    # Garantir que os parágrafos tenham quebras de linha adequadas
    # Substituir quebras de linha únicas por quebras duplas para garantir separação clara dos parágrafos
    processed = text.replace("\n\n", "DOUBLE_NEWLINE")  # Preservar quebras duplas
    processed = processed.replace("\n", "\n\n")  # Transformar quebras simples em duplas
    processed = processed.replace("DOUBLE_NEWLINE", "\n\n")  # Restaurar quebras duplas originais
    
    # Garantir que listas numeradas e com marcadores tenham espaçamento adequado
    processed = processed.replace("\n\n- ", "\n\n- ")
    processed = processed.replace("\n\n1. ", "\n\n1. ")
    
    # Remover espaços em branco extras no início e fim
    processed = processed.strip()
    
    return processed

if __name__ == '__main__':
    app.run(debug=True)
