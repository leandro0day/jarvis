"""
LLM module using Ollama
"""
import requests
import json
from typing import Generator, Optional, List, Dict


class OllamaLLM:
    def __init__(
        self, 
        model: str = "llama3.2:1b", 
        base_url: str = "http://localhost:11434",
        system_prompt: Optional[str] = None
    ):
        """
        Initialize Ollama LLM client.
        
        Args:
            model: Ollama model name
            base_url: Ollama API base URL
            system_prompt: System prompt for the assistant
        """
        self.model = model
        self.base_url = base_url
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.conversation_history: List[Dict[str, str]] = []
        
        print(f"🧠 Conectando con Ollama ({model})...")
        self._verify_connection()
        print("✅ Ollama listo")
    
    def _default_system_prompt(self) -> str:
        return """Eres Jarvis, un asistente de voz inteligente y amigable. 
Responde de manera concisa y natural, como si estuvieras hablando.
Evita respuestas muy largas ya que serán leídas en voz alta.
Responde siempre en español a menos que te pidan otro idioma."""
    
    def _verify_connection(self):
        """Verify connection to Ollama server."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if not any(self.model in name for name in model_names):
                print(f"⚠️ Modelo '{self.model}' no encontrado. Modelos disponibles: {model_names}")
                print(f"   Ejecuta: ollama pull {self.model}")
                
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "❌ No se pudo conectar con Ollama. "
                "Asegúrate de que Ollama esté corriendo (ollama serve)"
            )
    
    def chat(self, message: str, stream: bool = False) -> str | Generator[str, None, None]:
        """
        Send a message and get a response.
        
        Args:
            message: User message
            stream: Whether to stream the response
            
        Returns:
            Assistant response (string or generator if streaming)
        """
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        
        if stream:
            return self._stream_response(payload)
        else:
            return self._get_response(payload)
    
    def _get_response(self, payload: dict) -> str:
        """Get complete response from Ollama."""
        print("🤔 Pensando...")
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        assistant_message = result["message"]["content"]
        
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        print(f"🤖 Jarvis: {assistant_message}")
        
        return assistant_message
    
    def _stream_response(self, payload: dict) -> Generator[str, None, None]:
        """Stream response from Ollama."""
        print("🤔 Pensando...")
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        full_response = ""
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "message" in chunk:
                    content = chunk["message"].get("content", "")
                    full_response += content
                    yield content
        
        self.conversation_history.append({
            "role": "assistant",
            "content": full_response
        })
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        print("🗑️ Historial de conversación limpiado")
    
    def set_system_prompt(self, prompt: str):
        """Update the system prompt."""
        self.system_prompt = prompt
