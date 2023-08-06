# MusiSort : Using K-Means Clustering to automatically categorize digital music files.

# Abstract

Downloading music is done by many different people for many different reasons, whether it be for backups, data hoarding, or to listen to music while offline.  However, those who do download music, come across the issue of organizing all the files into categories that they can reference when needed.  The most known way to organize music is by genres.  The issue with genres however, is that they are set by humans and liable to be incorrect, or there could be no genre assigned to the audio file based on how it was retrieved.  Currently, if you want to find what genre a song belongs to, you have to manually search for it online and assign it to the song through a tool.  While this may work for a short list of songs, if you have a larger list (say about 1000 songs), this process becomes much more time consuming.  MusiSort aims to fix this issue by automatically sorting songs into categories based not on genre, but by musical similarity.  Through the use of machine learning, MusiSort can take a large list of audio files, and separate them into a list of categories based on their melodies, tempo, mood, and more.

# Description

AutoMusicSort is a tool being developed to collect music and put them into similar groups or clusters based on their waveform.  The program uses artifical intelligence to check similarities and differences between the different songs.  The main goal of the project is to create a tool which removes the need to manually sort music into different genres as this can be quite a difficult task.  

**Current Project Goals:**

[🏗️] Develop the algorithm to sort songs into categories.

[❌] Optimize the algorithms used to sort songs for faster completion.

[❌] Create a more user friendly terminal interface for easier usage.

[❌] Develop a GUI for more interactivity with the program.

(🏗️ : in progress , ❌ : not started yet , ✅ : completed)

# Information

It is recommended to use wav files when running the program as it provides improved performance.

**Current Dependencies Needed:**

- Typer : pip install "typer[all]"
- Librosa : pip install Librosa
- NumPy : pip install numpy
- ffmpeg : pip install ffmpeg

May be needed:

- OpenCV - pip install opencv-python
- matplotlib - pip install matplotlib

**Run command:**

`python ./src/main.py "folder_path_to_audio_files"`
