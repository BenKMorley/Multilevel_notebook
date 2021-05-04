from collections import Counter
import pdb                          # For debugging
import os                           # For filesystem management
from multiprocessing import Pool    # For parallel execution
from IPython.display import HTML

import numpy

from scipy.stats import truncnorm, norm, binom, ks_2samp, ttest_ind
from scipy import optimize
from scipy.optimize import least_squares, minimize, minimize_scalar
from scipy.special import factorial2

import matplotlib
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import colors, animation, rc
from matplotlib.animation import FuncAnimation

from tqdm import tqdm               # Gives loading bar while running


def animate(lattice_data, no_iterations, dt, save_fig=False, filename=None,
            show_fig=True, plotting_dimensions=2):
  """
    INPUTS :
    --------
    lattice_data : (N, L, L) or (N, M, L, L) numpy array of {-1, 1}, single level or multilevel spin data.
    no_iterations :  int, number of frames
    save_fig=False : Bool, if set to True then the animation will be saved in the
                     directory the script is being run in.
    filename=None : None or string, a string that the file is saved under
    show_fig=True : Bool, if True then the animation will display
    dt : float, change in time between frames

    RETURNS :
    ---------
    ani : Instance of matplotlib.animation.FuncAnimation class
  """
  L = lattice_data.shape[2]  # True for multilevel and single level

  #  If the data is multilevel, we want to change the array shape to (N * M, L, L) first
  if len(lattice_data.shape) == 4:
    lattice_data = lattice_data.reshape((lattice_data.shape[0] * lattice_data.shape[1], L, L))

  # Number of configs
  no_configs = lattice_data.shape[0]
  assert no_configs >= no_iterations, "Not enough configs to produce that many iterations"

  # Create figure and axis
  fig = plt.figure()
  ax = plt.gca()

  # Setting the axes properties
  ax.set_xlim([-0.5, L - 0.5])
  ax.set_ylim([-0.5, L - 0.5])

  #  In order to highlight the bounary sites
  lattice_data = lattice_data.astype(float)
  lattice_data[:, 0, :] = 0.5 * lattice_data[:, 0, :]
  lattice_data[:, L // 2, :] = 0.5 * lattice_data[:, L // 2, :]
  lattice_data[:, :, 0] = 0.5 * lattice_data[:, :, 0]
  lattice_data[:, :, L // 2] = 0.5 * lattice_data[:, :, L // 2]

  plot_me = ax.imshow(lattice_data[0])

  def update(num):
      data = lattice_data[num]
      plot_me.set_data(data)
      return plot_me,

  # Creating the Animation object
  ani = FuncAnimation(fig, update, frames=range(no_iterations),
                      interval=int(dt * 1000), blit=True, repeat=False)

  return ani


def animate_twopt(ising_slice, no_iterations, dt, delta, plotting_dimensions=2, multilevel=False):
  """
    Function designed to show the twopt function working on slice coordinates

    INPUTS :
    --------
    slice : Object of type single_slice_ising or multi_slice_ising
    no_iterations: int, number of configurations used
    dt : float, change in time between frames
    delta: int, twopt-function seperation
    multilevel: bool, if true the algorithm uses multilevel spin data.
  """
  lattice_data = ising_slice.spins.astype(float)
  slice_data = ising_slice.spin_slice.astype(float)
  L = lattice_data.shape[2]  # True for multilevel and single level

  # If the data is multilevel, then change the shape
  if len(lattice_data.shape) == 4:
    twopt = ising_slice.twopt_raw(delta)
    twopt = twopt.reshape((lattice_data.shape[0] * lattice_data.shape[1], L))
    slice_data = slice_data.reshape((lattice_data.shape[0] * lattice_data.shape[1], L))
    lattice_data = lattice_data.reshape((lattice_data.shape[0] * lattice_data.shape[1], L, L))

  else:
      twopt = ising_slice.twopt(delta)

  assert lattice_data.shape[0] >= no_iterations, "Not enough configs to produce that many iterations"

  # Create figure and axis
  fig, axes = plt.subplots(4, 1, gridspec_kw={'height_ratios': [5, 1, 1, 1]})

  # For the purpose of highlighting the boundary layer (with splitting = 2). Show the spin data
  lattice_data[0, :, 0] = 0.5 * lattice_data[0, :, 0]
  lattice_data[0, :, L // 2] = 0.5 * lattice_data[0, :, L // 2]

  # Show the spins before being turned into slice coordinates
  ax0 = axes[0].imshow(numpy.transpose(lattice_data[0]))

  # Show the slice data
  x1 = slice_data[0]
  ax1 = axes[1].bar(numpy.arange(len(x1)), x1)

  # Show the slice data at the second point in two-point function
  x2 = numpy.roll(slice_data[0], -delta)
  ax2 = axes[2].bar(numpy.arange(len(x1)), x2)

  # Show the product of the two points in the correlator
  ax3 = axes[3].bar(numpy.arange(len(x1)), twopt[0])

  # Plot appearance
  axes[0].set_xlim([-0.5, L - 0.5])
  axes[0].set_ylim([-0.5, L - 0.5])
  axes[1].set_aspect(0.85)
  axes[2].set_aspect(0.85)
  axes[3].set_aspect(0.85)

  for i in range(4):
    axes[i].set_xticklabels(["", ] * L)
    axes[i].set_xticks([])

  for i in range(1, 4):
    axes[i].set_ylim((-1, 1))

  axes[0].set_title("Spins")
  axes[1].set_title("Spin slice")
  axes[2].set_title("Spin slice, shifted by delta")
  axes[3].set_title("twopt function")

  fig.tight_layout(pad=1)
  axes = [ax0, ax1, ax2, ax3]

  def update(num):
    data0 = numpy.transpose(lattice_data[num])
    data1 = slice_data[num]
    data2 = numpy.roll(slice_data[num], -delta)
    data3 = twopt[num]
    data = [data0, data1, data2, data3]
    axs = [ax0, ax1, ax2, ax3]

    # Set new data into the image
    for i in range(1, 4):
      for bar, h in zip(axs[i], data[i]):
        bar.set_height(h)

    # Finaaly update the spins
    data0[:, 0] = 0.5 * data0[:, 0]
    data0[:, L // 2] = 0.5 * data0[:, L // 2]
    ax0.set_data(data0)

    return axes

  # Creating the Animation object
  ani = FuncAnimation(fig, update, frames=range(1, no_iterations),
                      interval=int(dt * 1000), blit=False, repeat=False)

  return ani


## NOT WORKING
def animate_slice_data(slice_data, N, M, L, no_iterations, dt, save_fig=False, filename=None,
                       show_fig=True, plotting_dimensions=2):
    """
        INPUTS :
        --------
        lattice_data : (N, L, L) or (N, M, L, L) numpy array of {-1, 1}, single level or multilevel spin data.
        no_iterations :  int, number of frames
        save_fig=False : Bool, if set to True then the animation will be saved in the
                        directory the script is being run in.
        filename=None : None or string, a string that the file is saved under
        show_fig=True : Bool, if True then the animation will display
        dt : float, change in time between frames

        RETURNS :
        ---------
        ani : Instance of matplotlib.animation.FuncAnimation class
    """

    # Flatten the data
    data = slice_data[0]

    # Create figure and axis
    fig, axes = plt.subplots(4, 1)

    a, b = numpy.histogram(data, int(L / 2))

    ax1 = axes[0].bar(b[:-1], a, width=4 / L, align='edge')

    axes = [bar_chart]

    def update(num):
        data = slice_data[num]
        a, b = numpy.histogram(data, int(L / 2))

        axs = [ax1]

        for bar, h in zip(axs[0], a):
            bar.set_height(h)

        return axes

    # Creating the Animation object
    ani = FuncAnimation(fig, update, frames=range(no_iterations),
                        interval=int(dt * 1000), blit=True, repeat=False)

    return ani