#!/usr/bin/env python3
"""
Solve Lx, Cp, SRF from the two frequencies measured by the SPICE simulation.

Usage:
    python3 solve.py [f1] [f2] [Cs] [C0] [Cstray]

Example (values printed by ngspice):
    python3 solve.py 7.667830e6 4.198656e6
"""
import math, sys

def solve(f1, f2, Cs=100e-12, C0=33e-12, Cstray=5e-12):
    K  = (f1 / f2) ** 2                 # ratio of squared frequencies
    CA = Cs / (K - 1)                   # total capacitance in state A
    Cp = CA - (C0 + Cstray)             # EPC
    Lx = 1 / ((2 * math.pi * f1) ** 2 * CA)
    SRF = 1 / (2 * math.pi * math.sqrt(Lx * Cp)) if Cp > 0 else float('inf')
    return K, CA, Cp, Lx, SRF

if __name__ == "__main__":
    f1 = float(sys.argv[1]) if len(sys.argv) > 1 else 7.667830e6
    f2 = float(sys.argv[2]) if len(sys.argv) > 2 else 4.198656e6
    Cs = float(sys.argv[3]) if len(sys.argv) > 3 else 100e-12
    C0 = float(sys.argv[4]) if len(sys.argv) > 4 else 33e-12
    Cstray = float(sys.argv[5]) if len(sys.argv) > 5 else 5e-12

    K, CA, Cp, Lx, SRF = solve(f1, f2, Cs, C0, Cstray)

    print(f"f1 (state A)      = {f1/1e6:.4f} MHz")
    print(f"f2 (state B)      = {f2/1e6:.4f} MHz")
    print(f"K = (f1/f2)^2     = {K:.4f}")
    print(f"C_A = Cs/(K-1)    = {CA*1e12:.3f} pF")
    print(f"Cp  = C_A-C0-Cst  = {Cp*1e12:.3f} pF")
    print(f"Lx                = {Lx*1e6:.4f} uH")
    print(f"SRF               = {SRF/1e6:.3f} MHz")
