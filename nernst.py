"""Nernst potential for a single ion (K+, monovalent cation).

Equation (single ion, equilibrium potential E_ion = 0):
    E = (RT / zF) * ln(Q)

For K+ (z = +1), with Q = K_out / K_in and converting ln -> log10
(ln(x) = ln(10) * log10(x)):

    E = (RT / F) * ln(K_out / K_in)
      = (RT / F) * ln(10) * log10(K_out / K_in)

Sanity checks (monovalent cation slope in mV per decade of K_out / K_in):
    37 C (310.15 K): slope = 61.54 mV/decade  -> K_in=140, K_out=4: E ~ -94.8 mV
    25 C (298.15 K): slope = 59.16 mV/decade
"""

import math

R = 8.314462618        # gas constant, J / (mol K)
F = 96485.33212        # Faraday constant, C / mol
LN10 = 2.302585092994046  # ln(10)


def kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15


def slope_mv_per_decade(T_celsius=37.0):
    """Nernst slope for a monovalent ion (mV per 10x of K_out/K_in)."""
    T = kelvin(T_celsius)
    return (R * T / F) * 1000.0 * LN10


def ek_mv(K_in, K_out, T_celsius=37.0):
    """Forward: K+ equilibrium potential in mV from concentrations.

    Parameters
    ----------
    K_in, K_out : float
        Intra- and extracellular K+ concentration (mmol/L).
    T_celsius : float
        Bath (extracellular solution) temperature in Celsius.

    Returns
    -------
    float
        E_K in mV.
    """
    if K_in <= 0 or K_out <= 0:
        raise ValueError("Concentrations must be > 0.")
    return slope_mv_per_decade(T_celsius) * math.log10(K_out / K_in)


def k_in_mmol(E_mv, K_out, T_celsius=37.0):
    """Reverse: intracellular K+ concentration (mmol/L) from E_K and K_out.

    From E = slope * log10(K_out / K_in):
        K_in = K_out / 10 ** (E / slope)
    """
    if K_out <= 0:
        raise ValueError("Extracellular concentration must be > 0.")
    slope = slope_mv_per_decade(T_celsius)
    return K_out / (10 ** (E_mv / slope))


if __name__ == "__main__":
    print("Slope at 37 C: %.3f mV/decade" % slope_mv_per_decade(37.0))
    print("Slope at 25 C: %.3f mV/decade" % slope_mv_per_decade(25.0))
    print("E_K(140, 4, 37 C) = %.3f mV" % ek_mv(140.0, 4.0, 37.0))
