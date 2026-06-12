# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:27:19 2026

"""
"""
FCS Oligomerization Simulator 
"""

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

st.set_page_config(
    page_title="FCS Oligomerization Simulator",
    page_icon="🔬",
    layout="wide",
)

C_MONO   = "#0072b2"
C_DIMER  = "#e69f00"
C_TRIMER = "#cc79a7"
C_TETRA  = "#009e73"

PLOT_RC = {
    "axes.facecolor":   "#1a1a2e",
    "figure.facecolor": "#1a1a2e",
    "axes.edgecolor":   "#3a3a5c",
    "axes.labelcolor":  "#eeeeee",
    "axes.grid":        True,
    "grid.color":       "#2a2a4a",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.5,
    "xtick.color":      "#dddddd",
    "ytick.color":      "#dddddd",
    "text.color":       "#ffffff",
    "legend.facecolor": "#16213e",
    "legend.edgecolor": "#3a3a5c",
    "legend.fontsize":  9,
    "font.size":        10,
    "axes.titlesize":   11,
    "axes.labelsize":   10,
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

/* ── Full dark theme ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.main,
.main .block-container {
    background-color: #0f0f1a !important;
    color: #e0e0e0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 5rem;
    max-width: 1100px;
}

/* ── Header bar ── */
[data-testid="stHeader"],
header[data-testid="stHeader"] {
    background-color: #0f0f1a !important;
    border-bottom: 1px solid #2a2a3e !important;
}
[data-testid="stHeader"] *:not(span),
[data-testid="stToolbarActions"] *:not(span) {
    color: #ffffff !important;
}
[data-testid="stHeader"] svg path,
[data-testid="stHeader"] svg circle,
[data-testid="stHeader"] svg rect,
[data-testid="stHeader"] svg polygon,
[data-testid="stToolbarActions"] svg path,
[data-testid="stToolbarActions"] svg circle,
[data-testid="stToolbarActions"] svg rect,
[data-testid="stToolbarActions"] svg polygon {
    fill: #ffffff !important;
    stroke: none !important;
}
[data-testid="stToolbarActions"] button:hover svg path,
[data-testid="stToolbarActions"] button:hover svg circle {
    fill: #e040fb !important;
}

/* ── Hide sidebar collapse toggle (fixes "keyboard_double" text leak) ── */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
button[data-testid="stSidebarCollapsedControl"],
button[aria-label*="sidebar"],
button[aria-label*="Sidebar"],
button[aria-label*="Close sidebar"],
button[aria-label*="Open sidebar"],
button[aria-label*="collapse"],
button[aria-label*="Collapse"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
}

/* ── Hide deploy button (white square) only ── */
[data-testid="stAppDeployButton"],
[data-testid="stAppDeployButton"] *,
[data-testid="stDeployButton"],
[data-testid="stDeployButton"] * {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #16162a !important;
    border-right: 1px solid #2a2a3e !important;
    padding-top: 1rem !important;
}
section[data-testid="stSidebar"] *:not(span) {
    color: #e0e0e0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
section[data-testid="stSidebar"] span {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #2a2a3e !important;
    margin: 18px 0 !important;
}
section[data-testid="stSidebar"] .stMarkdown {
    margin-bottom: 6px !important;
}
section[data-testid="stSidebar"] .stSelectbox  { margin-bottom: 18px !important; }
section[data-testid="stSidebar"] .stNumberInput { margin-bottom: 18px !important; }


/* Sidebar inputs */
section[data-testid="stSidebar"] input {
    background-color: #1e1e35 !important;
    color: #e0e0e0 !important;
    border: 1px solid #3a3a5c !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background-color: #1e1e35 !important;
    color: #e0e0e0 !important;
    border: 1px solid #3a3a5c !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background-color: #2a2a45 !important;
    border: none !important;
    border-radius: 4px !important;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button svg,
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button svg path {
    fill: #ffffff !important;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover {
    background-color: #e040fb !important;
}


/* ── Dropdown popup ── */
[data-baseweb="popover"], [data-baseweb="popover"] *,
[data-baseweb="menu"], [data-baseweb="menu"] *,
li[role="option"], li[role="option"] * {
    background-color: #1e1e35 !important;
    color: #e0e0e0 !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #e040fb !important;
    color: #ffffff !important;
}

/* ── Sidebar section labels ── */
.sidebar-label {
    font-size: 0.95rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7070a0 !important;
    font-weight: 700;
    margin-bottom: 10px;
    margin-top: 2px;
    display: block;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.sidebar-input-label {
    font-size: 0.82rem;
    color: #b0b0cc !important;
    margin-bottom: 3px;
    display: block;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Run button ── */
div.stButton > button {
    width: 100%;
    background-color: #e040fb !important;
    color: #ffffff !important;
    font-weight: 600;
    border-radius: 8px !important;
    padding: 0.6rem !important;
    border: none !important;
    font-size: 0.9rem;
    letter-spacing: 0.04em;
    margin-top: 4px;
    transition: background 0.15s, transform 0.1s;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
div.stButton > button:hover  {
    background-color: #c020d0 !important;
    transform: translateY(-1px);
}
div.stButton > button:active { background-color: #9900aa !important; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background-color: transparent !important;
    color: #e040fb !important;
    font-weight: 500;
    border: 1.5px solid #e040fb !important;
    border-radius: 8px !important;
    padding: 0.4rem 1.2rem;
    font-size: 0.85rem;
    margin-top: 8px;
    transition: all 0.15s;
}
[data-testid="stDownloadButton"] > button:hover {
    background-color: #e040fb !important;
    color: #ffffff !important;
}

/* ── Page header ── */
.page-header {
    margin-bottom: 2rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #2a2a3e;
}
.page-icon {
    font-size: 2.2rem;
    margin-right: 0.5rem;
    vertical-align: middle;
}
.page-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff !important;
    letter-spacing: -0.02em;
    line-height: 1.15;
    display: inline;
    vertical-align: middle;
}
.page-subtitle {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.9rem;
    color: #7070a0 !important;
    margin-top: 6px;
    font-weight: 400;
}

/* ── Section headings in main area ── */
.section-heading {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: #ffffff !important;
    margin-top: 0.5rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #2a2a3e;
    text-align: center;
}

/* ── All text in main area ── */
p, label, div, h1, h2, h3, h4, h5, h6,
.stMarkdown, [data-testid="stMarkdownContainer"] {
    color: #e0e0e0 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] * { color: #e040fb !important; }

/* Hide docstring */
[data-testid="stText"] { display: none; }
</style>

""", unsafe_allow_html=True)


# ── Physics ─────────────────────────────────────────────────────────────────────
def dimer_equilibria(C2, KD, f, C_l):
    C = 2 * C2
    r2 = 0.79
    alpha1 = (1 / (C * 4)) * (-KD + np.sqrt(8 * C * KD + KD**2))
    alpha2 = 1 - alpha1
    c = 1 - 2 * (alpha1 / (1 + (1 - alpha1) * (C_l * f / C)))
    tau_app = 0.5 * (c * (1 - r2) + np.sqrt(c**2 * (1 - r2)**2 + 4 * r2))
    return tau_app, alpha1, alpha2, np.zeros_like(alpha1), np.zeros_like(alpha1)

def trimer_equilibria(C3, KDE, f, C_l):
    r3 = 0.69
    C = 3 * C3
    KD = (3/4)*KDE**2
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
    alpha1 = c1      / C
    alpha2 = 2 * c2  / C
    alpha4 = 4 * c4  / C
    lf    = C_l * f / C
    denom = 1 + alpha2 * lf + alpha4 * 3 * lf
    a1 = alpha1                  / denom
    a2 = alpha2 * (1 +     lf)  / denom
    a3 = alpha4 * (1 + 3 * lf)  / denom
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
        tau_app, fM, fD, fT3, fT4 = dimer_equilibria(C_total / 2, KD, f, C_l)
        species = {"Monomer": fM, "Dimer": fD}
    elif model == "Trimer":
        tau_app, fM, fD, fT3, fT4 = trimer_equilibria(C_total / 3, KD, f, C_l)
        species = {"Monomer": fM, "Trimer": fT3}
    else:
        tau_app, fM, fD, fT3, fT4 = tetramer_equilibria(C_total / 4, KD, KD2, f, C_l)
        species = {"Monomer": fM, "Dimer": fD, "Tetramer": fT4}
    return C_total, tau_app, species

def make_figure(C, tau, species, model):
    species_colors = {
        "Monomer":  "#56b4e9",
        "Dimer":    "#e69f00",
        "Trimer":   "#cc79a7",
        "Tetramer": "#009e73",
    }
    n_map = {"Dimer": 2, "Trimer": 3, "Tetramer": 4}
    n = n_map[model]

    with plt.rc_context(PLOT_RC):
        fig = plt.figure(figsize=(8.5, 6.5), facecolor="#1a1a2e")
        gs = fig.add_gridspec(
            2, 1, height_ratios=[1.15, 1],
            hspace=0.58, top=0.88, bottom=0.10, left=0.11, right=0.96,
        )
        ax_tau  = fig.add_subplot(gs[0])
        ax_frac = fig.add_subplot(gs[1])

        def style_ax(ax):
            ax.set_facecolor("#1a1a2e")
            ax.tick_params(labelsize=9)
            for sp in ax.spines.values():
                sp.set_color("#5a5a7c")
                sp.set_linewidth(0.8)
            ax.grid(True, color="#2a2a4a", linewidth=0.6, linestyle="--")

        # tau panel
        style_ax(ax_tau)
        ax_tau.plot(C, tau, color="#e040fb", linewidth=2.2, solid_capstyle="round")
        ax_tau.set_xscale("log")
        ax_tau.set_xlim(C[0], C[-1])
        ax_tau.set_xlabel("Protein Concentration (nM)", color="#ccccdd", fontsize=9, labelpad=4)
        ax_tau.tick_params(axis="x", colors="#ccccdd", labelsize=8)
        ax_tau.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        tau_subscript = {2: "2", 3: "3", 4: "4"}.get(n, "D")
        ax_tau.set_ylabel(rf"$\tau_\mathrm{{app}}\ /\ \tau_{{{tau_subscript}}}$", fontsize=9, labelpad=6, color="#eeeeee")
        tau_lo = max(0.0, tau.min() - 0.05)
        ax_tau.set_ylim(tau_lo, 1.05)
        ax_tau.tick_params(axis="y", colors="#ccccdd", labelsize=8)

        # twin top axis
        ax2x = ax_tau.twiny()
        ax2x.set_xscale("log")
        ax2x.set_xlim(C[0], C[-1])
        log_lo = int(np.floor(np.log10(C[0])))
        log_hi = int(np.ceil(np.log10(C[-1])))
        base_ticks = [10**e for e in range(log_lo, log_hi + 1) if C[0] <= 10**e <= C[-1]]
        ax2x.set_xticks(base_ticks)
        ax2x.set_xticklabels([f"{v * n:g}" for v in base_ticks])
        ax2x.set_xlabel(r"$C_0$ (total monomer, nM)", color="#d9a0f0", fontsize=8.5, labelpad=4)
        ax2x.tick_params(axis="x", colors="#d9a0f0", labelsize=8)
        ax2x.spines["top"].set_color("#d9a0f0")
        ax2x.spines["top"].set_linewidth(1.0)
        for sp_name in ("bottom", "left", "right"):
            ax2x.spines[sp_name].set_color("#5a5a7c")

        # fraction panel
        style_ax(ax_frac)
        for name, frac in species.items():
            ax_frac.plot(C, frac, color=species_colors.get(name, "#aaaaaa"),
                         linewidth=2.0, label=name, solid_capstyle="round")
        ax_frac.set_xscale("log")
        ax_frac.set_xlim(C[0], C[-1])
        ax_frac.set_xlabel("Protein Concentration (nM)", fontsize=9, labelpad=4, color="#ccccdd")
        ax_frac.tick_params(axis="x", labelsize=8, colors="#ccccdd")
        ax_frac.tick_params(axis="y", labelsize=8, colors="#ccccdd")
        ax_frac.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax_frac.set_ylabel("Fractional concentration  α", fontsize=9, labelpad=6, color="#eeeeee")
        ax_frac.set_ylim(-0.02, 1.05)
        ax_frac.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax_frac.legend(loc="center right", framealpha=0.85, fontsize=9,
                       edgecolor="#3a3a5c", labelcolor="#ffffff")

    return fig


# ── Sidebar ──────────────────────────────────────────────────────────────────────
EQ_LABELS = {
    "Dimer":    "Dimer ⇌ Monomer",
    "Trimer":   "Trimer ⇌ Monomer",
    "Tetramer": "Tetramer ⇌ Dimer ⇌ Monomer",
}

with st.sidebar:
    st.markdown(
        "<div style='font-size:1.1rem; font-weight:700; color:#ffffff !important;"
        " letter-spacing:-0.01em; padding:6px 0 2px 0; font-family:\"Source Serif 4\",serif;'>"
        "🔬 FCS Simulator</div>"
        "<div style='font-size:0.72rem; color:#7070a0 !important; margin-bottom:4px;"
        " letter-spacing:0.05em; font-family:\"Source Serif 4\",serif;'>"
        "Oligomerization equilibria</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("<span class='sidebar-label'>Equilibrium Model</span>", unsafe_allow_html=True)
    model_label = st.selectbox("model", list(EQ_LABELS.values()), label_visibility="collapsed")
    model = [k for k, v in EQ_LABELS.items() if v == model_label][0]

    st.divider()
    st.markdown("<span class='sidebar-label'>Model Parameters</span>", unsafe_allow_html=True)

    if model == "Tetramer":
        st.markdown(
            "<span class='sidebar-input-label'>K<sub>d1</sub> — dimer→tetramer (nM)</span>",
            unsafe_allow_html=True,
        )
        KD1 = st.number_input("Kd1", label_visibility="collapsed",
                               min_value=1e-6, max_value=1e9, value=100.0, step=10.0, format="%.4g")
        st.markdown(
            "<span class='sidebar-input-label'>K<sub>d2</sub> — monomer→dimer (nM)</span>",
            unsafe_allow_html=True,
        )
        KD2 = st.number_input("Kd2", label_visibility="collapsed",
                               min_value=1e-6, max_value=1e9, value=500.0, step=10.0, format="%.4g")
    else:
        st.markdown(
            "<span class='sidebar-input-label'>K<sub>d</sub> (nM)</span>",
            unsafe_allow_html=True,
        )
        KD1 = st.number_input("Kd", label_visibility="collapsed",
                               min_value=1e-6, max_value=1e9, value=100.0, step=10.0, format="%.4g")
        KD2 = None

    st.markdown(
        "<span class='sidebar-input-label'>Labelling efficiency f (0–1)</span>",
        unsafe_allow_html=True,
    )
    f = st.number_input("f", label_visibility="collapsed",
                        min_value=0.0, max_value=1.0, value=0.5, step=0.05, format="%.2f")

    st.markdown(
        "<span class='sidebar-input-label'>Labeled concentration C<sub>L</sub> (nM)</span>",
        unsafe_allow_html=True,
    )
    C_l = st.number_input("CL", label_visibility="collapsed",
                           min_value=0.0, max_value=1e6, value=1.0, step=0.1, format="%.4g")

    st.divider()
    st.markdown("<span class='sidebar-label'>Protein Concentration Range (<span style='text-transform:none;'>nM</span>)</span>",
                unsafe_allow_html=True)
    col_lo, col_hi = st.columns(2)
    with col_lo:
        st.markdown("<span class='sidebar-input-label'>Min</span>", unsafe_allow_html=True)
        c_min = st.number_input("Min", label_visibility="collapsed",
                                 min_value=1e-6, max_value=1e6, value=1.0, step=1.0, format="%.4g")
    with col_hi:
        st.markdown("<span class='sidebar-input-label'>Max</span>", unsafe_allow_html=True)
        c_max = st.number_input("Max", label_visibility="collapsed",
                                 min_value=1e-6, max_value=1e9, value=1000.0, step=100.0, format="%.4g")

    st.divider()
    run_btn = st.button("▶  Run Simulation", use_container_width=True)


# ── Main area ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='page-header'>"
    "<span class='page-icon'>🔬</span>"
    "<span class='page-title'>FCS Oligomerization Simulator</span>"
    "</div>",
    unsafe_allow_html=True,
)

# Validate
errors = []
if c_min >= c_max:   errors.append("'C min' must be less than 'C max'.")
if c_min <= 0:       errors.append("'C min' must be > 0.")
if KD1   <= 0:       errors.append("Kd must be > 0.")
if model == "Tetramer" and KD2 <= 0:
    errors.append("Kd2 must be > 0.")
if errors:
    for e in errors: st.error(e)
    st.stop()

# Run
if run_btn or "last_result" not in st.session_state:
    with st.spinner("Running simulation…"):
        try:
            C, tau, species = run_simulation(
                model=model, KD=KD1, f=f, C_l=C_l,
                c_min=c_min, c_max=c_max, KD2=KD2,
            )
            st.session_state["last_result"] = dict(
                C=C, tau=tau, species=species,
                model=model, KD=KD1, KD2=KD2, f=f, C_l=C_l,
            )
        except Exception as exc:
            st.error(f"Simulation error: {exc}")
            st.stop()

if "last_result" not in st.session_state:
    st.stop()

res = st.session_state["last_result"]
C, tau, species = res["C"], res["tau"], res["species"]

# Section heading — sourced from last_result so it only appears after Run is pressed
st.markdown(f"<div class='section-heading'>{EQ_LABELS[res['model']]}</div>", unsafe_allow_html=True)

fig = make_figure(C, tau, species, res["model"])
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# Download
df_data = {"Concentration (nM)": C, "tau_app": tau}
df_data.update(species)
df = pd.DataFrame(df_data)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇  Download CSV",
    data=csv,
    file_name=f"fcs_{res['model'].lower()}_simulation.csv",
    mime="text/csv",
)
