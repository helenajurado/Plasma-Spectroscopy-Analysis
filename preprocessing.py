"""Preprocessing utilities for simple spectroscopy analysis."""
from __future__ import annotations

import numpy as np
import pandas as pd


def load_spectrum(path: str) -> pd.DataFrame:
    """Load a CSV file with columns wavelength_nm and intensity."""
    df = pd.read_csv(path)
    required = {"wavelength_nm", "intensity"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}. Expected {required}.")
    return df.sort_values("wavelength_nm").reset_index(drop=True)


def estimate_baseline(wavelength_nm: np.ndarray, intensity: np.ndarray, degree: int = 2) -> np.ndarray:
    """Estimate a smooth polynomial baseline.

    This is deliberately simple: it is good enough for the included sample data,
    but real spectra often require better baseline correction methods.
    """
    coeffs = np.polyfit(wavelength_nm, intensity, degree)
    return np.polyval(coeffs, wavelength_nm)


def subtract_baseline(df: pd.DataFrame, degree: int = 2) -> pd.DataFrame:
    """Return a copy of the spectrum with baseline and corrected intensity columns."""
    out = df.copy()
    baseline = estimate_baseline(out["wavelength_nm"].to_numpy(), out["intensity"].to_numpy(), degree)
    out["baseline"] = baseline
    out["intensity_corrected"] = out["intensity"] - baseline
    return out
