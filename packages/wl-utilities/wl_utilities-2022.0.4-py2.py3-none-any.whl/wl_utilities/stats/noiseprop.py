"""
The purpose of this code is to take a table containing the stacked &
single run values for flux & ivar for the sky-subtracted sky spectra
from a single WEAVE OB, and compare its Z-score distribution with a
normal distribution. The output is a pair of plots to help diagnose
whether ivar array is correct, as well as the recovered standard
deviation of fitting a Gaussian to each Z-score distribution (for
the stack and all runs). If the noise estimates and sky subtraction
are correct then it should be a normal distribution with a mean of
zero and standard deviation of one. It takes in a table described as
above, plus an optional file name for the PDF output, and a
non-optional mask to allow the user to focus on particular wavelengths
if desired.

TO DO: - how does this distribution vary by fibre? What about by
position on the plate/spectrograph?

-fit the distributions per sky fibre and see whether/how the
mean/stdev/skewness vary of if consistent over the OB

Original version by Dan Smith (daniel.j.b.smith@gmail.com) - please
don't judge my coding.
"""
import itertools
from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from lmfit.model import ModelResult
from lmfit.models import GaussianModel
from typing import List


def compute_z(v, ivar):
    """Computes z-score for an array v, given its inverse variance array"""
    kak = np.ones(v.T.shape) * np.median(v, axis=1)
    means = kak.T
    z = (v - means) * np.sqrt(ivar)
    zmask = ivar != 0
    return z, zmask


def make_histogram(flux, ivar, bins):
    """
    Returns a (bin_count, bin_centre) for a histogram of z-values defined by flux and ivar,
    and spanning a range defined input `bins`.
    :param flux: np.array of flux values
    :param ivar: np.array of inverse variance values
    :param bins: np.array of left edge values
    :return: bin_count, bin_centre
    """
    z, z_mask = compute_z(flux, ivar)
    nstack, b = np.histogram(z[z_mask].flatten(), bins=bins)
    x = b[:-1] + (0.5 * (b[1] - b[0]))
    return nstack, x


def fit_model(model: GaussianModel, y: np.ndarray, x: np.ndarray) -> ModelResult:
    """
    Fit a Gaussian model to the data.
    :param model: GaussianModel object
    :param y: np.array of ydata values (probably flux)
    :param x: np.array of xdata values (probably z-values)
    :return: ModelResult object
    """
    params = model.make_params(amplitude=np.max(y), center=0, sigma=1)
    result = model.fit(x, params, x=x)
    return result


zscore_fit = namedtuple("zscore_fit", ["nz", "x", "fit"])


def fit_zscore_models(table, bins, mask=None):
    """
    Fit a Gaussian to the z-scores of stack and single fluxes, return a namedtuple containing
    count(zscore), zscore, gaussian fit
    :param table: Table
    :param bins: np.array
    :param mask: np.array[boolean]
    """
    if mask is None:
        mask = np.ones_like(table[0]["stack_flux"], dtype=bool)
    model = GaussianModel()
    nstack, xstack = make_histogram(table["stack_flux"][:, mask], table["stack_ivar"][:, mask], bins)
    stack_result = fit_model(model, nstack, xstack)
    stack = zscore_fit(nstack, xstack, stack_result)
    sz = table["single_flux"].shape
    nruns = sz[1]

    singles = []
    for i in range(nruns):
        n_single, x_single = make_histogram(
            table["single_flux"][:, i, mask], table["single_ivar"][:, i, mask], bins
        )
        result_single = fit_model(model, n_single, x_single)
        single = zscore_fit(n_single, x_single, result_single)
        singles.append(single)
    return stack, singles


def plot_zscores(ax, bins, stack_result: zscore_fit, single_results: List[zscore_fit] = None):
    """
    Plot the zscore distribution for the stack run and each of the single runs.
    Also, plot the standard normal distribution for reference
    :param ax: Matplotlib.axes
    :param bins: np.array of bin edges
    :param stack_result: fitting result for stack
    :param single_results: list of fitting results for single
    """
    if single_results is None:
        single_results = []
    ax.fill_between(stack_result.x, stack_result.nz, step="post", alpha=0.3, label="stack")
    for i, single_result in enumerate(single_results):
        ax.step(single_result.x, single_result.nz, where="post", label=f"single#{i}", alpha=0.5)
    mu = 0
    sigma = 1
    x = np.linspace(mu - 5 * sigma, mu + 5 * sigma, 300)
    gauss = stats.norm.pdf(x, mu, sigma)
    gauss = gauss * (np.sum(stack_result.nz) / np.sum(gauss)) * (len(x) / len(bins))
    ax.plot(x, gauss, label="Expected")
    ax.legend()
    ax.set_xlabel("Z-score")
    ax.set_ylabel(r"$\propto P$")
    ax.set_xlim(-4, 4)


def plot_zscore_diff(ax, result1: zscore_fit, result2: zscore_fit, dz=0.0, errorbar=False, **kwargs):
    """Plot the difference between two fitting results
    :param ax: matplotlib axes
    :param result1: fitting result
    :param result2: fitting result
    :param dz: jitter results by
    :param errorbar: if True, plot the error bar
    :param kwargs: matplotlib kwargs for errorbar/scatter
    """
    if errorbar:
        return ax.errorbar(
            result1.x + dz, result2.nz - result1.nz, yerr=np.sqrt(result2.nz + result1.nz), **kwargs
        )
    return ax.scatter(result1.x + dz, result2.nz - result1.nz, **kwargs)


def plot_zscore_diffs(ax, stack_result: zscore_fit, single_results: List[zscore_fit] = None, dz=0.0):
    """Plot the difference between stacked and single fitting results
    :param ax: matplotlib axes
    :param stack_result: fitting result for stacked run
    :param single_results: list of single results
    :param dz: jitter results by
    """
    plot_zscore_diff(ax, single_results[0], single_results[1], errorbar=True, fmt=".", label="#2-#1")
    # plot diffs of the combinations of single results
    combinations = set(itertools.combinations(range(len(single_results)), 2)) - {(0, 1)}
    for combination in combinations:
        result1, result2 = single_results[combination[0]], single_results[combination[1]]
        plot_zscore_diff(
            ax, result1, result2, dz, errorbar=False, label=f"#{combination[1]+1}-#{combination[0]+1}"
        )
    # plot diffs of stack-singles
    for i, result in enumerate(single_results):
        _dz = ((-1) ** i) * (dz * ((i // 2) + 2))  # jitter the plots
        plot_zscore_diff(ax, result, stack_result, _dz, errorbar=True, label=f"single-#{i+1}")
    ax.legend()
    ax.set_xlabel("Z-score")
    ax.set_ylabel(r"$N(Z_1) - N(Z_2)$")


def plot_noise_properties(table, mask=None, bins=np.linspace(-5, 5, 60), plot_dz=0.0):
    """
    Plots the z-scores (x-mu / std) of the single and stacked runs given a table containing those results
    (expects column names of stack_flux and single_flux).
    Also plots the differences between pairs of (stack, single) and (single, single).
    :param table: Table
    :param mask: boolean
    :param bins: np.array
    """
    stack_result, single_results = fit_zscore_models(table, bins, mask)
    fig, axs = plt.subplots(2, figsize=(12, 10))
    plot_zscores(axs[0], bins, stack_result, single_results)
    plot_zscore_diffs(axs[1], stack_result, single_results, dz=plot_dz)
    return fig, axs


if __name__ == "__main__":
    # The purpose of this code is to find a WEAVE OB, identify the sky
    # fibres, and then use noiseprop.py to compare the distribution of the
    # sky-subtracted skyfibres with a normal distribution, for the
    # individual runs as well as the stacks. The output is a selection of
    # plots to help diagnose whether ivar array is correct and fits to the
    # resulting Z-score distribution. If the noise estimates are correct
    # then it should be a normal distribution with a mean of zero and
    # standard deviation of one.
    #
    # Original version by Dan Smith (daniel.j.b.smith@gmail.com)
    #
    from weaveio import *

    data = Data()

    def noise_spectra_query(
        parent, camera, use_sky_subtracted_spectra=False, targuse="S", split_into_subqueries=True
    ):
        # noqa
        if split_into_subqueries:
            parent = split(parent)
        stacks = parent.l1stack_spectra[
            (parent.l1stack_spectra.targuse == targuse) & (parent.l1stack_spectra.camera == camera)
        ]
        singles = stacks.l1single_spectra  # get single spectra for each stack spectrum
        if not use_sky_subtracted_spectra:
            stacks = stacks.noss
            singles = singles.noss
        singles_table = singles[["flux", "ivar"]]
        query = stacks[
            [stacks.obs.id, {"stack_flux": "flux", "stack_ivar": "ivar"}, "wvl", {"single_": singles_table}]
        ]  # add in the single spectra per stack spectrum
        return query

    # I just want WL-WIDE OBs:
    obs = data.obs
    # obs = obs[any(obs.surveys == 'WL-WIDE', wrt=obs)]
    obs = obs[obs.id == 3434]

    info = noise_spectra_query(obs, "blue", split_into_subqueries=False, use_sky_subtracted_spectra=True)
    table = info()
    plot_noise_properties(table, None)
    plt.savefig("test1_blue.pdf", bbox_inches="tight")

    info = noise_spectra_query(obs, "red", split_into_subqueries=False, use_sky_subtracted_spectra=True)
    table = info()
    plot_noise_properties(table, None)
    plt.savefig("test1_red.pdf", bbox_inches="tight")
    plt.show()
