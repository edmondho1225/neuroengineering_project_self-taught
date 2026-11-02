"""Reverse calculator: intracellular K+ from E_K and extracellular K+."""

from nernst import k_in_mmol


def main():
    print("=== Intracellular K+ from E_K (reverse) ===")
    try:
        E_mv = float(input("Measured equilibrium potential E_K [mV]: "))
        K_out = float(input("Extracellular K+ [mmol/L]: "))
        T = input("Bath temperature [C] (default 37): ").strip()
        T = 37.0 if T == "" else float(T)

        if K_out <= 0:
            print("Error: extracellular concentration must be > 0.")
            return

        K_in = k_in_mmol(E_mv, K_out, T)
        print("\nIntracellular K+ = %.2f mmol/L" % K_in)
    except ValueError as e:
        print("Invalid input:", e)


if __name__ == "__main__":
    main()
