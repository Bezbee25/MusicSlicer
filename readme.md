# Audio Recorder Readme

This is a Python program for recording audio with customizable parameters. It allows you to capture audio input and save it as MP3 files, with options to control various aspects of the recording process.

## Prerequisites

Before using this program, you need to install the following dependencies:

- [Python](https://www.python.org/) (version 3.x recommended)
- [Pyaudio](https://pypi.org/project/PyAudio/) - A Python library for audio processing.

You can install Pyaudio using pip:

```bash
pip install pyaudio
```

## Usage

To use this program, follow these steps:

1. Clone this repository or download the script.

2. Open a terminal and navigate to the directory containing the script.

3. Run the script with your desired parameters. Here are the available options:

   - `-f` or `--format`: Audio format (default: `pyaudio.paInt16`).
   - `-c` or `--channels`: Number of audio channels (default: `2`).
   - `-r` or `--rate`: Sampling rate in Hz (default: `44100`).
   - `-k` or `--chunk`: Size of the audio chunk (default: `1024`).
   - `-t` or `--record_threshold`: Threshold to start recording (default: `inf`).
   - `-d` or `--min_silence_duration`: Minimum silence duration in seconds to stop recording permanently (default: `30`).
   - `-s` or `--silence_between_songs_threshold`: Silence threshold between songs (default: `0.09`).
   - `-m` or `--min_music_duration`: Minimum music duration in seconds (default: `46`).
   - `-p` or `--path`: Output path for MP3 files (default: `Files`).
   - `-n` or `--filename`: Base filename for MP3 files.

4. The program will start recording audio input based on your specified parameters.

## Example Usage

```bash
python main.py -f 44100 -c 2 -r 1024 -t 0.05 -d 30 -s 0.1 -m 60 -p Output -n recording
```

This command will start recording audio with a 44.1 kHz sampling rate, 2 channels, a chunk size of 1024, a recording threshold of 0.05, a minimum silence duration of 30 seconds to stop recording, a silence threshold of 0.1 between songs, a minimum music duration of 60 seconds, and save the MP3 files in the "Output" directory with the base filename "recording."

## License

This program is open-source and released under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as needed.