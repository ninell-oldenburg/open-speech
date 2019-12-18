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
import time

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
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
        for F in (StartPage, Analyze):
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

        self.button = Button(self, text='Record', command=self.record)
        self.button.pack({"side": "left"})

        button1 = tk.Button(self, text="Analyze", command=lambda: controller.show_frame("Analyze")) # Analyse button
        button2 = tk.Button(self, text="Again", command=lambda: controller.show_frame("PageTwo"))

        button2.pack({"side": "right"})
        button1.pack({"side": "right"})

    def record(self):
        rec = reco.Recorder(channels=2)
        print('entered record')
        with rec.open('nonblocking.wav', 'wb') as file:
            file.start_recording()
            time.sleep(5.0)
            file.stop_recording()

class Analyze(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Again",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ =='__main__':
    app = GUI()
    app.mainloop()