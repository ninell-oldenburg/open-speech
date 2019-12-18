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

class Main:

    def __init__(self,filename):
        self.snd = psl.Sound(filename)
        self.pitch = self.snd.to_pitch(pitch_floor=75.0, pitch_ceiling=600.0)
        self.voiced_frames = self.pitch.count_voiced_frames()
        self.intensity = self.snd.to_intensity()
        self.formant = self.snd.to_formant_burg(max_number_of_formants=5, maximum_formant=5500)

    def display_pitch(self):

        pitch_values = self.pitch.selected_array['frequency']
        pitch_values[pitch_values == 0] = np.nan

        for t in range(0, len(pitch_values)) :
            print(str(t) + ': ' + str(pitch_values[t]))

        plt.plot(self.pitch.xs(), pitch_values, 'o', markersize=5)
        plt.plot(self.pitch.xs(), pitch_values, 'o', markersize=2)

        #plt.show()

    def display_db(self):

        intensity_values = self.intensity.values.T

        for t in range(0, len(intensity_values)):
            print(intensity_values[t])

    def display_formants(self):

        frame_number_fo = self.formant.get_number_of_frames()

        formant_values_f1 = np.zeros(frame_number_fo)
        formant_values_f2 = np.zeros(frame_number_fo)

        for i in range(1, frame_number_fo):
            t = self.formant.get_time_from_frame_number(i)
            formant_values_f1[i] = self.formant.get_value_at_time(1, t)
            formant_values_f2[i] = self.formant.get_value_at_time(2, t)

            print('F1: ' + str(formant_values_f1[i]))
            print('F2: ' + str(formant_values_f2[i]))


    def main(self):
        self.display_pitch()
        self.display_db()
        self.display_formants()


if __name__ == '__main__' :
    this_func = Main('audio/08.wav')
    print(this_func.main())


