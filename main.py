#
# OpenSpeech Project
# Ninell Oldenburg
# Univesity of Potsdam & University of Dramatic Art »Ernst Busch«, Berlin
# Licensed under GNU General Public License
# Python 3.6
#

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import parselmouth as psl

class Main:

    def __init__(self,filename):
        self.snd = psl.Sound(filename)
        self.pitch = self.snd.to_pitch()
        self.intensity = self.snd.to_intensity()

    def display_pitch(self):

        pitch_values = self.pitch.selected_array['frequency']
        pitch_values[pitch_values == 0] = np.nan

        for t in range(0, len(pitch_values)) :
            print(str(t) + ': ' + str(pitch_values[t]))

        plt.plot(self.pitch.xs(), pitch_values, 'o', markersize=5)
        plt.plot(self.pitch.xs(), pitch_values, 'o', markersize=2)

        plt.show()

    def display_db(self):

        intensity_values = self.intensity.values.T

        for t in range(0, len(intensity_values)):
            print(intensity_values[t])


    def main(self):
        #self.display_pitch()
        self.display_db()


if __name__ == '__main__' :
    this_func = Main('audio/08.wav')
    print(this_func.main())
