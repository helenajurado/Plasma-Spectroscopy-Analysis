# Plasma Spectroscopy Analysis

A small scientific Python project for analysing emission spectra using peak detection and Gaussian fitting. This project connects numerical data analysis with basic physical interpretation of spectral lines, with applications in plasma physics, astrophysics and radiation analysis.

![Spectrum fit](figures/spectrum_fit.png)

## Goal

The goal of this project is to build a simple and reproducible pipeline for analysing emission spectra. The analysis focuses on identifying spectral lines, fitting them with Gaussian profiles, extracting relevant parameters and interpreting them from a physical point of view.

## Motivation

I chose this project because I am interested in plasma physics, spectroscopy, nuclear fusion and astrophysics. I think spectral line analysis is a simple but realistic way to connect scientific programming with physical interpretation.

## Physics background

Emission spectra contain peaks at specific wavelengths. These peaks are associated with radiative transitions in atoms, ions or molecules. In plasma physics and astrophysics, spectral lines can provide information about the physical conditions of the emitting system. In this project, each spectral line is approximated using a Gaussian profile. From the fitted profile, we can estimate:

* the central wavelength of the line
* the line amplitude
* the line width
* the integrated intensity
* the residuals of the fit

The central wavelength can also be related to the photon energy using:

$$
E = \frac{hc}{\lambda}
$$

where (h) is Planck's constant, (c) is the speed of light and $\lambda$) is the wavelength.



