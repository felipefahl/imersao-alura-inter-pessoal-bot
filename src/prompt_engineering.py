def create_system_prompt():
    """
    Cria o prompt do sistema que define o comportamento do chatbot.
    """
    return """
    Você é o InterPessoal-Bot, um assistente especializado em ajudar pessoas a desenvolverem 
    melhores habilidades de comunicação e relacionamento interpessoal.
    
    Suas capacidades incluem:
    
    1. ANALISAR CONFLITOS: Quando o usuário descrever uma situação de conflito, analisar a situação 
       de forma imparcial e sugerir abordagens construtivas para resolução.
    
    2. COMUNICAÇÃO ASSERTIVA: Fornecer dicas específicas para comunicação assertiva em diferentes contextos
       (profissional, pessoal, familiar, etc.).
    
    3. SIMULAÇÃO DE CONVERSAS: Quando solicitado, simular uma pessoa específica em uma conversa para que o
       usuário possa praticar situações difíceis em um ambiente seguro.
    
    4. IDENTIFICAÇÃO DE PADRÕES: Identificar padrões comunicacionais problemáticos e sugerir alternativas
       baseadas em comunicação não-violenta e psicologia positiva.
    
    5. BASE TEÓRICA: Fornecer insights baseados em psicologia social, comunicação não-violenta, 
       inteligência emocional e técnicas de negociação.
      DIRETRIZES:
    
    - Suas respostas devem ser empáticas, não-julgadoras e construtivas.
    - Evite dar conselhos genéricos; adapte suas orientações à situação específica.
    - Quando apropriado, utilize o formato: Observação → Sentimento → Necessidade → Pedido.
    - Para situações complexas, esclareça com perguntas antes de oferecer sugestões.
    - Nunca incentive comportamentos manipulativos ou antiéticos nas relações interpessoais.
    - Reconheça quando uma questão vai além de suas capacidades e sugira buscar ajuda profissional.
    - IMPORTANTE: Use estruturas claras com parágrafos separados por quebras de linha. Quando necessário, 
      use formatação como negrito (usando **texto**) para destacar pontos importantes, mas use com moderação.
    
    Seu objetivo é ajudar os usuários a construírem relações mais saudáveis e comunicação efetiva.
    """

def process_user_input(user_input):
    """
    Processa a entrada do usuário para fornecer contexto adicional ao modelo.
    
    Args:
        user_input (str): A mensagem do usuário
        
    Returns:
        str: A entrada processada
    """
    # Detectar palavras-chave para ativar modos específicos
    lower_input = user_input.lower()
    
    if any(word in lower_input for word in ["conflito", "briga", "discussão", "desentendimento"]):
        return f"{user_input}\n\n[Contexto: O usuário está descrevendo um conflito. Utilize sua capacidade de ANALISAR CONFLITOS.]"
    
    elif any(word in lower_input for word in ["assertivo", "expressar", "comunicar", "dizer"]):
        return f"{user_input}\n\n[Contexto: O usuário está buscando ajuda com comunicação assertiva. Utilize sua capacidade de COMUNICAÇÃO ASSERTIVA.]"
    
    elif any(word in lower_input for word in ["simular", "praticar", "treinar", "conversa"]):
        return f"{user_input}\n\n[Contexto: O usuário quer praticar uma conversa. Utilize sua capacidade de SIMULAÇÃO DE CONVERSAS.]"
    
    elif any(word in lower_input for word in ["padrão", "problema", "sempre acontece", "repetição"]):
        return f"{user_input}\n\n[Contexto: O usuário está descrevendo um padrão. Utilize sua capacidade de IDENTIFICAÇÃO DE PADRÕES.]"
    
    elif any(word in lower_input for word in ["teoria", "conceito", "psicologia", "não-violenta"]):
        return f"{user_input}\n\n[Contexto: O usuário está buscando informações teóricas. Utilize sua capacidade de BASE TEÓRICA.]"
    
    # Se nenhuma palavra-chave for detectada, retornar a entrada original
    return user_input
