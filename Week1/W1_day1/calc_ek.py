"""Forward K+ equilibrium potential calculator (interactive)."""

from nernst import ek_mv


def main():
    print("=== K+ equilibrium potential (forward) ===")
    try:
        K_in = float(input("Intracellular K+ [mmol/L]: "))
        K_out = float(input("Extracellular K+ [mmol/L]: "))
        T = input("Bath temperature [C] (default 37): ").strip()
        T = 37.0 if T == "" else float(T)

        if K_in <= 0 or K_out <= 0:
            print("Error: concentrations must be > 0.")
            return
        if K_out >= K_in:
            print("Warning: K_out >= K_in is non-physiological; "
                  "E_K should be negative for K+.")

        E = ek_mv(K_in, K_out, T)
        print("\nE_K = %.2f mV" % E)
    except ValueError as e:
        print("Invalid input:", e)


if __name__ == "__main__":
    main()
