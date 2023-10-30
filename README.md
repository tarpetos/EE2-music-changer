<h1 style="text-align:center">Music Replacer for Empire Earth 2</h1> 

---

## Overview

This project provides a Python-based utility to replace music files in the game Empire Earth 2, 
allowing users to customize the in-game music according to their preferences.

## Features

- **Music Replacement**: Replace in-game music with custom audio files.
- **Path Management**: Automatically find paths for directories related to the game and custom music.
- **Music Compression**: Has functions to compress MP3 files to make it smaller.

## How to Use

1. **Clone Repository**: Clone this repository to your local machine. Ensure Python 3.10 or above is installed.
2. **Install Dependencies**: Install the required libraries using 
    ```sh
    pip install -r requirements.txt
3. **Run the Application**: Execute the application using 
   ```sh 
   python3 main.py
4. **Application options**: You have 2 options. Back to default music and load your music.
5. **Custom Music Folder Creation**: Create a folder called `custom_music` in `Documents` directory. And place your music there.
6. **For Linux users**: Path to the game music directory will be found automatically. All you need to do is to follow the instructions.
7. **For Windows users**: You need  to set the path to the game directory (or above directory) manually via graphical interface.

## Flet dependencies installation for Linux

```sh
sudo apt-get update
```

```sh
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

## Packaging desktop app
```sh
pyinstaller main.spec
```

## Compatibility

The application is compatible with both Windows and Linux operating systems. Ensure the required dependencies are installed and the game Empire Earth 2 is accessible on the system for successful music replacement.