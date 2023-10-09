import os
import pyaudio
import time
import threading
import copy
import argparse
import random
import string
from pydub import AudioSegment

class MP3Saver:
    def __init__(self, output_path):
        self.output_path = output_path

    def save_mp3_thread(self, audio_segment, output_filename):
        with self.file_write_lock:
            mp3_path = os.path.join(self.output_path, output_filename)  # Chemin complet du fichier MP3
            audio_copy = copy.deepcopy(audio_segment)
            audio_copy.export(mp3_path, format="mp3")
            print(f"L'enregistrement a été sauvegardé dans '{mp3_path}'")

    def save_mp3(self, audio_segment, output_filename):

        # Verrou pour assurer une écriture de fichier sécurisée
        self.file_write_lock = threading.Lock()
        mp3_thread = threading.Thread(target=self.save_mp3_thread, args=(audio_segment, output_filename))
        mp3_thread.start()


class AudioRecorder:
    def __init__(self, args):
        self.format = args.format
        self.channels = args.channels
        self.rate = args.rate
        self.chunk = args.chunk
        self.record_threshold = args.record_threshold
        self.min_silence_duration = args.min_silence_duration
        self.silence_between_songs_threshold = args.silence_between_songs_threshold
        self.min_music_duration = args.min_music_duration
        self.output_path = args.path  # Chemin de sortie
        self.output_filename_base = args.filename  # Nom de base du fichier MP3
        self.counter = 0

        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(self.output_path, exist_ok=True)

        # Si aucun nom de fichier de base n'est spécifié, choisir un nom de base aléatoire
        if not self.output_filename_base:
            self.output_filename_base = self.generate_random_character_name_base()

        # Initialisation de PyAudio
        self.audio = pyaudio.PyAudio()

        # Configuration du flux audio d'entrée (microphone)
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)

        self.start_time = None
        self.recording = False
        self.silence_start_time = None
        self.audio_segment = None
        
        self.mp3_saver = MP3Saver(self.output_path)  # Créez une instance de MP3Saver

    def generate_random_character_name_base(self):
        character_names = ["alice", "bob", "cinderella", "dumbledore", "elmo", "frodo", "gandalf", "harry", "inigo", "joker", "khan", "luke", "mario", "ned", "obiwan", "pikachu", "quasimodo", "rocky", "spock", "thor", "ursula", "voldemort", "wolverine", "xena", "yoda", "zeus"]
        return random.choice(character_names)

    def generate_output_filename(self):
        self.counter += 1
        return f"{self.output_filename_base}_{self.counter}.mp3"

    def record_audio(self):
        try:
            while True:
                data = self.stream.read(self.chunk)

                audio_data = AudioSegment(
                    data,
                    frame_rate=self.rate,
                    sample_width=self.audio.get_sample_size(self.format),
                    channels=self.channels
                )

                if abs(audio_data.dBFS) < self.record_threshold:
                    if not self.recording:
                        print("Début de l'enregistrement...")
                        self.recording = True
                        self.start_time = time.time()
                        self.audio_segment = AudioSegment.silent(duration=0)
                        self.silence_start_time = None

                if self.recording:
                    self.audio_segment += audio_data

                if abs(audio_data.dBFS) == self.record_threshold:
                    if self.recording:
                        if self.silence_start_time is None:
                            self.silence_start_time = time.time()
                        elif time.time() - self.silence_start_time >= self.silence_between_songs_threshold:
                            print("Arrêt de l'enregistrement...")
                            if time.time() - self.start_time >= self.min_music_duration:
                                output_filename = self.generate_output_filename()
                                self.mp3_saver.save_mp3(self.audio_segment, output_filename)
                            self.audio_segment = None
                            self.recording = False

                            self.start_time = None

                    elif self.silence_start_time and time.time() - self.silence_start_time >= self.min_silence_duration:
                        print("Sortie du programme...")
                        break

        except KeyboardInterrupt:
            pass
        finally:
            # Fermeture du flux audio
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

    def start_recording(self):
        # Créer un thread pour l'enregistrement audio
        audio_thread = threading.Thread(target=self.record_audio)
        audio_thread.start()

        try:
            while True:
                if audio_thread.is_alive():
                    time.sleep(1)
                else:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            # Fermeture du flux audio
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()


def parse_args():
    parser = argparse.ArgumentParser(description="Enregistrement audio avec paramètres personnalisables.")
    parser.add_argument("-f", "--format", type=int, default=pyaudio.paInt16, help="Format audio")
    parser.add_argument("-c", "--channels", type=int, default=1, help="Nombre de canaux audio")
    parser.add_argument("-r", "--rate", type=int, default=44100, help="Taux d'échantillonnage en Hz")
    parser.add_argument("-k", "--chunk", type=int, default=1024, help="Taille du chunk audio")
    parser.add_argument("-t", "--record_threshold", type=float, default=float('inf'), help="Seuil pour commencer l'enregistrement")
    parser.add_argument("-d", "--min_silence_duration", type=int, default=30, help="Durée minimale de silence en secondes pour arrêter définitivement l'enregistrement")
    parser.add_argument("-s", "--silence_between_songs_threshold", type=float, default=0.09, help="Seuil de silence entre les chansons")
    parser.add_argument("-m", "--min_music_duration", type=int, default=60, help="Durée minimale de la musique en secondes")
    parser.add_argument("-p","--path", default="Files", help="Chemin de sortie pour les fichiers MP3")
    parser.add_argument("-n","--filename", help="Nom de base du fichier MP3")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    recorder = AudioRecorder(args)
    recorder.start_recording()
