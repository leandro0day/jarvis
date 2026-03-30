"""
Jarvis - Main voice assistant class
"""
from typing import Optional
from .stt import SpeechToText
from .llm import OllamaLLM
from .tts import TextToSpeech


class Jarvis:
    def __init__(
        self,
        whisper_model: str = "base",
        ollama_model: str = "llama3.2:1b",
        tts_voice: str = "es-MX-JorgeNeural",
        language: str = "es",
        ollama_url: str = "http://localhost:11434",
        system_prompt: Optional[str] = None
    ):
        """
        Initialize Jarvis voice assistant.
        
        Args:
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            ollama_model: Ollama model name
            tts_voice: Edge TTS voice name
            language: Language code
            ollama_url: Ollama API URL
            system_prompt: Custom system prompt for the LLM
        """
        print("=" * 50)
        print("🤖 Inicializando Jarvis...")
        print("=" * 50)
        
        self.stt = SpeechToText(model_name=whisper_model, language=language)
        self.llm = OllamaLLM(
            model=ollama_model, 
            base_url=ollama_url,
            system_prompt=system_prompt
        )
        self.tts = TextToSpeech(voice=tts_voice)
        
        self.wake_words = ["jarvis", "oye jarvis", "hey jarvis"]
        self.exit_words = ["adiós", "adios", "salir", "terminar", "apágate", "apagate"]
        
        print("=" * 50)
        print("✅ Jarvis está listo!")
        print("=" * 50)
    
    def process_command(self, text: str) -> tuple[str, bool]:
        """
        Process a voice command.
        
        Args:
            text: Transcribed text
            
        Returns:
            Tuple of (response, should_exit)
        """
        text_lower = text.lower().strip()
        
        if not text_lower:
            return "", False
        
        if any(word in text_lower for word in self.exit_words):
            return "Hasta luego, que tengas un buen día.", True
        
        if "limpiar historial" in text_lower or "borrar historial" in text_lower:
            self.llm.clear_history()
            return "Historial de conversación limpiado.", False
        
        response = self.llm.chat(text)
        return response, False
    
    def run_once(self) -> bool:
        """
        Run one interaction cycle.
        
        Returns:
            False if should exit, True otherwise
        """
        text = self.stt.listen()
        
        if not text.strip():
            return True
        
        response, should_exit = self.process_command(text)
        
        if response:
            self.tts.speak(response)
        
        return not should_exit
    
    def run(self, wake_word_mode: bool = False):
        """
        Run the main assistant loop.
        
        Args:
            wake_word_mode: If True, wait for wake word before processing
        """
        print("\n🎤 Jarvis está escuchando...")
        print("   Di 'adiós' para terminar\n")
        
        self.tts.speak("Hola, soy Jarvis. ¿En qué puedo ayudarte?")
        
        try:
            while True:
                if wake_word_mode:
                    print("\n💤 Esperando wake word...")
                    text = self.stt.listen(duration=3.0)
                    
                    if not any(word in text.lower() for word in self.wake_words):
                        continue
                    
                    self.tts.speak("Sí, dime")
                
                if not self.run_once():
                    self.tts.speak("Hasta luego, que tengas un buen día.")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n👋 Jarvis apagado por el usuario")
            self.tts.speak("Hasta luego")
