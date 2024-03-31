import openai
from pydub import AudioSegment
import os

# Credenciales de OpenAI
openai.api_key = ""

# Define la función para transcribir audio usando Whisper API
def transcribe(audio_path):
    # Realiza la llamada a la API de Whisper para transcribir el audio en español
    with open(audio_path, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file, language="en")

    # Obtiene el texto de la transcripción del resultado de la API
    transcript = response['text']
    return transcript

# Define la función para transcribir un audio de más de 30 minutos
def transcribe_audio(audio_path):
    # Carga el archivo de audio utilizando PyDub
    song = AudioSegment.from_file(audio_path)

    # Define la duración máxima de cada trozo en milisegundos (25 minutos)
    max_chunk_duration = 25 * 60 * 1000

    # Divide el audio en trozos más pequeños
    audio_chunks = [song[i:i + max_chunk_duration] for i in range(0, len(song), max_chunk_duration)]

    # Transcribe cada trozo y concatena los resultados
    transcript = ""
    for i, chunk in enumerate(audio_chunks):
        # Exporta el trozo actual a un archivo temporal
        chunk_path = f"temp_chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")

        # Transcribe el trozo utilizando Whisper API en español
        partial_transcript = transcribe(chunk_path)

        # Concatena el texto del trozo al resultado final
        transcript += partial_transcript

        # Elimina el archivo temporal del trozo actual
        os.remove(chunk_path)

    return transcript

# Ruta del archivo de audio a transcribir
audio_path = "C:/Users/TuUsuario/input.mp3"

transcript = transcribe_audio(audio_path)

# Imprime la transcripción
print(transcript)
