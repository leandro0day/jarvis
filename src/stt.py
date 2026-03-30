"""
Speech-to-Text module using OpenAI Whisper
"""
import whisper
import numpy as np
import sounddevice as sd
import queue
import threading
from typing import Optional, Callable


class SpeechToText:
    def __init__(self, model_name: str = "base", language: str = "es"):
        """
        Initialize Whisper STT.
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
            language: Language code for transcription
        """
        print(f"🎤 Cargando modelo Whisper '{model_name}'...")
        self.model = whisper.load_model(model_name)
        self.language = language
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self._recording_thread: Optional[threading.Thread] = None
        print("✅ Whisper listo")
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        if status:
            print(f"⚠️ Audio status: {status}")
        self.audio_queue.put(indata.copy())
    
    def record_audio(self, duration: float = 5.0) -> np.ndarray:
        """
        Record audio for a specified duration.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Audio data as numpy array
        """
        print(f"🎙️ Grabando por {duration} segundos...")
        
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()
        
        return audio_data.flatten()
    
    def record_until_silence(
        self, 
        silence_threshold: float = 0.01, 
        silence_duration: float = 1.5,
        max_duration: float = 30.0
    ) -> np.ndarray:
        """
        Record audio until silence is detected.
        
        Args:
            silence_threshold: RMS threshold for silence detection
            silence_duration: Duration of silence to stop recording
            max_duration: Maximum recording duration
            
        Returns:
            Audio data as numpy array
        """
        print("🎙️ Escuchando... (habla ahora)")
        
        audio_chunks = []
        silence_samples = 0
        silence_samples_threshold = int(silence_duration * self.sample_rate / 1024)
        max_samples = int(max_duration * self.sample_rate / 1024)
        
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
            blocksize=1024,
            callback=self._audio_callback
        ):
            samples_recorded = 0
            while samples_recorded < max_samples:
                try:
                    chunk = self.audio_queue.get(timeout=0.1)
                    audio_chunks.append(chunk)
                    samples_recorded += 1
                    
                    rms = np.sqrt(np.mean(chunk**2))
                    
                    if rms < silence_threshold:
                        silence_samples += 1
                    else:
                        silence_samples = 0
                    
                    if silence_samples >= silence_samples_threshold and len(audio_chunks) > 10:
                        print("🔇 Silencio detectado")
                        break
                        
                except queue.Empty:
                    continue
        
        if audio_chunks:
            return np.concatenate(audio_chunks).flatten()
        return np.array([], dtype=np.float32)
    
    def transcribe(self, audio: np.ndarray) -> str:
        """
        Transcribe audio to text.
        
        Args:
            audio: Audio data as numpy array
            
        Returns:
            Transcribed text
        """
        if len(audio) == 0:
            return ""
        
        print("📝 Transcribiendo...")
        
        result = self.model.transcribe(
            audio,
            language=self.language,
            fp16=False
        )
        
        text = result["text"].strip()
        print(f"💬 Escuché: {text}")
        
        return text
    
    def listen(self, duration: Optional[float] = None) -> str:
        """
        Listen and transcribe speech.
        
        Args:
            duration: If provided, record for this duration. Otherwise, record until silence.
            
        Returns:
            Transcribed text
        """
        if duration:
            audio = self.record_audio(duration)
        else:
            audio = self.record_until_silence()
        
        return self.transcribe(audio)
