#!/usr/bin/env python3
"""
Jarvis - Voice Assistant
Main entry point
"""
import argparse
from src.jarvis import Jarvis


def main():
    parser = argparse.ArgumentParser(
        description="Jarvis - Asistente de voz con Whisper, Ollama y Coqui TTS"
    )
    
    parser.add_argument(
        "--whisper-model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Modelo de Whisper para STT (default: base)"
    )
    
    parser.add_argument(
        "--ollama-model",
        type=str,
        default="llama3.2:1b",
        help="Modelo de Ollama para LLM (default: llama3.2:1b)"
    )
    
    parser.add_argument(
        "--tts-voice",
        type=str,
        default="es-MX-JorgeNeural",
        help="Voz de Edge TTS (default: es-MX-JorgeNeural)"
    )
    
    parser.add_argument(
        "--language",
        type=str,
        default="es",
        help="Código de idioma (default: es)"
    )
    
    parser.add_argument(
        "--ollama-url",
        type=str,
        default="http://localhost:11434",
        help="URL de Ollama API (default: http://localhost:11434)"
    )
    
    parser.add_argument(
        "--wake-word",
        action="store_true",
        help="Activar modo wake word (espera 'Jarvis' antes de escuchar)"
    )
    
    args = parser.parse_args()
    
    jarvis = Jarvis(
        whisper_model=args.whisper_model,
        ollama_model=args.ollama_model,
        tts_voice=args.tts_voice,
        language=args.language,
        ollama_url=args.ollama_url
    )
    
    jarvis.run(wake_word_mode=args.wake_word)


if __name__ == "__main__":
    main()
