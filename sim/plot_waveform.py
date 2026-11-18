#!/usr/bin/env python3
"""Plot the two oscillator states captured by waveform.cir."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load(fn):
    d = np.loadtxt(fn)
    return d[:,0]*1e6, d[:,1], d[:,2]   # time[us], tank, out

tA, tankA, outA = load("waveA.txt")
tB, tankB, outB = load("waveB.txt")

# window: first 2 us
w = 2.0
mA = tA <= w
mB = tB <= w

fig, ax = plt.subplots(2, 2, figsize=(12, 6), sharex="col")

# V(out) square wave
ax[0,0].plot(tA[mA], outA[mA], color="#fb7185", lw=1.5)
ax[0,0].set_title("State A — relay OPEN  (C = C0 + Cp + Cstray ≈ 43 pF)", fontsize=11)
ax[0,0].set_ylabel("V(out)  [V]")
ax[0,0].set_ylim(-0.2, 3.5); ax[0,0].grid(alpha=.3)
ax[0,0].text(0.02, 0.9, "f₁ ≈ 7.67 MHz", transform=ax[0,0].transAxes, fontsize=12, color="#fb7185")

ax[0,1].plot(tB[mB], outB[mB], color="#38bdf8", lw=1.5)
ax[0,1].set_title("State B — relay CLOSED (C = C0 + Cs + Cp + Cstray ≈ 143 pF)", fontsize=11)
ax[0,1].set_ylabel("V(out)  [V]")
ax[0,1].set_ylim(-0.2, 3.5); ax[0,1].grid(alpha=.3)
ax[0,1].text(0.02, 0.9, "f₂ ≈ 4.20 MHz", transform=ax[0,1].transAxes, fontsize=12, color="#38bdf8")

# V(tank) sine
ax[1,0].plot(tA[mA], tankA[mA], color="#34d399", lw=1.5)
ax[1,0].set_xlabel("time [µs]"); ax[1,0].set_ylabel("V(tank)  [V]")
ax[1,0].grid(alpha=.3); ax[1,0].set_ylim(1.2, 2.1)

ax[1,1].plot(tB[mB], tankB[mB], color="#c084fc", lw=1.5)
ax[1,1].set_xlabel("time [µs]"); ax[1,1].set_ylabel("V(tank)  [V]")
ax[1,1].grid(alpha=.3); ax[1,1].set_ylim(1.2, 2.1)

fig.suptitle("LCR/EPC Meter — LC oscillator + relay calibration (ngspice, Option B)", fontsize=13)
fig.tight_layout()
fig.savefig("oscillator_states.png", dpi=130)
print("saved oscillator_states.png")
