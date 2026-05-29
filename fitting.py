"""Peak detection, Gaussian fitting and simple physical estimates."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# Physical constants
C = 299_792_458.0          # m/s
H = 6.62607015e-34         # J s
K_B = 1.380649e-23         # J/K
EV = 1.602176634e-19       # J


@dataclass
class GaussianFit:
    line_name: str
    center_nm: float
    amplitude: float
    sigma_nm: float
    offset: float
    fwhm_nm: float
    area: float
    velocity_shift_kms: float


def gaussian(x: np.ndarray, amplitude: float, center: float, sigma: float, offset: float) -> np.ndarray:
    """Gaussian emission line plus constant offset."""
    return amplitude * np.exp(-0.5 * ((x - center) / sigma) ** 2) + offset


def detect_peaks(df: pd.DataFrame, prominence: float = 0.15, distance: int = 40) -> np.ndarray:
    """Detect emission peaks in a baseline-corrected spectrum."""
    y = df["intensity_corrected"].to_numpy()
    peaks, _ = find_peaks(y, prominence=prominence * np.max(y), distance=distance)
    return peaks


def fit_line(
    df: pd.DataFrame,
    line_name: str,
    expected_center_nm: float,
    window_nm: float = 3.0,
) -> tuple[GaussianFit, pd.DataFrame]:
    """Fit one emission line around an expected wavelength."""
    mask = (df["wavelength_nm"] >= expected_center_nm - window_nm) & (df["wavelength_nm"] <= expected_center_nm + window_nm)
    local = df.loc[mask].copy()
    if len(local) < 8:
        raise ValueError(f"Not enough data points to fit {line_name}.")

    x = local["wavelength_nm"].to_numpy()
    y = local["intensity_corrected"].to_numpy()

    p0 = [float(np.max(y) - np.min(y)), expected_center_nm, 0.35, float(np.median(y))]
    bounds = ([0, expected_center_nm - window_nm, 0.02, -np.inf], [np.inf, expected_center_nm + window_nm, 3.0, np.inf])
    popt, _ = curve_fit(gaussian, x, y, p0=p0, bounds=bounds, maxfev=20000)
    amplitude, center, sigma, offset = popt

    fwhm = 2 * np.sqrt(2 * np.log(2)) * abs(sigma)
    area = abs(amplitude * sigma * np.sqrt(2 * np.pi))
    velocity_shift = C * ((center - expected_center_nm) / expected_center_nm) / 1000.0

    fit = GaussianFit(
        line_name=line_name,
        center_nm=float(center),
        amplitude=float(amplitude),
        sigma_nm=float(abs(sigma)),
        offset=float(offset),
        fwhm_nm=float(fwhm),
        area=float(area),
        velocity_shift_kms=float(velocity_shift),
    )
    local["fit"] = gaussian(x, *popt)
    return fit, local


def photon_energy_ev(wavelength_nm: float) -> float:
    """Photon energy in eV from wavelength in nm."""
    wavelength_m = wavelength_nm * 1e-9
    return H * C / wavelength_m / EV


def doppler_temperature_from_fwhm(line_center_nm: float, fwhm_nm: float, ion_mass_kg: float = 1.6735575e-27) -> float:
    """Estimate ion temperature from Doppler broadening.

    Assumes the measured FWHM is entirely thermal Doppler broadening.
    This is an upper-limit style estimate for teaching purposes because real spectra
    also include instrumental, pressure and Stark broadening.
    """
    delta_lambda_m = fwhm_nm * 1e-9
    lambda_m = line_center_nm * 1e-9
    return (ion_mass_kg * C**2 / (8 * K_B * np.log(2))) * (delta_lambda_m / lambda_m) ** 2


def fits_to_dataframe(fits: list[GaussianFit]) -> pd.DataFrame:
    """Convert a list of GaussianFit objects into a clean results table."""
    return pd.DataFrame([fit.__dict__ for fit in fits])
