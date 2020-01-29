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

# basic class for frame model
class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        # initialze the frame with some buttons as well as a welcome text
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.body_font = font.Font(family='Helvetica', size=13)
        self.geometry("1000x400")
        self.QUIT = Button(self, text="Exit", command=self.quit)
        self.QUIT.pack({"side": "top"})
        self.text = list(utt.data['examples'].keys())[0]
        self.self_record = True

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # all frames are going to be rendered b e f o r e the actual frame is called
        self.frames = {}
        for F in (StartPage, Text, Analyze, Instruct, Originals):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def set_text(self, text):
        # setter for which text is used
        self.text = text


# welcome page class
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

        self.button = Button(self, text='Originale anhören', command=lambda: controller.show_frame("Originals"))
        self.button.pack({"anchor": "s"})

        self.button = Button(self, text='Wie geht das?', command=lambda: controller.show_frame("Instruct"))
        self.button.pack({"anchor": 's'})


# this is the class where you choose the input text
# and record the text
class Text(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcher Satz soll aufgenommen werden?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.running = None

        # options for the dropdown menu
        OPTIONS = list(utt.data['examples'].keys())
        variable = StringVar(self)
        variable.set(OPTIONS[0])

        # dropdown menu f
        w = OptionMenu(self, variable, *OPTIONS)
        w.pack()

        # show text button
        # would be nice to show the right away without having to click on 'show text' (TODO)
        button = Button(self, text="Text anzeigen", command=lambda: self.show_text(variable.get()))
        button.pack()

        # the final text corresponding to the user chosen title
        default = OPTIONS[0]
        self.var = utt.data['examples'][default][0]
        self.l = tk.Label(self, text=self.var, font=controller.body_font)
        self.l.pack({"anchor": 's'})

        # start record button
        self.button_rec = Button(self, text='Start Aufnahme', command=self.start)
        self.button_rec.pack({"anchor": 's'})

        # stop record button
        self.button_stop = Button(self, text='Stop Aufnahme', command=self.stop)
        self.button_stop.pack({"anchor": 's'})

        # analysis button
        button_ana = tk.Button(self, text="Analysieren", command=lambda: controller.show_frame("Analyze"))
        button_ana.pack({"anchor": 's'})

        # back button
        button_back = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button_back.pack({"anchor": 's'})

        # the recorder class comes from recorder.py (by Steven Loria)
        # every input device with it's id is printed to the console
        self.rec = reco.Recorder(channels=2, input_device_index=0)

    # when showing the text to the user at the same time change it from the controller
    # I used a global bool self_record for that
    def show_text(self,name):
        self.controller.set_text(name)
        text = utt.data['examples'][name][0]
        self.l.configure(text=text)
        if self.controller.self_record == False:
            self.controller.self_record = True

    # the functions stops recording if there is a stream running
    def stop(self):
        self.running
        if self.running is not None:
            self.running.stop_recording()
            self.running.close()
            self.running = None
        else:
            print('not runnning')

    # the function starts recording if there is no function running
    def start(self):
        self.running
        if self.running is not None:
            print('already running')
        else:
            self.running = self.rec.open('nonblocking.wav','wb')
            self.running.start_recording()

# if you want to record a text by yourself
# you can listen to the originals (pre-recorded voices)
class Originals(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcher Satz soll gespielt werden?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.running = None

        # options for the dropdown menu
        OPTIONS = list(utt.data['examples'].keys())
        variable = StringVar(self)
        variable.set(OPTIONS[0])

        # still using a dropdown menu
        w = OptionMenu(self, variable, *OPTIONS)
        w.pack()

        # show text button
        # would be nice to show the right away without having to click on 'show text' (TODO)
        button = Button(self, text="Text anzeigen", command=lambda: self.show_text(variable.get()))
        button.pack()

        # the final text corresponding to the user chosen title
        default = OPTIONS[0]
        self.var = utt.data['examples'][default][0]
        self.l = tk.Label(self, text=self.var, font=controller.body_font)
        self.l.pack({"anchor": 's'})

        # analysis button
        button_ana = tk.Button(self, text="Analysieren", command=lambda: controller.show_frame("Analyze"))
        button_ana.pack({"anchor": 's'})

    # when showing the text to the user at the same time change it from the controller
    # I used a global bool self_record for that
    def show_text(self,name):
        self.controller.set_text(name)
        text = utt.data['examples'][name][0]
        self.l.configure(text=text)
        if self.controller.self_record == True:
            self.controller.self_record = False


# a class for instrutions
class Instruct(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Wie geht das?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # put pre-defined text in it and show it
        instruct = utt.data['welcome']['instructions']
        text = tk.Label(self, text=instruct, font=controller.body_font)
        text.pack()

        # back button
        button_back = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button_back.pack({"anchor": 's'})


# class for running the analysis
# the analysis can be made in two ways
# either with the matplotlib resulting in an animated graph
# or the unity-way resulting in different csv tables that you can use via unity
class Analyze(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analyse anzeigen? Das kann eine Weile dauern", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # matplotlib button
        self.button_mat = Button(self, text='Matplotlib', command=self.matplot_plot)
        self.button_mat.pack({"anchor": 's'})

        # unity button
        self.button_uni = Button(self, text='Unity', command=self.plot_analysis2)
        self.button_uni.pack({"anchor": 's'})

        # back button
        button_back = tk.Button(self, text="Zurück", command=lambda: controller.show_frame("StartPage"))
        button_back.pack({"anchor": 's'})

    # matplotlib function
    def matplot_plot(self):
        # name is defined depending on whether the self-record mode was used
        # or if the originals should be used (still the path is hard-coded (TODO))
        name = ''
        if self.controller.self_record == True:
            name += 'nonblocking.wav'
        else:
            name += 'audio/busch/' + utt.data['names'][self.controller.text] + '.wav'
        figure = Main(name,self.controller.text)
        plot = Plotting(figure.main())
        plot.plot_this_fig()

    # unity interface
    def plot_analysis2(self):
        # OSC-Stuff:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1")
        parser.add_argument("--port", type=int, default=5005)
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port);

        # analyse result:
        name = ''
        if self.controller.self_record == True:
            name += 'nonblocking.wav'
        else:
            name += 'audio/busch/' + utt.data['names'][self.controller.text] + '.wav'
        figure = Main(name, self.controller.text)
        result = figure.main()

        # dump files:
        if self.controller.self_record == True:
            copyfile('nonblocking.wav', 'render/nonblocking.wav')
        else:
            copyfile(name, 'render/nonblocking.wav')
            
        # split into syllables
        text = ''
        for x in self.controller.text:
            text += x + '\n'
        file_db = open('render/text.txt', 'w')
        print(text, file=file_db)
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
        time.sleep(3) # you shall wait for 3 seconds! not 2! and not 4!
        client.send_message("/start", "start")

if __name__ =='__main__':
    app = GUI()
    app.mainloop()
