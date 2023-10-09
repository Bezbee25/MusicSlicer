
import pyaudio
import argparse
from lib.AudioRecorder import AudioRecorder
# sudo modprobe snd-dummy enable=1

def parse_args():
    parser = argparse.ArgumentParser(description="Enregistrement audio avec paramètres personnalisables.")
    parser.add_argument("-f", "--format", type=int, default=pyaudio.paInt16, help="Format audio")
    parser.add_argument("-c", "--channels", type=int, default=2, help="Nombre de canaux audio")
    parser.add_argument("-r", "--rate", type=int, default=44100, help="Taux d'échantillonnage en Hz")
    parser.add_argument("-k", "--chunk", type=int, default=1024, help="Taille du chunk audio")
    parser.add_argument("-t", "--record_threshold", type=float, default=float('inf'), help="Seuil pour commencer l'enregistrement")
    parser.add_argument("-d", "--min_silence_duration", type=int, default=30, help="Durée minimale de silence en secondes pour arrêter définitivement l'enregistrement")
    parser.add_argument("-s", "--silence_between_songs_threshold", type=float, default=0.09, help="Seuil de silence entre les chansons")
    parser.add_argument("-m", "--min_music_duration", type=int, default=46, help="Durée minimale de la musique en secondes")
    parser.add_argument("-p","--path", default="Files", help="Chemin de sortie pour les fichiers MP3")
    parser.add_argument("-n","--filename", help="Nom de base du fichier MP3")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    recorder = AudioRecorder(args)
    recorder.start_recording()
