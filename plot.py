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


class Plotting(object):

    def __init__(self, sound, i):
        self.pitch = sound.pitch
        self.dura = sound.duration
        index = str(i)

        for value in self.pitch:
            np.nan_to_num(value)

        self.db = sound.db
        self.f1_2 = sound.f1_2

        self.pitch_min = np.nanmin(self.pitch[np.nonzero(self.pitch)])
        self.pitch_max = np.nanmax(self.pitch)

        # First set up the figure, the axis, and the plot element we want to animate
        self.fig = plt.figure()
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 2, 3)
        ax3 = self.fig.add_subplot(2, 2, 4)

        ax1.set_xlim(0,self.dura)
        ax1.set_ylim(0,600)
        ax1.set_facecolor('xkcd:navy')

        self.string = utt.data['examples'][index]
        self.label = ax1.text(5, 500, self.string[0], ha='center', color='xkcd:white', va='center', fontsize=12)

        self.scatter = ax1.scatter([], [], s=30, c='xkcd:white', linewidths=1, marker='.')

        ax2.set_xlim(0, 2)
        ax2.set_ylim(0, 80)
        ax2.set_facecolor('xkcd:navy')

        x = range(1,2)
        y = [1, 2, 3]
        self.bar = ax2.bar(x, y, color='xkcd:white')

        ax3.set_xlim(0, 1)
        ax3.set_ylim(0, 1)
        ax3.set_facecolor('xkcd:navy')

        # implementiert
        # muss nun noch an F1 und F2 angepasst werden

        u = np.linspace(0, 1, 91)
        v = np.linspace(0, 1, 91)
        w = np.linspace(0, 25, len(self.pitch))
        X3, Y3, T3 = np.meshgrid(u, v, w)
        sinT3 = np.sin(2 * np.pi * T3 / T3.max(axis=2)[..., np.newaxis])
        self.G = (X3 ** 2 + Y3 ** 2)
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

        self.label.set_text(self.string[:i + 1])

        y_bar = self.db[i:]

        for j, b in enumerate(self.bar):
            if len(y_bar) > j:
                b.set_height(y_bar[j])

        self.cax.set_array(self.G[:-1, :-1, i].flatten())

        return self.scatter,

    def plot_this_fig(self):
        # call the animator.  blit=True means only re-draw the parts that have changed.

        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                       frames=len(self.pitch), interval=10, blit=False)

        # save the animation as an mp4.  This requires ffmpeg or mencoder to be
        # installed.  The extra_args ensure that the x264 codec is used, so that
        # the video can be embedded in html5.  You may need to adjust this for
        # your system: for more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
        anim.save('animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

        plt.show()


if __name__ == '__main__':
    ana = Main('audio/08.wav')
    test = Plotting(ana.main(), 1)
    test.plot_this_fig()