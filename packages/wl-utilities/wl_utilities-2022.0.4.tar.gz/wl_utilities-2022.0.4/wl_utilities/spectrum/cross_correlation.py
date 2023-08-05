from scipy.signal import correlate, correlation_lags
import numpy as np


def cross_correlate_spectra(s, sref, wl, wlref, dwl=0.1):
    """
    Takes in a spectrum (s) and corresponding wl array (wl) to cross
    correlate with a reference wavelength-calibrated spectrum (sref)
    and correspnding wavelength array (wlref). Interpolates to a
    common wavelength grid, then does cross-correlation and
    calculates the wavelength of the peak in the cross-correlation
    function.
    :param s: spectrum flux array
    :param sref: reference flux array
    :param wl: wavelength array
    :param wlref: reference wavelength array
    dwl: wavelength step size
    return: lag array, cross-correlation function, and the maximum lag
    """
    wl_min = np.int(np.round(np.max([np.min(wl), np.min(wlref)])))
    wl_max = np.int(np.round(np.min([np.max(wl), np.max(wlref)])))
    steps = np.int((wl_max - wl_min) / dwl)

    wl_common = np.linspace(wl_min, wl_max, steps)

    s1 = np.interp(wl_common, wl, s)
    sref1 = np.interp(wl_common, wlref, sref)
    correlation = correlate(s1, sref1, mode="full")
    lags = correlation_lags(s1.size, sref1.size, mode="full")
    lags = lags * dwl
    lag = lags[np.argmax(correlation)]

    return lags, correlation, lag


if __name__ == "__main__":
    # The purpose of this example is to get some data a WEAVE OB, identify
    # the sky fibres, and then use wl_test.py to compare the wavelength
    # solution of a test sky spectrum (not sky subtracted) with another
    # sky spectrum with known calibration (e.g. the example below using
    # the gemini sky spectrum). The output is a lag in angstroms, which in
    # the examples below has automatically been offset by 50.48 A just to
    # see if it can be recovered. The WEAVE model wavelength solution
    # seems to be good to ~0.7 Angstrom relative to the Gemini spectrum.
    #
    # Original version by Dan Smith (daniel.j.b.smith@gmail.com)
    #

    from weaveio import *
    import matplotlib.pyplot as plt
    import numpy as np

    data = Data()

    ob = data.obs[3434]

    # read in a single OB of spectra
    specs = ob.l1single_spectra[ob.l1single_spectra.colour == "blue"]
    specs = specs[specs.targuse == "S"]
    info = specs.noss[["wvl", "flux"]]
    table = info(limit=50)

    spec2test = table["flux"][0, :]
    wl2test = table["wvl"][0, :] + 50.48

    spec_ref = table["flux"][30, :]
    wl_ref = table["wvl"][20, :]

    lags, corr, lag = cross_correlate_spectra(spec2test, spec_ref, wl2test, wl_ref)

    plt.plot(lags, corr)
    plt.xlim(-100, 100)
    plt.xlabel("Offset (wavelength, angstrom)")
    plt.ylabel("Correlation")
    plt.savefig("eg.pdf", bbox_inches="tight")

    print("Lag in A relative a reference sky spec fibre: {:.1f}".format(lag))

    # try again this time using a GEMINI sky spectrum downloaded from
    # https://www.gemini.edu/observing/telescopes-and-sites/sites#OptSky
    #

    from astropy.io import ascii

    data = ascii.read("skybg_50_10.dat")
    spec_ref = data["spec"]
    wl_ref = data["nm"] * 10.0  # is in nm, so x 10

    lags, corr, lag = cross_correlate_spectra(spec2test, spec_ref, wl2test, wl_ref, dwl=1e-2)
    plt.figure()
    plt.plot(lags, corr)
    plt.xlim(-100, 100)
    plt.xlabel("Offset (wavelength, angstrom)")
    plt.ylabel("Correlation")
    plt.savefig("eg_gemini.pdf", bbox_inches="tight")

    print("Lag in A relative to Gemini sky spec: {:.2f}".format(lag))

    plt.show()
