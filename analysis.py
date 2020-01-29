#
# OpenSpeech Project
# Ninell Oldenburg
# Univesity of Potsdam & University of Dramatic Art »Ernst Busch«, Berlin
# Licensed under GNU General Public License
# Python 3.6
#

import numpy as np
import matplotlib.pyplot as plt
import parselmouth as psl
import wave
import contextlib
import collections
import glob
import warnings
import utt

# Main class for the analysis of the soundfile
class Main:

    # takes filename and text as input
    # and uses praat-interface to get the right data out of it
    def __init__(self,filename,text):
        self.name = filename
        self.textname = text
        self.snd = psl.Sound(filename)
        self.pitch = self.snd.to_pitch(pitch_floor=75.0, pitch_ceiling=600.0)
        self.voiced_frames = self.pitch.count_voiced_frames()
        self.intensity = self.snd.to_intensity()
        self.formant = self.snd.to_formant_burg(max_number_of_formants=5, maximum_formant=5500)

    # post processing function to properly get the pitch in a resonable array
    def get_pitch(self):

        pitch_values = self.pitch.selected_array['frequency']
        pitch_values[pitch_values == 0] = np.nan

        return pitch_values

    # post processing function to properly get the db scale in a resonable array
    def get_db(self):

        list = []

        for lists in self.intensity.values:
            for value in lists:
                list.append(value)
                """
                if len(fra_ener_dis) < value:
                    print(len(fra_ener_dis))
                    for i in range(len(fra_ener_dis),int(value)+1):
                        fra_ener_dis.append([])
                fra_ener_dis[int(value)].append(1)
                """

        db = np.array(list)

        return db

    # post processing function to properly get the formants 1 and 2
    # in a resonable array of two arrays
    def get_formants(self):

        frame_number_fo = self.formant.get_number_of_frames()

        formant_values_f1 = np.zeros(frame_number_fo)
        formant_values_f2 = np.zeros(frame_number_fo)

        for i in range(1, frame_number_fo):
            t = self.formant.get_time_from_frame_number(i)
            formant_values_f1[i] = self.formant.get_value_at_time(1, t)
            formant_values_f2[i] = self.formant.get_value_at_time(2, t)

        return formant_values_f1, formant_values_f2

    # compute the overall duration of the sound
    def get_duration(self):

        with contextlib.closing(wave.open(self.name,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    # just make a normal plot (to check whether everything was processed correctly)
    def make_plot(self,a,b,c):
        pitch = a
        db = b
        text = c

        x1 = np.linspace(0, len(pitch), len(pitch))
        x2 = np.linspace(0, len(db), len(db))
        x3 = np.linspace(0, len(text), len(text))

        y1 = pitch
        y2 = db
        y3 = text

        plt.subplot(4, 1, 1)
        plt.plot(x1, y1)
        plt.title('A tale of 2 subplots')
        plt.ylabel('Pitch')

        plt.subplot(4, 1, 2)
        plt.plot(x2, y2)
        plt.xlabel('Number of Frames')
        plt.ylabel('Decibel')

        plt.subplot(4, 1, 3)
        plt.plot(x3, y3)
        plt.xlabel('Number of Frames')
        plt.ylabel('Text')

        plt.subplot(4, 1, 4)
        bins = np.linspace(0,100,100)
        plt.hist(b,bins)
        plt.xlabel('dB scale')
        plt.ylabel('Number of Frmaes')

        #plt.xticks([])
        #plt.yticks([])

        plt.show()

    # trim everything on one length: pitch, db, text
    # length: 25 fps
    def post_process(self,a,b,t):
        anim_len = int(round(self.get_duration()*25)) # exact length for animation
        array_a = np.zeros(anim_len)
        array_b = np.zeros(anim_len)
        textlist = np.empty(anim_len, dtype=object)

        diff_a = int(len(a)/anim_len)
        diff_b = int(len(b)/anim_len)
        long = 1
        short = 1
        if anim_len > len(t):
            long = anim_len
            short = len(t)
        else:
            long = len(t)
            short = anim_len
        diff_t = int(long/short)
        c = 0
        d = 0
        e = 0

        for i in range(0,len(b)):

            if (i % diff_a == 0 and (i/diff_a)<anim_len):
                lst = []
                for j in range(i-diff_a,i):
                    lst.append(a[j])
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    lst = np.array(lst)
                    array_a[c] = lst[~np.isnan(lst)].mean()
                c+=1

            if (i % diff_b == 0 and (i/diff_b)<anim_len):
                list = []
                for j in range(i-diff_b,i):
                    list.append(b[j])
                list = np.array(list)
                array_b[d] = list[~np.isnan(list)].mean()
                d+=1

            if (i % diff_t == 0 and e<len(t) and i<anim_len):
                textlist[i] = t[e]
                e+=1

            if i<anim_len and textlist[i] == None:
                textlist[i] = ''

        return array_a, array_b, textlist

    def main(self):
        # Output: np.arrays (dtype=float) with #1 pitch; #2 db values; #3 formant f1 and f2, duration as float
        # as well as np array #4 quality (which is db for now as well) and #5 string array of text

        text = utt.data['examples'][self.textname][1].split(' ')

        pitch = self.get_pitch()
        db = self.get_db()

        # the line below can be used to cut down the fps to 25
        # (works without as well but has a very high computation time)
        # pitch, db, text = self.post_process(self.get_pitch(),self.get_db(),text)

        # self.make_plot(pitch,db,text)

        Point = collections.namedtuple('Point', ['pitch', 'db', 'f1_2', 'duration', 'quality', 'text'])
        result = Point(pitch, db, self.get_formants(), self.get_duration(), db, text)

        return result


if __name__ == '__main__' :
    #for wave_file in sorted(glob.glob("audio/*.wav")):
        #print("Processing {}...".format(wave_file))
        #this_func = Main(wave_file)
        #this_func.make_plot()
        #print(this_func.main())

    this_func = Main('audio/busch/ballade1.wav','Ballade an der Reichstag 1')
    this_func.main()
