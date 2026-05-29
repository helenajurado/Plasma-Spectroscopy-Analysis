"""Plotting utilities for spectroscopy analysis."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_spectrum(df: pd.DataFrame, output_path: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(df["wavelength_nm"], df["intensity"], label="Measured spectrum")
    if "baseline" in df.columns:
        ax.plot(df["wavelength_nm"], df["baseline"], linestyle="--", label="Estimated baseline")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Intensity (arb. units)")
    ax.set_title("Emission spectrum")
    ax.legend()
    fig.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_fit(df: pd.DataFrame, fitted_windows: list[pd.DataFrame], output_path: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(df["wavelength_nm"], df["intensity_corrected"], label="Baseline-corrected spectrum")
    for window in fitted_windows:
        ax.plot(window["wavelength_nm"], window["fit"], linewidth=2)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Corrected intensity (arb. units)")
    ax.set_title("Gaussian fits to emission lines")
    ax.legend()
    fig.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_residuals(fitted_windows: list[pd.DataFrame], output_path: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for window in fitted_windows:
        residual = window["intensity_corrected"] - window["fit"]
        ax.plot(window["wavelength_nm"], residual)
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Residual (arb. units)")
    ax.set_title("Fit residuals")
    fig.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=180)
    plt.close(fig)
