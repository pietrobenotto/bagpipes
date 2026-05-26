from __future__ import print_function, division, absolute_import

import numpy as np

try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt

except RuntimeError:
    pass

from .general import *

from .. import utils


def plot_sfh_posterior(fit, show=False, save=True, colorscheme="bw",logScale=False):
    """ Make a plot of the SFH posterior. """

    update_rcParams()

    fig = plt.figure(figsize=(12, 4))
    ax = plt.subplot()

    add_sfh_posterior(fit, ax, colorscheme=colorscheme, logScale=logScale)

    if save:
        plotpath = "pipes/plots/" + fit.run + "/" + fit.galaxy.ID + "_sfh.pdf"
        plt.savefig(plotpath, bbox_inches="tight")
        plt.close(fig)

    if show:
        plt.show()
        plt.close(fig)

    return fig, ax


def add_sfh_posterior(fit, ax, colorscheme="bw", z_axis=True, zorder=4,
                      label=None, logScale=False, zvals=[0, 0.5, 1, 2, 4, 10]):

    color1 = "black"
    color2 = "gray"
    alpha = 0.6

    if colorscheme == "irnbru":
        color1 = "darkorange"
        color2 = "navajowhite"
        alpha = 0.6

    if colorscheme == "purple":
        color1 = "purple"
        color2 = "purple"
        alpha = 0.4

    if colorscheme == "blue":
        color1 = "dodgerblue"
        color2 = "dodgerblue"
        alpha = 0.7

    if colorscheme == "green":
        color1 = "green"
        color2 = "green"
        alpha = 0.4

    # Calculate median redshift and median age of Universe
    if "redshift" in fit.fitted_model.params:
        redshift = np.median(fit.posterior.samples["redshift"])

    else:
        redshift = fit.fitted_model.model_components["redshift"]

    age_of_universe = np.interp(redshift, utils.z_array, utils.age_at_z)

    # Calculate median and confidence interval for SFH posterior
    post = np.percentile(fit.posterior.samples["sfh"], (16, 50, 84), axis=0).T

    # Plot the SFH
    x = fit.posterior.sfh.ages*10**-9 #Gyr

    ax.plot(x, post[:, 1], color=color1, zorder=zorder+1)
    ax.fill_between(x, post[:, 0], post[:, 2], color=color2,
                    alpha=alpha, zorder=zorder, lw=0, label=label)

    ax.set_ylim(0., np.max([ax.get_ylim()[1], 1.1*np.max(post[:, 2])]))


    if logScale:
        ax.set_xlim(0.003,age_of_universe) #5Myr
        ax.set_xscale("log")
    else:
        ax.set_xlim(0,age_of_universe)


    # Add redshift axis along the top
    if z_axis and not logScale:
        ax2 = add_z_axis(ax, zvals=zvals,logScale=False)
        ax2.set_xlim(ax2.get_xlim()[::-1])

        #ax.set_xlim(left=1.e-3)

    # Set axis labels
    ax.tick_params(axis='both', which='major', labelsize=10)

    if tex_on:
        ax.set_ylabel("$\\mathrm{SFR\\ \\ [M_\\odot\\ \\mathrm{yr}^{-1}]}$",fontsize=10)
        ax.set_xlabel("$\\mathrm{Lookback\\ time\\ \\ [Gyr]}$",fontsize=10)

    else:
        ax.set_ylabel("SFR / M_sol yr^-1",fontsize=10)
        ax.set_xlabel("Lookback time / Gyr",fontsize=10)

    if z_axis and not logScale:
        return ax2
