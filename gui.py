#
# OpenSpeech Project
# Ninell Oldenburg
# Univesity of Potsdam & University of Dramatic Art »Ernst Busch«, Berlin
# Licensed under GNU General Public License
# Python 3.6
#

import tkinter as tk
from tkinter import Button
from tkinter import font
import recorder as reco
from analysis import Main
import time
from plot import Plotting
import utt

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("1000x400")
        self.QUIT = Button(self, text="Exit", command=self.quit)
        self.QUIT.pack({"side": "top"})

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Analyze, Record, Instruct):
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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to OpenSpeech!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        welcome = utt.data['welcome']['welcome_text']
        text = tk.Text(self, height=4, width=50)
        text.insert(tk.END, welcome)
        text.pack()

        self.button = Button(self, text='Aufnahme', command=lambda: controller.show_frame("Record"))
        self.button.pack({"anchor": "s"})

        self.button = Button(self, text='Wie geht das?', command=lambda: controller.show_frame("Instruct"))
        self.button.pack({"anchor": 's'})

class Record(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcher Satz soll aufgenommen werden?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        text = tk.Text(self, height=20, width=80)

        for index, sentence in utt.data['examples'].items():
            text.insert(tk.END, str(index) + ' ')
            text.insert(tk.END, sentence + '\n \n')
            print('reached')

        text.pack()

        self.button = Button(self, text='Aufnehmen', command=self.record)
        self.button.pack({"anchor": 's'})

        button1 = tk.Button(self, text="Analyse", command=lambda: controller.show_frame("Analyze"))
        button1.pack({"anchor": 's'})

    def record(self):
        rec = reco.Recorder(channels=2)
        print('entered record')
        with rec.open('nonblocking.wav', 'wb') as file:
            file.start_recording()
            time.sleep(5.0)
            file.stop_recording()

class Instruct(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Wie geht das?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        instruct = utt.data['welcome']['instructions']
        text = tk.Text(self, height=4, width=50)
        text.insert(tk.END, instruct)
        text.pack()

        button1 = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button1.pack({"anchor": 's'})

class Analyze(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analyse anzeigen? Das kann eine Weile dauern", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.button = Button(self, text='Anzeigen', command=self.plot_analysis)
        self.button.pack({"anchor": 's'})

        button1 = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button1.pack({"anchor": 's'})

    def plot_analysis(self):
        figure = Main('nonblocking.wav')
        plot = Plotting(figure.main(), 1)
        plot.plot_this_fig()

if __name__ =='__main__':
    app = GUI()
    app.mainloop()