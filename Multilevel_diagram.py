import matplotlib.pyplot as plt
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict
import numpy
import inspect
plt.rcParams.update({"text.usetex": True})

grid = numpy.zeros((8, 8))
grid[:, 0] = numpy.ones(8)
grid[:, 4] = numpy.ones(8)
grid = 1 - grid

plt.imshow(grid, cmap='Set3')

ax = plt.gca()
ax.grid(color='w', linestyle='-', linewidth=2)
ax.set_xticks(numpy.arange(-.5, 8, 1))
ax.set_yticks(numpy.arange(-.5, 8, 1))

for xlabel_i in ax.axes.get_xticklabels():
    xlabel_i.set_visible(False)
    xlabel_i.set_fontsize(0.0)
for xlabel_i in ax.axes.get_yticklabels():
    xlabel_i.set_fontsize(0.0)
    xlabel_i.set_visible(False)
for tick in ax.axes.get_xticklines():
    tick.set_visible(False)
for tick in ax.axes.get_yticklines():
    tick.set_visible(False)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

x = plt.Rectangle((1.5, 4.5), 1, 1, color='slateblue', lw=4, zorder=100, fill=None)
y = plt.Rectangle((5.5, 1.5), 1, 1, color='slateblue', lw=4, zorder=100, fill=None)
plt.arrow(2.5, 5, 2.6, -2.7, lw=4, color='indigo', head_width=0.3, zorder=100)
plt.text(4.6, 3.5, r'$ \delta = y - x $', color='indigo', fontsize=23)
plt.text(1.4, 6.2, r'$ \phi (x) $', color='slateblue', fontsize=23)
plt.text(5.4, 1.2, r'$ \phi (y) $', color='slateblue', fontsize=23)

B1 = plt.Rectangle((-0.45, -0.45), 0.9, 7.9, color='maroon', lw=4, zorder=80, fill=None)
B2 = plt.Rectangle((3.55, -0.45), 0.9, 7.9, color='maroon', lw=4, zorder=80, fill=None)
plt.text(1.6, -0.7, r'$ \partial B $', color='maroon', fontsize=23)

plt.text(1.75, 2.2, r'$ \Lambda_1 $', color='orangered', fontsize=23)
plt.arrow(2.4, 2, 0.7, 0, color='orangered', zorder=100, head_width=0.3)
plt.arrow(1.6, 2, -0.7, 0, color='orangered', zorder=100, head_width=0.3)
plt.text(5.6, 5.6, r'$ \Lambda_2 $', color='orangered', fontsize=23)
plt.arrow(6.4, 5.4, 0.7, 0, color='orangered', zorder=100, head_width=0.3)
plt.arrow(5.6, 5.4, -0.7, 0, color='orangered', zorder=100, head_width=0.3)


ax.add_patch(x)
ax.add_patch(y)
ax.add_patch(B1)
ax.add_patch(B2)

fig = plt.gcf()
fig.set_size_inches(6, 6)

plt.show()
