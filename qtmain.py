import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTabWidget,QTextEdit , QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
import pyaudio
from lib.AudioRecorder import AudioRecorder
import threading
import argparse
import queue

# Queue for thread log messages
log_queue = queue.Queue()

# Function to capture the console log from the thread
def capture_log_thread(log_queue):
    while True:
        message = log_queue.get()
        if message is None:
            break
        log_text.insertPlainText(message)  # Use insertPlainText to display log messages

# Redirect standard output and error streams to log queue
class StdoutRedirector:
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def write(self, message):
        self.log_queue.put(message)
        self.stdout.write(message)

    def flush(self):
        self.stdout.flush()

# Redirect stdout and stderr
sys.stdout = StdoutRedirector(log_queue)
sys.stderr = StdoutRedirector(log_queue)
# Fonction pour lancer l'enregistrement audio
def start_recording():
    global recording_status  # Utilisation de la variable globale
    # Récupérer les valeurs des widgets de l'interface
    channels_val = channels_entry.text() or "2"
    rate_val = rate_entry.text() or "44100"
    chunk_val = chunk_entry.text() or "1024"
    min_silence_duration_val = min_silence_duration_entry.text() or "30"
    silence_between_songs_threshold_val = silence_between_songs_threshold_entry.text() or "0.1"
    min_music_duration_val = min_music_duration_entry.text() or "46"
    path_val = path_entry.text() or "Files"
    filename_val = filename_entry.text() or ""

    # Créer des arguments à partir des valeurs
    args = argparse.Namespace(
        format=pyaudio.paInt16,
        channels=int(channels_val),
        rate=int(rate_val),
        chunk=int(chunk_val),
        record_threshold=float('inf'),
        min_silence_duration=int(min_silence_duration_val),
        silence_between_songs_threshold=float(silence_between_songs_threshold_val),
        min_music_duration=int(min_music_duration_val),
        path=path_val,
        filename=filename_val
    )

    # Lancer l'enregistrement audio dans un thread pour ne pas bloquer l'interface
    def record_audio_thread():
        recorder = AudioRecorder(args)
        update_status_label(True)
        recorder.start_recording()
        update_status_label(False)

    recording_thread = threading.Thread(target=record_audio_thread)
    recording_thread.start()

def update_status_label(recording_status):
    if recording_status:
        status_label.setText("Statut: ON")
        record_button.setText("Recording in progress")
        record_button.setEnabled(False)
    else:
        status_label.setText("Statut: OFF")
        record_button.setText("Start recording")
        record_button.setEnabled(True)
        

app = QApplication(sys.argv)

# Créer une fenêtre principale
window = QMainWindow()
window.setWindowTitle("Enregistrement audio")
window.resize(400, 400)

# Créer un widget central
central_widget = QWidget()

# Créer un onglet widget
tab_widget = QTabWidget()

# Onglet "Recorder"
tab_recorder = QWidget()
vbox_recorder = QVBoxLayout()

filename_label = QLabel("Nom de base du fichier MP3:")
filename_entry = QLineEdit("")  # Valeur par défaut
path_label = QLabel("Chemin de sortie pour les fichiers MP3:")
path_entry = QLineEdit("")  # Valeur par défaut

# Libellé pour le statut
status_label = QLabel("Statut: OFF")
log_text = QTextEdit()
log_text.setReadOnly(True)

vbox_recorder.addWidget(filename_label)
vbox_recorder.addWidget(filename_entry)
vbox_recorder.addWidget(path_label)
vbox_recorder.addWidget(path_entry)
vbox_recorder.addWidget(status_label)
vbox_recorder.addWidget(log_text)

tab_recorder.setLayout(vbox_recorder)

# Onglet "Param"
tab_params = QWidget()
vbox_params = QVBoxLayout()

channels_label = QLabel("Nombre de canaux audio:")
channels_entry = QLineEdit("2")  # Valeur par défaut
rate_label = QLabel("Taux d'échantillonnage en Hz:")
rate_entry = QLineEdit("44100")  # Valeur par défaut
chunk_label = QLabel("Taille du chunk audio:")
chunk_entry = QLineEdit("1024")  # Valeur par défaut
min_silence_duration_label = QLabel("Durée minimale de silence en secondes:")
min_silence_duration_entry = QLineEdit("30")  # Valeur par défaut
silence_between_songs_threshold_label = QLabel("Seuil de silence entre les chansons:")
silence_between_songs_threshold_entry = QLineEdit("0.1")  # Valeur par défaut
min_music_duration_label = QLabel("Durée minimale de la musique en secondes:")
min_music_duration_entry = QLineEdit("46")  # Valeur par défaut


vbox_params.addWidget(channels_label)
vbox_params.addWidget(channels_entry)
vbox_params.addWidget(rate_label)
vbox_params.addWidget(rate_entry)
vbox_params.addWidget(chunk_label)
vbox_params.addWidget(chunk_entry)
vbox_params.addWidget(min_silence_duration_label)
vbox_params.addWidget(min_silence_duration_entry)
vbox_params.addWidget(silence_between_songs_threshold_label)
vbox_params.addWidget(silence_between_songs_threshold_entry)
vbox_params.addWidget(min_music_duration_label)
vbox_params.addWidget(min_music_duration_entry)

tab_params.setLayout(vbox_params)

# Ajouter les onglets au widget de l'onglet
tab_widget.addTab(tab_recorder, "Recorder")
tab_widget.addTab(tab_params, "Param")

# Ajouter le widget de l'onglet à la fenêtre principale
window.setCentralWidget(tab_widget)

# Bouton "Enregistrer"
record_button = QPushButton("Start recording")
record_button.clicked.connect(start_recording)

# Ajouter le bouton "Enregistrer" en dehors des onglets
button_layout = QVBoxLayout()
button_layout.addWidget(record_button)

# Ajouter le layout du bouton en dehors des onglets
central_layout = QVBoxLayout()
central_layout.addWidget(tab_widget)
central_layout.addLayout(button_layout)

central_widget.setLayout(central_layout)


# Thread to capture and display log messages
log_thread = threading.Thread(target=capture_log_thread, args=(log_queue,))
log_thread.start()






# Create a system tray icon
system_tray_icon = QSystemTrayIcon()
icon = QIcon("Capture.png")  # Replace with the path to your icon file
system_tray_icon.setIcon(icon)

# Create a menu for the system tray icon
tray_menu = QMenu()

# Add actions to the menu
show_action = QAction("Show")
exit_action = QAction("Exit")

# Add the actions to the menu
tray_menu.addAction(show_action)
tray_menu.addAction(exit_action)

# Set the menu for the system tray icon
system_tray_icon.setContextMenu(tray_menu)

# Function to show the main window when "Show" is clicked
def show_main_window():
    window.show()

# Connect the "Show" action to the function
show_action.triggered.connect(show_main_window)

# Add the system tray icon to your application
system_tray_icon.show()

# Définir le widget central de la fenêtre principale
window.setCentralWidget(central_widget)


# Afficher la fenêtre
window.show()

sys.exit(app.exec_())
