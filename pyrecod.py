import pyaudio
from pydub import AudioSegment
import time
import threading
import copy

# Paramètres d'enregistrement
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_THRESHOLD = float('inf')  # Seuil pour commencer l'enregistrement
MIN_SILENCE_DURATION = 30  # Durée minimale de silence en secondes pour arrêter définitivement l'enregistrement
SILENCE_BETWEEN_SONGS_THRESHOLD = 0.02  # Seuil de silence entre les chansons
MIN_MUSIC_DURATION = 60

# Initialisation de PyAudio
audio = pyaudio.PyAudio()

# Configuration du flux audio d'entrée (microphone)
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

start_time = None
recording = False
silence_start_time = None
audio_segment = None
counter = 0  # Compteur pour le nom des fichiers MP3

# Verrou pour assurer une écriture de fichier sécurisée
file_write_lock = threading.Lock()

def save_mp3_thread(audio_segment, counter):
    with file_write_lock:
        mp3_filename = f"enregistrement_{counter}.mp3"
        mp3_filename = mp3_filename.replace(" ", "_")
        audio_copy = copy.deepcopy(audio_segment)
        audio_copy.export(mp3_filename, format="mp3")
        print(f"L'enregistrement a été sauvegardé dans '{mp3_filename}'")

def save_mp3(audio_segment, counter):
    mp3_thread = threading.Thread(target=save_mp3_thread, args=(audio_segment, counter))
    mp3_thread.start()

def record_audio():
    global start_time, recording, silence_start_time, audio_segment, counter
    try:
        while True:
            data = stream.read(CHUNK)
            
            audio_data = AudioSegment(
                data,
                frame_rate=RATE,
                sample_width=audio.get_sample_size(FORMAT),
                channels=CHANNELS
            )
            
            if abs(audio_data.dBFS) < RECORD_THRESHOLD:
                if not recording:
                    print("Début de l'enregistrement...")
                    recording = True
                    start_time = time.time()
                    audio_segment = AudioSegment.silent(duration=0)
            
            if recording:
                audio_segment += audio_data
            # print(type(audio_data.dBFS))
            if abs(audio_data.dBFS) == RECORD_THRESHOLD:
                if recording:
                    if silence_start_time is None:
                        silence_start_time = time.time()
                    elif time.time() - silence_start_time >= SILENCE_BETWEEN_SONGS_THRESHOLD:
                        print("Arrêt de l'enregistrement...")
                        if time.time() - start_time >= MIN_MUSIC_DURATION:
                            save_mp3(audio_segment, counter)
                            counter += 1
                        audio_segment = None
                        recording = False
                        silence_start_time = None
                        start_time = None

                    elif time.time() - silence_start_time >= MIN_SILENCE_DURATION:
                        print("Sortie du programme...")
                        break
                else:
                    silence_start_time = None
    except KeyboardInterrupt:
        pass
    finally:
        # Fermeture du flux audio
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Créer un thread pour l'enregistrement audio
audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

try:
    while True:
        if audio_thread.is_alive():
            time.sleep(1)  # Attendre 1 seconde pour éviter de surcharger le processeur
        else:
            break
except KeyboardInterrupt:
    pass
finally:
    # Fermeture du flux audio
    stream.stop_stream()
    stream.close()
    audio.terminate()
