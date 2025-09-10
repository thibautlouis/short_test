import numpy as np
import matplotlib.pyplot as plt

lam = np.linspace(3600, 9800, 9000)
z0 = 0.2
z1 = 1
lines_em = {
    "[O II]": 3727.0,
    "Hβ": 4861.3,
}
lines_abs = {
    "Ca K": 3934.0,
    "Ca H": 3969.0,
}

def rest_continuum(lam_rest):
    pw = (lam_rest/5500.0)**(-1.5)
    brk = 1.0 - 0.35*0.5*(1.0 + np.tanh((4000.0 - lam_rest)/120.0))
    return pw * brk

def gaussian(x, mu, sigma):
    return np.exp(-0.5*((x-mu)/sigma)**2)

def sigma_R(lam_obs, R=3000):
    return lam_obs/(R*2.355)

def add_lines(lam_obs, lines, z, flux, amp_scale=1.0, R=3000):
    out = flux.copy()
    for lr in lines.values():
        lo = lr*(1+z)
        sig = sigma_R(lo, R)
        out += amp_scale*gaussian(lam_obs, lo, sig)
    return out

def make_spectrum(lam_obs, z, seed=0):
    lam_rest = lam_obs/(1+z)
    flux = rest_continuum(lam_rest)
    flux = add_lines(lam_obs, lines_em, z, flux, amp_scale=1.0)
    flux = add_lines(lam_obs, lines_abs, z, flux, amp_scale=-0.3)
    rng = np.random.default_rng(seed)
    flux = flux + rng.normal(0, 0.02, lam_obs.shape)
    return flux/np.percentile(flux, 95)

flux_z04 = make_spectrum(lam, z0, seed=1)
flux_z08 = make_spectrum(lam, z1, seed=2)

plt.figure(figsize=(14,6))
plt.plot(lam, flux_z04, lw=1.0, color="tab:blue", label="spectre galaxie fixe", alpha=1)
#plt.plot(lam, flux_z08, lw=1.0, color="tab:red", label="spectre galaxie qui s'éloigne")
#plt.show()


#sys.exit()
def mark_lines(z, y_offset, color, alpha=1):
    # Décalage horizontal des labels pour lisibilité
    offsets = {"left": -50, "right": 50}
    toggle = True
    for name, lr in {**lines_em, **lines_abs}.items():
        lo = lr*(1+z)
        if lam.min() <= lo <= lam.max():
            plt.axvline(lo, color=color, ls=":", lw=0.8, alpha=0.7)
            dx = offsets["left"] if toggle else offsets["right"]
            toggle = not toggle
            plt.text(lo+dx, y_offset, name, color=color, fontsize=14,
                     rotation=90, ha="center", va="bottom", alpha=alpha)

mark_lines(z0, 1.05, "tab:blue", alpha=1)
#mark_lines(z1, 1.05, "tab:red")
plt.ylim(0.3,1.5)
plt.yticks(fontsize=24)
plt.xticks(fontsize=24)
plt.ylabel("Spectre", fontsize=24)
plt.xlabel("Longueur d’onde observée [Å]", fontsize=24)
plt.legend(fontsize=22)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("spectre_fixed.png", bbox_inches="tight")
plt.clf()
plt.close()
