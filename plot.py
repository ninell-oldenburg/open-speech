#
# OpenSpeech Project
# Ninell Oldenburg
# Univesity of Potsdam & University of Dramatic Art »Ernst Busch«, Berlin
# Licensed under GNU General Public License
# Python 3.6
#

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from analysis import Main
import utt
import play
import threading


class Plotting(object):

    def __init__(self, sound):
        self.pitch = sound.pitch
        self.dura = sound.duration
        self.quality = sound.quality
        self.text = sound.text

        for value in self.pitch:
            np.nan_to_num(value)

        self.db = sound.db
        self.f1_2 = sound.f1_2

        self.pitch_min = np.nanmin(self.pitch[np.nonzero(self.pitch)])
        self.pitch_max = np.nanmax(self.pitch)

        # set up the figure, the axis, and the subplot elements
        self.fig = plt.figure()
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 2, 3)
        ax3 = self.fig.add_subplot(2, 2, 4)

        ax1.set_xlim(0,self.dura)
        ax1.set_ylim(self.pitch_min - 50, self.pitch_max + 50)
        ax1.set_ylabel('Tonhöhe (Hz)')
        ax1.set_facecolor('xkcd:navy')
        ax1.axes.get_xaxis().set_visible(False)

        self.label = ax1.text(self.dura/2, self.pitch_max, self.text[0], ha='center', color='xkcd:white', va='center', fontsize=12)
        self.scatter = ax1.scatter([], [], s=30, c='xkcd:white', linewidths=1, marker='.')

        ax2.set_xlim(0, 2)
        ax2.set_ylim(0, np.nanmax(self.db))
        ax2.set_ylabel('Dezibel')
        ax2.set_facecolor('xkcd:navy')
        ax2.axes.get_xaxis().set_visible(False)

        x = range(1,2)
        y = [1, 2, 3]
        self.bar = ax2.bar(x, y, color='xkcd:white')

        ax3.set_xlim(0, 1)
        ax3.set_ylim(0, 1)
        ax3.set_facecolor('xkcd:navy')
        ax3.axes.get_yaxis().set_visible(False)
        ax3.axes.get_xaxis().set_visible(False)

        # example of circle implementation from:
        # https://brushingupscience.com/2016/06/21/matplotlib-animations-the-easy-way/

        u = np.linspace(1, 0, 91)
        v = np.linspace(1, 0, 91)
        w = self.quality
        X3, Y3, T3 = np.meshgrid(u, v, w)
        sinT3 = np.sin(0.5 * np.pi * T3 / T3.max(axis=2)[..., np.newaxis])
        self.G = (X3 ** 2 + Y3 ** 2) * sinT3
        self.cax = ax3.pcolormesh(u, v, self.G[:-1, :-1, 0], vmin=0, vmax=1, cmap='Blues')
        self.fig.colorbar(self.cax)

    # initialization function: plot the background of each frame
    def init(self):
        self.scatter.set_offsets([])
        self.bar[0].set_height(0)
        self.label.set_text([])

        return self.scatter,

    # animation function.  This is called sequentially
    def animate(self, i):

        y = self.pitch
        x = np.linspace(0, self.dura, len(y))
        data = np.hstack((x[:i, np.newaxis], y[:i, np.newaxis]))
        self.scatter.set_offsets(data)

        self.label.set_text(self.text[i])

        y_bar = self.db[:i]
        for j, b in enumerate(self.bar):
            if len(y_bar) > j:
                b.set_height(y_bar[j])

        self.cax.set_array(self.G[:-1, :-1, i].flatten())

        return self.scatter,

    def plot_this_fig(self):
        # call the animator.  blit=True means only re-draw the parts that have changed.

        interval = (self.dura * 1000)/len(self.pitch)

        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                       frames=len(self.pitch), interval=interval, blit=False)

        # save the animation as an mp4.  This requires ffmpeg or mencoder to be
        # installed.  The extra_args ensure that the x264 codec is used, so that
        # the video can be embedded in html5.  You may need to adjust this for
        # your system: for more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
        anim.save('animation.mp4', fps=25, extra_args=['-vcodec', 'libx264'])

        # play.Play('audio/busch/ballade1.wav')
        plt.show()

        """
        x = threading.Thread(target=play.Play, args=(,))
        y = threading.Thread(target=plt.show, args=())
        x.start()
        y.start()
        """

if __name__ == '__main__':
    ana = Main('audio/busch/ballade1.wav', 'Ballade an der Reichstag 1')
    test = Plotting(ana.main())
    test.plot_this_fig()
    #play.Play('audio/busch/ballade1.wav')
