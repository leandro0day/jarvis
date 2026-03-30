# 🤖 Jarvis - Asistente de Voz

Un asistente de voz inteligente que utiliza:
- **Whisper** (OpenAI) para reconocimiento de voz (STT)
- **Ollama** como cerebro de IA (LLM)
- **Edge TTS** (Microsoft) para síntesis de voz (TTS)

## 📋 Requisitos Previos

### 1. Ollama
Instala y ejecuta Ollama:

```bash
# Instalar Ollama (macOS)
brew install ollama

# O descarga desde https://ollama.ai

# Iniciar el servidor
ollama serve

# Descargar un modelo (en otra terminal)
ollama pull llama3.2:1b
```

### 2. Dependencias del Sistema

```bash
# macOS
brew install portaudio ffmpeg

# Ubuntu/Debian
sudo apt-get install portaudio19-dev ffmpeg

# Fedora
sudo dnf install portaudio-devel ffmpeg
```

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o en Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 💻 Uso

### Modo Básico
```bash
python main.py
```

### Con Opciones
```bash
# Usar modelo Whisper más grande (mejor precisión)
python main.py --whisper-model medium

# Usar otro modelo de Ollama
python main.py --ollama-model llama3.2

# Modo wake word (espera "Jarvis" antes de escuchar)
python main.py --wake-word

# Todas las opciones
python main.py --whisper-model small --ollama-model llama3.2:1b --tts-voice es-MX-DaliaNeural --wake-word
```

### Opciones Disponibles

| Opción | Descripción | Default |
|--------|-------------|---------|
| `--whisper-model` | Modelo Whisper (tiny, base, small, medium, large) | base |
| `--ollama-model` | Modelo de Ollama | llama3.2:1b |
| `--tts-voice` | Voz de Edge TTS | es-MX-JorgeNeural |
| `--language` | Código de idioma | es |
| `--ollama-url` | URL del servidor Ollama | http://localhost:11434 |
| `--wake-word` | Activar modo wake word | False |

## 🎤 Comandos de Voz

- **"Adiós"** / **"Salir"** - Termina la sesión
- **"Limpiar historial"** - Borra el historial de conversación
- **"Jarvis"** (en modo wake word) - Activa el asistente

## 📁 Estructura del Proyecto

```
jarvis/
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias
├── README.md           # Este archivo
└── src/
    ├── __init__.py
    ├── jarvis.py       # Clase principal del asistente
    ├── stt.py          # Speech-to-Text (Whisper)
    ├── llm.py          # LLM (Ollama)
    └── tts.py          # Text-to-Speech (Coqui)
```

## 🔧 Voces TTS Disponibles

Algunas voces de Edge TTS en español:

- `es-MX-JorgeNeural` - Español mexicano (masculino)
- `es-MX-DaliaNeural` - Español mexicano (femenino)
- `es-ES-AlvaroNeural` - Español de España (masculino)
- `es-ES-ElviraNeural` - Español de España (femenino)
- `es-AR-TomasNeural` - Español argentino (masculino)

Para ver todas las voces disponibles:
```python
from src.tts import TextToSpeech
voices = TextToSpeech.list_voices()
for v in voices:
    if v['Locale'].startswith('es'):
        print(f"{v['ShortName']} - {v['Gender']}")
```

## 🐛 Solución de Problemas

### Error de conexión con Ollama
```bash
# Asegúrate de que Ollama esté corriendo
ollama serve
```

### Error de audio
```bash
# Verifica que el micrófono esté funcionando
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### Modelo no encontrado
```bash
# Descarga el modelo de Ollama
ollama pull llama3.2:1b

# Los modelos de Whisper y TTS se descargan automáticamente
```

## 📝 Licencia

MIT License
