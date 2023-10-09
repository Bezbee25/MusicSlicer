import tkinter as tk
import argparse

import pyaudio
from lib.AudioRecorder import AudioRecorder
import threading

# Fonction pour lancer l'enregistrement audio
def start_recording():
    # Récupérer les valeurs des widgets de l'interface
    format_val = format_var.get()
    channels_val = channels_var.get()
    rate_val = rate_var.get()
    chunk_val = chunk_var.get()
    record_threshold_val = record_threshold_var.get()
    min_silence_duration_val = min_silence_duration_var.get()
    silence_between_songs_threshold_val = silence_between_songs_threshold_var.get()
    min_music_duration_val = min_music_duration_var.get()
    path_val = path_var.get()
    filename_val = filename_var.get()

    # Créer des arguments à partir des valeurs
    args = argparse.Namespace(
        format=format_val,
        channels=channels_val,
        rate=rate_val,
        chunk=chunk_val,
        record_threshold=record_threshold_val,
        min_silence_duration=min_silence_duration_val,
        silence_between_songs_threshold=silence_between_songs_threshold_val,
        min_music_duration=min_music_duration_val,
        path=path_val,
        filename=filename_val
    )

    # Lancer l'enregistrement audio dans un thread pour ne pas bloquer l'interface
    def record_audio_thread():
        recorder = AudioRecorder(args)
        recorder.start_recording()

    recording_thread = threading.Thread(target=record_audio_thread)
    recording_thread.start()

# Créer la fenêtre principale
root = tk.Tk()
root.title("Enregistrement audio")

# Créer des variables Tkinter pour stocker les valeurs des paramètres
format_var = tk.IntVar(value=pyaudio.paInt16)
channels_var = tk.IntVar(value=1)
rate_var = tk.IntVar(value=44100)
chunk_var = tk.IntVar(value=1024)
record_threshold_var = tk.DoubleVar(value=float('inf'))
min_silence_duration_var = tk.IntVar(value=30)
silence_between_songs_threshold_var = tk.DoubleVar(value=0.1)
min_music_duration_var = tk.IntVar(value=46)
path_var = tk.StringVar(value="Files")
filename_var = tk.StringVar()

# Créer des libellés et des entrées pour chaque paramètre
format_label = tk.Label(root, text="Format audio:")
format_entry = tk.Entry(root, textvariable=format_var)
channels_label = tk.Label(root, text="Nombre de canaux audio:")
channels_entry = tk.Entry(root, textvariable=channels_var)
rate_label = tk.Label(root, text="Taux d'échantillonnage en Hz:")
rate_entry = tk.Entry(root, textvariable=rate_var)
chunk_label = tk.Label(root, text="Taille du chunk audio:")
chunk_entry = tk.Entry(root, textvariable=chunk_var)
record_threshold_label = tk.Label(root, text="Seuil pour commencer l'enregistrement:")
record_threshold_entry = tk.Entry(root, textvariable=record_threshold_var)
min_silence_duration_label = tk.Label(root, text="Durée minimale de silence en secondes:")
min_silence_duration_entry = tk.Entry(root, textvariable=min_silence_duration_var)
silence_between_songs_threshold_label = tk.Label(root, text="Seuil de silence entre les chansons:")
silence_between_songs_threshold_entry = tk.Entry(root, textvariable=silence_between_songs_threshold_var)
min_music_duration_label = tk.Label(root, text="Durée minimale de la musique en secondes:")
min_music_duration_entry = tk.Entry(root, textvariable=min_music_duration_var)
path_label = tk.Label(root, text="Chemin de sortie pour les fichiers MP3:")
path_entry = tk.Entry(root, textvariable=path_var)
filename_label = tk.Label(root, text="Nom de base du fichier MP3:")
filename_entry = tk.Entry(root, textvariable=filename_var)

# Créer un bouton pour lancer l'enregistrement
record_button = tk.Button(root, text="Enregistrer", command=start_recording)

# Disposer les widgets dans la fenêtre
format_label.grid(row=0, column=0, sticky="w")
format_entry.grid(row=0, column=1)
channels_label.grid(row=1, column=0, sticky="w")
channels_entry.grid(row=1, column=1)
rate_label.grid(row=2, column=0, sticky="w")
rate_entry.grid(row=2, column=1)
chunk_label.grid(row=3, column=0, sticky="w")
chunk_entry.grid(row=3, column=1)
record_threshold_label.grid(row=4, column=0, sticky="w")
record_threshold_entry.grid(row=4, column=1)
min_silence_duration_label.grid(row=5, column=0, sticky="w")
min_silence_duration_entry.grid(row=5, column=1)
silence_between_songs_threshold_label.grid(row=6, column=0, sticky="w")
silence_between_songs_threshold_entry.grid(row=6, column=1)
min_music_duration_label.grid(row=7, column=0, sticky="w")
min_music_duration_entry.grid(row=7, column=1)
path_label.grid(row=8, column=0, sticky="w")
path_entry.grid(row=8, column=1)
filename_label.grid(row=9, column=0, sticky="w")
filename_entry.grid(row=9, column=1)
record_button.grid(row=10, columnspan=2)

# Démarrer l'interface Tkinter
root.mainloop()
