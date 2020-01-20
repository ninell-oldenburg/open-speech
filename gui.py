#
# OpenSpeech Project
# Ninell Oldenburg
# Univesity of Potsdam & University of Dramatic Art »Ernst Busch«, Berlin
# Licensed under GNU General Public License
# Python 3.6
#

import tkinter as tk
from tkinter import *
from tkinter import font
import recorder as reco
from analysis import Main
from plot import Plotting
import utt

# Julian Jungel
# University of Dramatic Art »Ernst Busch«, Berlin
# Function plot_analysis2() for Unity-Interface
from shutil import copyfile
import time
import argparse
from pythonosc import udp_client

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.body_font = font.Font(family='Helvetica', size=13)
        self.geometry("1000x400")
        self.QUIT = Button(self, text="Exit", command=self.quit)
        self.QUIT.pack({"side": "top"})
        self.text = list(utt.data['examples'].keys())[0]

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Text, Analyze, Instruct):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def set_text(self, text):
        print('old text: ' + self.text)
        self.text = text
        print('new text: ' + self.text)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to OpenSpeech!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        welcome = utt.data['welcome']['welcome_text']
        self.l = tk.Label(self, text=welcome, font=controller.body_font)
        self.l.pack()

        self.button = Button(self, text='Aufnahme', command=lambda: controller.show_frame("Text"))
        self.button.pack({"anchor": "s"})

        self.button = Button(self, text='Wie geht das?', command=lambda: controller.show_frame("Instruct"))
        self.button.pack({"anchor": 's'})


class Text(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcher Satz soll aufgenommen werden?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.running = None

        OPTIONS = list(utt.data['examples'].keys())

        variable = StringVar(self)
        variable.set(OPTIONS[0])

        w = OptionMenu(self, variable, *OPTIONS)
        w.pack()

        button = Button(self, text="Text anzeigen", command=lambda: self.show_text(variable.get()))
        button.pack()

        default = OPTIONS[0]
        self.var = utt.data['examples'][default][0]
        self.l = tk.Label(self, text=self.var, font=controller.body_font)
        self.l.pack({"anchor": 's'})

        self.button_rec = Button(self, text='Start Aufnahme', command=self.start)
        self.button_rec.pack({"anchor": 's'})

        self.button_stop = Button(self, text='Stop Aufnahme', command=self.stop)
        self.button_stop.pack({"anchor": 's'})

        button_ana = tk.Button(self, text="Analysieren", command=lambda: controller.show_frame("Analyze"))
        button_ana.pack({"anchor": 's'})

        button_back = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button_back.pack({"anchor": 's'})

        self.rec = reco.Recorder(channels=2)

    def show_text(self,name):
        self.controller.set_text(name)
        text = utt.data['examples'][name][0]
        self.l.configure(text=text)

    def stop(self):
        self.running
        if self.running is not None:
            self.running.stop_recording()
            self.running.close()
            self.running = None
        else:
            print('not runnning')

    def start(self):
        self.running
        if self.running is not None:
            print('already running')
        else:
            self.running = self.rec.open('nonblocking.wav','wb')
            self.running.start_recording()


class Instruct(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Wie geht das?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        instruct = utt.data['welcome']['instructions']
        text = tk.Label(self, text=instruct, font=controller.body_font)
        text.pack()

        button1 = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button1.pack({"anchor": 's'})


class Analyze(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analyse anzeigen? Das kann eine Weile dauern", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.button = Button(self, text='Matplotlib', command=self.plot_analysis)
        self.button.pack({"anchor": 's'})

        self.button2 = Button(self, text='Unity', command=self.plot_analysis2)
        self.button2.pack({"anchor": 's'})

        button1 = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button1.pack({"anchor": 's'})

    def plot_analysis(self):
        figure = Main('nonblocking.wav',self.controller.text)
        plot = Plotting(figure.main())
        plot.plot_this_fig()

    # Unity interface

    def plot_analysis2(self):
        # OSC-Stuff:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1")
        parser.add_argument("--port", type=int, default=5005)
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port);

        # analyse result:
        figure = Main('nonblocking.wav',self.controller.text)
        result = figure.main()

        # dump files:
        copyfile('nonblocking.wav', 'render/nonblocking.wav')

        # SILBEN IN ZEILEN
        file_db = open('render/text.txt', 'w')
        print(result.text, file=file_db)
        file_db.close()

        file_db = open('render/db.csv', 'w')
        for v in result.db:
            print(v, file=file_db)
        file_db.close()

        file_db = open('render/duration.csv', 'w')
        print(result.duration, file=file_db)
        file_db.close()

        file_db = open('render/pitch.csv', 'w')
        for v in result.pitch:
            print(v, file=file_db)
        file_db.close()

        # wait just long enough - but not too long! - and then send OSC message:
        time.sleep(3)   # you shall wait for 3 seconds! not 2! and not 4!
        client.send_message("/start", "start")

if __name__ =='__main__':
    app = GUI()
    app.mainloop()
