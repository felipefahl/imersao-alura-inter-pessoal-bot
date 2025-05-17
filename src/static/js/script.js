document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chatBox");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const resetBtn = document.getElementById("resetBtn");
  const suggestionBtns = document.querySelectorAll(".suggestion-btn");
  const rateLimitInfo = document.getElementById("rateLimitInfo");

  // Variável para controlar se já mostramos o aviso de limite
  let hasShownRateLimitWarning = false;

  // Função para mostrar o aviso de limite de taxa
  function showRateLimitWarning(show = true) {
    if (show) {
      rateLimitInfo.classList.add("show");
      // Ocultar automaticamente após 20 segundos
      setTimeout(() => {
        rateLimitInfo.classList.remove("show");
      }, 20000);
    } else {
      rateLimitInfo.classList.remove("show");
    }
  }

  // Scroll para a parte inferior do chat
  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  // Adiciona uma mensagem ao chat
  function addMessageToChat(text, isUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isUser ? "user" : "bot");

    // Processar o texto para substituir caracteres Markdown e adicionar quebras de linha
    const formattedText = processMessageText(text);

    // Usar innerHTML para permitir quebras de linha
    messageDiv.innerHTML = formattedText;
    
    chatBox.appendChild(messageDiv);
    scrollToBottom();
  }

  // Função para processar o texto da mensagem
  function processMessageText(text) {
    if (!text) return "";
    
    // Substituir quebras de linha por tags <br>
    let processed = text.replace(/\n/g, "<br>");
    
    // Remover formatação Markdown comum
    processed = processed
      // Negrito
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/__(.*?)__/g, "<strong>$1</strong>")
      // Itálico
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/_(.*?)_/g, "<em>$1</em>")
      // Remover caracteres Markdown que não foram convertidos
      .replace(/\*\*/g, "")
      .replace(/\*/g, "")
      .replace(/\_\_/g, "")
      .replace(/\_/g, "");
    
    return processed;
  }

  // Exibe indicador de digitação
  function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("message", "bot", "typing-indicator");
    typingDiv.innerHTML = "<p>Digitando...</p>";
    chatBox.appendChild(typingDiv);
    scrollToBottom();
    return typingDiv;
  }

  // Remove o indicador de digitação
  function removeTypingIndicator(indicator) {
    if (indicator && indicator.parentNode === chatBox) {
      chatBox.removeChild(indicator);
    }
  }

  // Envia a mensagem para o backend
  async function sendMessage(message) {
    try {
      // Mostrar indicador de digitação
      const typingIndicator = showTypingIndicator();

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      // Remover indicador de digitação
      removeTypingIndicator(typingIndicator);

      // Verificar se houve um erro na API
      if (data.error || !response.ok) {
        // Se for um erro de limite de taxa (429)
        if (response.status === 429) {
          addMessageToChat(
            data.response ||
              "Limite de requisições atingido. Por favor, aguarde um momento antes de enviar outra mensagem.",
            false
          );
          // Adicionar classe de erro
          chatBox.lastChild.classList.add("error-message");
          
          // Mostrar aviso de limite de taxa
          showRateLimitWarning();
          hasShownRateLimitWarning = true;
        } else {
          // Outros erros
          addMessageToChat(
            data.response ||
              "Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde.",
            false
          );
          // Adicionar classe de erro
          chatBox.lastChild.classList.add("error-message");
        }
      } else {
        // Resposta normal
        addMessageToChat(data.response);
      }
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);

      // Remover indicador de digitação em caso de erro
      const typingIndicators = document.querySelectorAll(".typing-indicator");
      typingIndicators.forEach((indicator) => removeTypingIndicator(indicator));

      // Mensagem de erro genérica
      addMessageToChat(
        "Desculpe, ocorreu um erro de conexão. Por favor, verifique sua internet e tente novamente.",
        false
      );
      // Adicionar classe de erro
      chatBox.lastChild.classList.add("error-message");
    }
  }

  // Evento para o botão de enviar
  sendBtn.addEventListener("click", function () {
    const message = userInput.value.trim();
    if (message.length === 0) return;

    // Adiciona a mensagem do usuário ao chat
    addMessageToChat(message, true);

    // Envia a mensagem para o backend
    sendMessage(message);

    // Limpa o campo de entrada
    userInput.value = "";
  });

  // Evento para pressionar Enter no textarea
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // Previne a quebra de linha padrão
      sendBtn.click();
    }
  });

  // Evento para o botão de resetar
  resetBtn.addEventListener("click", async function () {
    try {
      const response = await fetch("/api/reset", {
        method: "POST",
      });

      const data = await response.json();

      // Verificar se houve um erro na API
      if (data.error || !response.ok) {
        addMessageToChat(
          data.response ||
            "Erro ao reiniciar a conversa. Por favor, tente novamente em alguns instantes.",
          false
        );
        // Adicionar classe de erro
        chatBox.lastChild.classList.add("error-message");
      } else {
        // Limpa o histórico de chat
        chatBox.innerHTML = "";        // Adiciona a mensagem de boas-vindas formatada
        const welcomeMessage = `👋 **Olá! Sou o InterPessoal-Bot**, seu assistente para desenvolvimento de habilidades interpessoais.

Posso ajudar você com:

• Análise de situações de conflito
• Comunicação assertiva
• Simulação de conversas difíceis
• Identificação de padrões de comunicação
• Insights baseados em psicologia social

Como posso ajudá-lo hoje?`;
        
        addMessageToChat(welcomeMessage, false);
        
        // Resetar o flag de aviso de limite de taxa
        hasShownRateLimitWarning = false;
        showRateLimitWarning(false);
      }
    } catch (error) {
      console.error("Erro ao resetar conversa:", error);
      addMessageToChat(
        "Não foi possível reiniciar a conversa. Por favor, tente novamente.",
        false
      );
      // Adicionar classe de erro
      chatBox.lastChild.classList.add("error-message");
    }
  });

  // Evento para os botões de sugestão
  suggestionBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const suggestionText = this.textContent;
      userInput.value = suggestionText;
      sendBtn.click();
    });
  });

  // Inicializa com o scroll na parte inferior
  scrollToBottom();
});
