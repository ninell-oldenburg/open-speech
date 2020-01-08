# OpenSpeech Project

This is a program to make speech visible. Through a GUI you can record a sentence and get the visible analysis of it afterwards. 
Current state of the art: visualizes pitch, loudness (in decibel) and voice quality (namely: if the utterances is whispered
or not wispered).

# Use

Download all the .py files. You can make your own recording or text me to get sample recordings. Open the program in the terminal
using 'python3 gui.py' and the GUI will open. It comes with instructions (in German). 

# Dependecies

You need Python 3.x as well as the modules numpy, matplotlib, ffmpeg, sounddevice, tkinter, portaudio, pyaudio, parselmouth.

## Problems

This following issue occured to me several times on macOS Catalina: https://github.com/YannickJadoul/Parselmouth/issues/10 
Solved it with installing and uninstalling either python-parselmouth or parselmouth (try both) via pip or pip3, respectively.

# Share

Please use the code and/or edit it. Let me know, what you are going to do with it. I'd be glad to hear. Everything is licensed 
under GNU General Public License.

# Paperwork

I am going to write a Thesis about the program, so please feel free to contact me to get it.
