#
# OpenSpeech Project
# Ninell Oldenburg
# Univesity of Potsdam & University of Dramatic Art »Ernst Busch«, Berlin
# Licensed under GNU General Public License
# Python 3.6
#

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import parselmouth as psl
import wave
import contextlib
import collections
import glob
import math

class Main:

    # takes filename to analyse as argument
    def __init__(self,filename):
        self.name = filename
        self.snd = psl.Sound(filename)
        self.pitch = self.snd.to_pitch(pitch_floor=75.0, pitch_ceiling=600.0)
        self.voiced_frames = self.pitch.count_voiced_frames()
        self.intensity = self.snd.to_intensity()
        self.formant = self.snd.to_formant_burg(max_number_of_formants=5, maximum_formant=5500)

    def get_pitch(self):

        pitch_values = self.pitch.selected_array['frequency']
        pitch_values[pitch_values == 0] = np.nan

        return pitch_values

    def get_db(self):

        list = []

        for lists in self.intensity.values:
            for value in lists:
                list.append(value)

        db = np.array(list)

        return db

    def get_formants(self):

        frame_number_fo = self.formant.get_number_of_frames()

        formant_values_f1 = np.zeros(frame_number_fo)
        formant_values_f2 = np.zeros(frame_number_fo)

        for i in range(1, frame_number_fo):
            t = self.formant.get_time_from_frame_number(i)
            formant_values_f1[i] = self.formant.get_value_at_time(1, t)
            formant_values_f2[i] = self.formant.get_value_at_time(2, t)

        return formant_values_f1, formant_values_f2

    def get_duration(self):

        with contextlib.closing(wave.open(self.name,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    def make_plot(self,a,b):
        pitch = a
        db = b

        x1 = np.linspace(0, len(pitch), len(pitch))
        x2 = np.linspace(0, len(db), len(db))

        y1 = pitch
        y2 = db

        plt.subplot(2, 1, 1)
        plt.plot(x1, y1)
        plt.title('A tale of 2 subplots')
        plt.ylabel('Pitch')

        plt.subplot(2, 1, 2)
        plt.plot(x2, y2)
        plt.xlabel('Number of Frames')
        plt.ylabel('Decibel')

        plt.show()


    def post_process(self,a,b):
        c = 0
        new_array = np.zeros(len(b))
        dis = int(len(b)/(len(b)-len(a)))
        for i in range(0,len(a)):
            if (i % dis == 0):
                new_array[i] = np.mean([a[i],a[i-1]])
                c+=1
            else:
                new_array[i+c] = a[i]
        return new_array



    def main(self):
        # Output: 4 np.arrays with #1 pitch; #2 db values; #3 formant f1; #4 formant f2

        pitch = self.get_pitch()
        db = self.get_db()

        if len(db) > len(pitch):
            pitch = self.post_process(pitch,db)
        elif len(db) < len(pitch):
            db = self.post_process(db,pitch)

        # self.make_plot(pitch,db)

        Point = collections.namedtuple('Point', ['pitch', 'db', 'f1_2', 'duration'])
        result = Point(pitch, db, self.get_formants(), self.get_duration())

        return result


if __name__ == '__main__' :
    #for wave_file in sorted(glob.glob("audio/*.wav")):
        #print("Processing {}...".format(wave_file))
        #this_func = Main(wave_file)
        #this_func.make_plot()
        #print(this_func.main())

    this_func = Main('audio/08.wav')
    this_func.main()
