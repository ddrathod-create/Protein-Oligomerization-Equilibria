# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:27:19 2026

@author: Dhanashri
"""

"""
FCS Oligomerization Simulator — Streamlit version
Simulates apparent diffusion time (tau_app) and fractional species concentrations
for dimer, trimer, and tetramer equilibria models.
"""

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FCS Oligomerization Simulator",
    page_icon="🔬",
    layout="wide",
)

# ── Plot palette ───────────────────────────────────────────────────────────────
C_TAU    = "#000000"
C_MONO   = "#0072b2"
C_DIMER  = "#e69f00"
C_TRIMER = "#cc79a7"
C_TETRA  = "#009e73"

PLOT_RC = {
    "axes.facecolor":   "#ffffff",
    "figure.facecolor": "#f7f7f7",
    "axes.edgecolor":   "#aaaaaa",
    "axes.labelcolor":  "#111111",
    "axes.grid":        True,
    "grid.color":       "#eeeeee",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.5,
    "xtick.color":      "#444444",
    "ytick.color":      "#444444",
    "text.color":       "#111111",
    "legend.facecolor": "#ffffff",
    "legend.edgecolor": "#dddddd",
    "legend.fontsize":  9,
    "font.size":        10,
    "axes.titlesize":   11,
    "axes.labelsize":   10,
}

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #f0f0f0;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #0072b2;
        font-size: 1.1rem;
    }
    /* Main run button */
    div.stButton > button {
        width: 100%;
        background-color: #000000;
        color: #ffffff;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.55rem;
        border: none;
        font-size: 1rem;
        letter-spacing: 0.02em;
        transition: background 0.15s;
    }
    div.stButton > button:hover {
        background-color: #222222;
        color: #ffffff;
    }
    div.stButton > button:active {
        background-color: #444444;
    }
    /* Remove excess top padding */
    .block-container { padding-top: 1.5rem; }
    /* Metric labels */
    [data-testid="metric-container"] label { font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)


# ── Physics ────────────────────────────────────────────────────────────────────

def dimer_equilibria(C2, KD, f, C_l):
    C = 2 * C2
    r2 = 0.79
    alpha1 = (1 / (C * 4)) * (-KD + np.sqrt(8 * C * KD + KD**2))
    alpha2 = 1 - alpha1
    c = 1 - 2 * (alpha1 / (1 + (1 - alpha1) * (C_l * f / C)))
    tau_app = 0.5 * (c * (1 - r2) + np.sqrt(c**2 * (1 - r2)**2 + 4 * r2))
    return tau_app, alpha1, alpha2, np.zeros_like(alpha1), np.zeros_like(alpha1)


def trimer_equilibria(C3, KD, f, C_l):
    r3 = 0.69
    C = 3 * C3
    a1 = 9 * C**4 * KD + np.sqrt(81 * C**8 * KD**2 + 4 * C**6 * KD**3)
    f1 = (2**(1/3) * KD) / (a1**(1/3))
    f2 = (a1**(1/3)) / (2**(1/3) * C**2)
    alpha1 = (1/3) * (-f1 + f2)
    alpha3 = 1 - alpha1
    c = 1 - 2 * (alpha1 / (1 + (1 - alpha1) * (2 * C_l * f / C)))
    tau_app = 0.5 * (c * (1 - r3) + np.sqrt(c**2 * (1 - r3)**2 + 4 * r3))
    return tau_app, alpha1, np.zeros_like(alpha1), alpha3, np.zeros_like(alpha1)


def tetramer_equilibria(C4, KD1, KD2, f, C_l):
    C = np.atleast_1d(np.array(4 * C4, dtype=float))
    r1 = 0.79 * 0.79
    r2 = 0.79

    c1 = np.zeros(len(C))
    for i, Ctot in enumerate(C):
        pp = [4 / (KD2**2 * KD1), 0, 2 / KD2, 1, -Ctot]
        roots = np.roots(pp)
        valid = roots[(roots.real > 0) & (np.abs(roots.imag) < 1e-10)].real
        c1[i] = valid[0]

    c2 = c1**2 / KD2
    c4 = c2**2 / KD1

    alpha1 = c1       / C
    alpha2 = 2 * c2   / C
    alpha4 = 4 * c4   / C

    lf    = C_l * f / C
    denom = 1 + alpha2 * 1 * lf + alpha4 * 3 * lf
    a1 = alpha1                    / denom
    a2 = alpha2 * (1 +     lf)    / denom
    a3 = alpha4 * (1 + 3 * lf)    / denom

    b1 = r1 + r2 + 1
    b2 = a1 * r1 + a2 * r2 + a3
    b3 = r1 * r2 + r1 + r2
    b4 = a1 * r1 * (r2 + 1) + a2 * r2 * (r1 + 1) + a3 * (r2 + r1)
    b5 = r1 * r2

    tau_app = np.zeros(len(C))
    for i in range(len(C)):
        pp = [1, (b1 - 2 * b2[i]), (b3 - 2 * b4[i]), -b5]
        roots = np.roots(pp)
        valid = roots[(roots.real > 0) & (np.abs(roots.imag) < 1e-10)].real
        tau_app[i] = np.max(valid)

    return tau_app, alpha1, alpha2, np.zeros_like(alpha1), alpha4


def run_simulation(model, KD, f, C_l, c_min, c_max, KD2=None, N=200):
    C_total = np.logspace(np.log10(c_min), np.log10(c_max), N)

    if model == "Dimer":
        C2 = C_total / 2
        tau_app, fM, fD, fT3, fT4 = dimer_equilibria(C2, KD, f, C_l)
        species = {"Monomer": fM, "Dimer": fD}
    elif model == "Trimer":
        C3 = C_total / 3
        tau_app, fM, fD, fT3, fT4 = trimer_equilibria(C3, KD, f, C_l)
        species = {"Monomer": fM, "Trimer": fT3}
    else:  # Tetramer
        C4 = C_total / 4
        tau_app, fM, fD, fT3, fT4 = tetramer_equilibria(C4, KD, KD2, f, C_l)
        species = {"Monomer": fM, "Dimer": fD, "Tetramer": fT4}

    return C_total, tau_app, species


def make_figure(C, tau, species, model):
    species_colors = {
        "Monomer":  C_MONO,
        "Dimer":    C_DIMER,
        "Trimer":   C_TRIMER,
        "Tetramer": C_TETRA,
    }
    n_map = {"Dimer": 2, "Trimer": 3, "Tetramer": 4}
    n = n_map[model]

    with plt.rc_context(PLOT_RC):
        fig = plt.figure(figsize=(9, 7), facecolor="#f7f7f7")
        gs = fig.add_gridspec(
            2, 1,
            height_ratios=[1.15, 1],
            hspace=0.55,
            top=0.90,
            bottom=0.09,
            left=0.10,
            right=0.95,
        )
        ax_tau  = fig.add_subplot(gs[0])
        ax_frac = fig.add_subplot(gs[1])

        def style_ax(ax):
            ax.set_facecolor("#ffffff")
            ax.tick_params(labelsize=9)
            for sp in ax.spines.values():
                sp.set_color("#cccccc")
                sp.set_linewidth(0.8)
            ax.grid(True, color="#eeeeee", linewidth=0.5, linestyle="--")

        # ── tau panel ─────────────────────────────────────────────────────────
        style_ax(ax_tau)
        ax_tau.plot(C, tau, color=C_TAU, linewidth=2.2,
                    solid_capstyle="round", label=r"$\tau_\mathrm{app}$")
        ax_tau.set_xscale("log")
        ax_tau.set_xlim(C[0], C[-1])
        ax_tau.set_xlabel("Protein Concentration (nM)", color="#444444",
                           fontsize=9, labelpad=4)
        ax_tau.tick_params(axis="x", colors="#444444", labelsize=8)
        ax_tau.xaxis.set_major_formatter(
            ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax_tau.set_ylabel(
            r"Normalized $\tau$  ($\tau_\mathrm{app}\ /\ \tau_\mathrm{D}$)",
            fontsize=9, labelpad=6)
        ax_tau.set_title(f"{model} Equilibrium", fontsize=10,
                          fontweight="bold", color="#1a1a1a", loc="center", pad=6)
        tau_lo = max(0.0, tau.min() - 0.05)
        ax_tau.set_ylim(tau_lo, 1.05)

        # Top twin axis — oligomer concentration
        ax2x = ax_tau.twiny()
        ax2x.set_xscale("log")
        ax2x.set_xlim(C[0], C[-1])

        log_lo = int(np.floor(np.log10(C[0])))
        log_hi = int(np.ceil(np.log10(C[-1])))
        base_ticks = [10**e for e in range(log_lo, log_hi + 1)
                      if C[0] <= 10**e <= C[-1]]
        ax2x.set_xticks(base_ticks)
        ax2x.set_xticklabels([f"{v * n:g}" for v in base_ticks])
        ax2x.set_xlabel(r"$C_0$ nM (total monomer conc)",
                         color="#cc79a7", fontsize=9, labelpad=4)
        ax2x.tick_params(axis="x", colors="#cc79a7", labelsize=8)
        ax2x.spines["top"].set_color("#cc79a7")
        ax2x.spines["top"].set_linewidth(1.2)
        for sp_name in ("bottom", "left", "right"):
            ax2x.spines[sp_name].set_color("#cccccc")
            ax2x.spines[sp_name].set_linewidth(0.8)

        # ── fraction panel ────────────────────────────────────────────────────
        style_ax(ax_frac)
        for name, frac in species.items():
            col = species_colors.get(name, "#444444")
            ax_frac.plot(C, frac, color=col, linewidth=1.8,
                         label=name, solid_capstyle="round")
        ax_frac.set_xscale("log")
        ax_frac.set_xlim(C[0], C[-1])
        ax_frac.set_xlabel("Protein Concentration (nM)", fontsize=9, labelpad=4)
        ax_frac.tick_params(axis="x", labelsize=8)
        ax_frac.xaxis.set_major_formatter(
            ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax_frac.set_ylabel("Fractional concentration  α", fontsize=9, labelpad=6)
        ax_frac.set_ylim(-0.02, 1.05)
        ax_frac.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax_frac.legend(loc="center right", framealpha=0.9, fontsize=9)

    return fig


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔬 FCS Oligomerization Simulator")
    st.caption("FCS oligomerization model")
    st.divider()

    st.markdown("**Equilibrium type**")
    model_label = st.selectbox(
        "Model",
        ["Dimer ⇌ Monomer", "Trimer ⇌ Monomer", "Tetramer ⇌ Dimer ⇌ Monomer"],
        label_visibility="collapsed",
    )
    model = model_label.split(" ")[0]  # "Dimer", "Trimer", or "Tetramer"

    st.divider()
    st.markdown("**Model parameters**")

    if model == "Tetramer":
        KD1 = st.number_input(
            "Kd1 — dimer→tetramer (nM)",
            min_value=1e-6, max_value=1e9, value=100.0, step=10.0, format="%.4g"
        )
        KD2 = st.number_input(
            "Kd2 — monomer→dimer (nM)",
            min_value=1e-6, max_value=1e9, value=500.0, step=10.0, format="%.4g"
        )
    else:
        KD1 = st.number_input(
            "Kd (nM)",
            min_value=1e-6, max_value=1e9, value=100.0, step=10.0, format="%.4g"
        )
        KD2 = None

    f = st.slider("Labelling efficiency  f", min_value=0.0, max_value=1.0,
                  value=0.5, step=0.01)

    C_l = st.number_input(
        "Labeled concentration CL (nM)",
        min_value=0.0, max_value=1e6, value=1.0, step=0.1, format="%.4g"
    )

    st.divider()
    st.markdown("**Concentration range (nM)**")
    col_lo, col_hi = st.columns(2)
    with col_lo:
        c_min = st.number_input("Min", min_value=1e-6, max_value=1e6,
                                 value=1.0, step=1.0, format="%.4g")
    with col_hi:
        c_max = st.number_input("Max", min_value=1e-6, max_value=1e9,
                                 value=1000.0, step=100.0, format="%.4g")

    st.divider()
    run_btn = st.button("▶  Run simulation", use_container_width=True)


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown("## FCS Oligomerization Simulator")
st.caption("Apparent diffusion time and fractional species concentrations")

# Validate inputs
errors = []
if c_min >= c_max:
    errors.append("'C min' must be less than 'C max'.")
if c_min <= 0:
    errors.append("'C min' must be > 0.")
if KD1 <= 0:
    errors.append("Kd must be > 0.")
if model == "Tetramer" and KD2 <= 0:
    errors.append("Kd2 must be > 0.")

if errors:
    for e in errors:
        st.error(e)
    st.stop()

# Auto-run on first load OR when button pressed
if run_btn or "last_result" not in st.session_state:
    with st.spinner("Running simulation…"):
        try:
            C, tau, species = run_simulation(
                model=model,
                KD=KD1,
                f=f,
                C_l=C_l,
                c_min=c_min,
                c_max=c_max,
                KD2=KD2,
            )
            st.session_state["last_result"] = {
                "C": C, "tau": tau, "species": species,
                "model": model, "KD": KD1, "KD2": KD2,
                "f": f, "C_l": C_l,
            }
        except Exception as exc:
            st.error(f"Simulation error: {exc}")
            st.stop()

res = st.session_state["last_result"]
C, tau, species = res["C"], res["tau"], res["species"]

# ── Summary metrics ────────────────────────────────────────────────────────────
tau_min  = float(tau.min())
tau_range = float(tau.max() - tau.min())

# Crossover concentration: where monomer fraction ≈ 0.5
mono = species.get("Monomer", np.ones_like(C))
idx_cross = int(np.argmin(np.abs(mono - 0.5)))
c_cross = float(C[idx_cross])

m1, m2, m3 = st.columns(3)
m1.metric("τ_app at C_min", f"{tau[0]:.3f}", help="Normalized diffusion time at lowest concentration")
m2.metric("τ_app at C_max", f"{tau[-1]:.3f}", help="Normalized diffusion time at highest concentration")
m3.metric("~50 % oligomer at", f"{c_cross:.1f} nM",
          help="Concentration where monomer fraction ≈ 0.5")

# ── Plot ───────────────────────────────────────────────────────────────────────
fig = make_figure(C, tau, species, res["model"])
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# ── Data table (expandable) ────────────────────────────────────────────────────
with st.expander("📄  Show raw data table"):
    import pandas as pd
    df_data = {"Concentration (nM)": C, "tau_app": tau}
    df_data.update(species)
    df = pd.DataFrame(df_data)
    st.dataframe(df.style.format("{:.5g}"), use_container_width=True, height=300)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇  Download CSV",
        data=csv,
        file_name=f"fcs_{res['model'].lower()}_simulation.csv",
        mime="text/csv",
    )