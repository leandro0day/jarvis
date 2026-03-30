"""
Text-to-Speech module using Edge TTS (Microsoft)
"""
import edge_tts
import asyncio
import tempfile
import os
from typing import Optional
import pygame


class TextToSpeech:
    def __init__(
        self, 
        voice: str = "es-MX-JorgeNeural",
        rate: str = "+0%",
        volume: str = "+0%"
    ):
        """
        Initialize Edge TTS.
        
        Args:
            voice: Voice name. Some Spanish options:
                - es-MX-JorgeNeural (Mexican Spanish, male)
                - es-MX-DaliaNeural (Mexican Spanish, female)
                - es-ES-AlvaroNeural (Spain Spanish, male)
                - es-ES-ElviraNeural (Spain Spanish, female)
                - es-AR-TomasNeural (Argentine Spanish, male)
            rate: Speech rate (e.g., "+10%", "-10%")
            volume: Volume adjustment (e.g., "+10%", "-10%")
        """
        print(f"🔊 Inicializando TTS con voz '{voice}'...")
        
        self.voice = voice
        self.rate = rate
        self.volume = volume
        
        pygame.mixer.init()
        
        print("✅ TTS listo")
    
    def _run_async(self, coro):
        """Run async coroutine in sync context."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    
    async def _generate_audio(self, text: str, output_path: str):
        """Generate audio file from text."""
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume
        )
        await communicate.save(output_path)
    
    def speak(self, text: str, blocking: bool = True):
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to speak
            blocking: Whether to wait for playback to complete
        """
        if not text.strip():
            return
        
        print(f"🗣️ Hablando: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            temp_path = f.name
        
        try:
            self._run_async(self._generate_audio(text, temp_path))
            
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            if blocking:
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
        finally:
            try:
                pygame.mixer.music.unload()
                os.unlink(temp_path)
            except:
                pass
    
    def speak_to_file(self, text: str, output_path: str):
        """
        Convert text to speech and save to file.
        
        Args:
            text: Text to speak
            output_path: Output audio file path
        """
        if not text.strip():
            return
        
        self._run_async(self._generate_audio(text, output_path))
        print(f"💾 Audio guardado en: {output_path}")
    
    @staticmethod
    def list_voices() -> list:
        """List available voices."""
        async def get_voices():
            voices = await edge_tts.list_voices()
            return voices
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(get_voices())
    
    def speak_streaming(self, text_generator, sentence_delimiter: str = "."):
        """
        Speak text as it's being generated (for streaming LLM responses).
        
        Args:
            text_generator: Generator yielding text chunks
            sentence_delimiter: Character to split sentences
        """
        buffer = ""
        
        for chunk in text_generator:
            buffer += chunk
            
            while sentence_delimiter in buffer:
                sentence, buffer = buffer.split(sentence_delimiter, 1)
                sentence = sentence.strip()
                if sentence:
                    self.speak(sentence + sentence_delimiter)
        
        if buffer.strip():
            self.speak(buffer.strip())
