# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:27:19 2026

@author: Dhanashri
"""
"""
FCS Oligomerization Simulator — Streamlit version
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

C_TAU    = "#000000"
C_MONO   = "#0072b2"
C_DIMER  = "#e69f00"
C_TRIMER = "#cc79a7"
C_TETRA  = "#009e73"

PLOT_RC = {
    "axes.facecolor":   "#ffffff",
    "figure.facecolor": "#ffffff",
    "axes.edgecolor":   "#cccccc",
    "axes.labelcolor":  "#333333",
    "axes.grid":        True,
    "grid.color":       "#f0f0f0",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.5,
    "xtick.color":      "#555555",
    "ytick.color":      "#555555",
    "text.color":       "#222222",
    "legend.facecolor": "#ffffff",
    "legend.edgecolor": "#eeeeee",
    "legend.fontsize":  9,
    "font.size":        10,
    "axes.titlesize":   11,
    "axes.labelsize":   10,
}

st.markdown("""
<style>
/* ── Global light theme ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: #f8f8f6 !important;
    color: #1a1a1a !important;
}

/* Fix header so top-right icons (Share, ⋮) are visible */
[data-testid="stHeader"] {
    background-color: #f8f8f6 !important;
    border-bottom: 1px solid #e0e0e0 !important;
}
[data-testid="stHeader"] * {
    color: #1a1a1a !important;
}
[data-testid="stHeader"] button,
[data-testid="stHeader"] svg,
[data-testid="stHeader"] svg path {
    color: #333333 !important;
    fill: #333333 !important;
    stroke: #333333 !important;
}
[data-testid="stToolbar"] {
    color: #333333 !important;
}
[data-testid="stToolbar"] button {
    color: #333333 !important;
}
[data-testid="stToolbar"] svg path {
    fill: #333333 !important;
}

.main .block-container {
    background-color: #f8f8f6 !important;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 960px;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #1e1e1e !important;
    border-right: 1px solid #333 !important;
}
section[data-testid="stSidebar"] * {
    color: #e8e8e8 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #3a3a3a !important;
    margin: 12px 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 2px !important;
}
section[data-testid="stSidebar"] .stMarkdown { margin-bottom: 0 !important; }

/* Add breathing room between sidebar input groups */
section[data-testid="stSidebar"] .stSelectbox  { margin-bottom: 6px !important; }
section[data-testid="stSidebar"] .stNumberInput { margin-bottom: 8px !important; }
section[data-testid="stSidebar"] .stSlider      { margin-bottom: 8px !important; }

/* Sidebar section headers */
.sidebar-section-label {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888888 !important;
    font-weight: 600;
    margin-bottom: 6px;
    margin-top: 4px;
    display: block;
}

/* Sidebar inputs on dark bg */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: #2d2d2d !important;
    color: #e8e8e8 !important;
    border: 1px solid #444 !important;
    border-radius: 5px !important;
}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background-color: #2d2d2d !important;
    color: #e8e8e8 !important;
    border: 1px solid #444 !important;
}
/* Number input stepper buttons */
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background-color: #3a3a3a !important;
    border: none !important;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button *,
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button svg,
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button svg path {
    color: #ffffff !important;
    fill: #ffffff !important;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover {
    background-color: #555 !important;
}
/* Slider track labels */
section[data-testid="stSidebar"] [data-testid="stSlider"] p,
section[data-testid="stSidebar"] [data-testid="stSlider"] label,
section[data-testid="stSidebar"] [data-testid="stSlider"] span {
    color: #e8e8e8 !important;
}

/* ── Dropdown popup ── */
[data-baseweb="popover"], [data-baseweb="popover"] *,
[data-baseweb="menu"], [data-baseweb="menu"] *,
li[role="option"], li[role="option"] * {
    background-color: #2d2d2d !important;
    color: #e8e8e8 !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #0072b2 !important;
    color: #ffffff !important;
}

/* ── Run button ── */
div.stButton > button {
    width: 100%;
    background-color: #0072b2 !important;
    color: #ffffff !important;
    font-weight: 600;
    border-radius: 6px;
    padding: 0.55rem;
    border: none !important;
    font-size: 0.9rem;
    letter-spacing: 0.03em;
    margin-top: 10px;
    transition: background 0.15s;
}
div.stButton > button:hover  { background-color: #005a8e !important; }
div.stButton > button:active { background-color: #004470 !important; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background-color: transparent !important;
    color: #0072b2 !important;
    font-weight: 500;
    border: 1.5px solid #0072b2 !important;
    border-radius: 6px;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    margin-top: 6px;
}
[data-testid="stDownloadButton"] > button:hover {
    background-color: #0072b2 !important;
    color: #ffffff !important;
}

/* ── Page header ── */
.page-header {
    margin-bottom: 1.6rem;
}
.page-title {
    font-size: 1.55rem;
    font-weight: 700;
    color: #111111 !important;
    letter-spacing: -0.01em;
    line-height: 1.25;
    margin-bottom: 4px;
}
.page-byline {
    font-size: 0.72rem;
    color: #999999 !important;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 0.92rem;
    color: #777777 !important;
    font-style: italic;
    margin-bottom: 0;
    font-weight: 400;
}

/* ── Main area text ── */
p, span, label, div, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stCaption,
[data-testid="stMarkdownContainer"] {
    color: #1a1a1a !important;
}

/* Hide the docstring from showing up */
[data-testid="stText"] { display: none; }

/* ── Spinner ── */
[data-testid="stSpinner"] * { color: #0072b2 !important; }

/* ── Plot container spacing ── */
[data-testid="stImage"], .stPyplot {
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
}
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
        "Monomer":  C_MONO,
        "Dimer":    C_DIMER,
        "Trimer":   C_TRIMER,
        "Tetramer": C_TETRA,
    }
    n_map = {"Dimer": 2, "Trimer": 3, "Tetramer": 4}
    n = n_map[model]

    with plt.rc_context(PLOT_RC):
        fig = plt.figure(figsize=(8.5, 6.5), facecolor="#ffffff")
        gs = fig.add_gridspec(
            2, 1, height_ratios=[1.15, 1],
            hspace=0.58, top=0.88, bottom=0.10, left=0.11, right=0.96,
        )
        ax_tau  = fig.add_subplot(gs[0])
        ax_frac = fig.add_subplot(gs[1])

        def style_ax(ax):
            ax.set_facecolor("#ffffff")
            ax.tick_params(labelsize=9)
            for sp in ax.spines.values():
                sp.set_color("#dddddd")
                sp.set_linewidth(0.8)
            ax.grid(True, color="#f2f2f2", linewidth=0.6, linestyle="--")

        # tau panel
        style_ax(ax_tau)
        ax_tau.plot(C, tau, color="#111111", linewidth=2.0, solid_capstyle="round")
        ax_tau.set_xscale("log")
        ax_tau.set_xlim(C[0], C[-1])
        ax_tau.set_xlabel("Protein Concentration (nM)", color="#555", fontsize=9, labelpad=4)
        ax_tau.tick_params(axis="x", colors="#555", labelsize=8)
        ax_tau.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax_tau.set_ylabel(r"$\tau_\mathrm{app}\ /\ \tau_\mathrm{D}$", fontsize=9, labelpad=6)
        tau_lo = max(0.0, tau.min() - 0.05)
        ax_tau.set_ylim(tau_lo, 1.05)

        # twin top axis
        ax2x = ax_tau.twiny()
        ax2x.set_xscale("log")
        ax2x.set_xlim(C[0], C[-1])
        log_lo = int(np.floor(np.log10(C[0])))
        log_hi = int(np.ceil(np.log10(C[-1])))
        base_ticks = [10**e for e in range(log_lo, log_hi + 1) if C[0] <= 10**e <= C[-1]]
        ax2x.set_xticks(base_ticks)
        ax2x.set_xticklabels([f"{v * n:g}" for v in base_ticks])
        ax2x.set_xlabel(r"$C_0$ (total monomer, nM)", color="#aa6699", fontsize=8.5, labelpad=4)
        ax2x.tick_params(axis="x", colors="#aa6699", labelsize=8)
        ax2x.spines["top"].set_color("#aa6699")
        ax2x.spines["top"].set_linewidth(1.0)
        for sp_name in ("bottom", "left", "right"):
            ax2x.spines[sp_name].set_color("#dddddd")
            ax2x.spines[sp_name].set_linewidth(0.8)

        # fraction panel
        style_ax(ax_frac)
        for name, frac in species.items():
            ax_frac.plot(C, frac, color=species_colors.get(name, "#444"),
                         linewidth=1.8, label=name, solid_capstyle="round")
        ax_frac.set_xscale("log")
        ax_frac.set_xlim(C[0], C[-1])
        ax_frac.set_xlabel("Protein Concentration (nM)", fontsize=9, labelpad=4, color="#555")
        ax_frac.tick_params(axis="x", labelsize=8, colors="#555")
        ax_frac.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax_frac.set_ylabel("Fractional concentration  α", fontsize=9, labelpad=6)
        ax_frac.set_ylim(-0.02, 1.05)
        ax_frac.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax_frac.legend(loc="center right", framealpha=0.9, fontsize=9,
                       edgecolor="#eeeeee")

    return fig


# ── Sidebar ────────────────────────────────────────────────────────────────────
EQ_LABELS = {
    "Dimer":    "Dimer ⇌ Monomer",
    "Trimer":   "Trimer ⇌ Monomer",
    "Tetramer": "Tetramer ⇌ Dimer ⇌ Monomer",
}

with st.sidebar:
    st.markdown(
        "<div style='font-size:1.05rem; font-weight:700; color:#ffffff !important;"
        " letter-spacing:-0.01em; padding: 8px 0 3px 0;'>FCS Simulator</div>"
        "<div style='font-size:0.72rem; color:#999 !important; margin-bottom:10px;'>"
        "Oligomerization equilibria</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("<span class='sidebar-section-label'>Equilibrium model</span>",
                unsafe_allow_html=True)
    model_label = st.selectbox(
        "model", list(EQ_LABELS.values()), label_visibility="collapsed"
    )
    model = [k for k, v in EQ_LABELS.items() if v == model_label][0]

    st.divider()
    st.markdown("<span class='sidebar-section-label'>Model parameters</span>",
                unsafe_allow_html=True)

    if model == "Tetramer":
        # Use HTML labels with proper subscripts via markdown
        st.markdown(
            "<div style='font-size:0.85rem; color:#cccccc !important; margin-bottom:2px;'>"
            "K<sub>d1</sub> — dimer→tetramer (nM)</div>",
            unsafe_allow_html=True,
        )
        KD1 = st.number_input(
            "Kd1", label_visibility="collapsed",
            min_value=1e-6, max_value=1e9, value=100.0, step=10.0, format="%.4g"
        )
        st.markdown(
            "<div style='font-size:0.85rem; color:#cccccc !important; margin-bottom:2px;'>"
            "K<sub>d2</sub> — monomer→dimer (nM)</div>",
            unsafe_allow_html=True,
        )
        KD2 = st.number_input(
            "Kd2", label_visibility="collapsed",
            min_value=1e-6, max_value=1e9, value=500.0, step=10.0, format="%.4g"
        )
    else:
        st.markdown(
            "<div style='font-size:0.85rem; color:#cccccc !important; margin-bottom:2px;'>"
            "K<sub>d</sub> (nM)</div>",
            unsafe_allow_html=True,
        )
        KD1 = st.number_input(
            "Kd", label_visibility="collapsed",
            min_value=1e-6, max_value=1e9, value=100.0, step=10.0, format="%.4g"
        )
        KD2 = None

    f = st.slider("Labelling efficiency  f", 0.0, 1.0, 0.5, 0.01)

    st.markdown(
        "<div style='font-size:0.85rem; color:#cccccc !important; margin-bottom:2px;'>"
        "Labeled concentration C<sub>L</sub> (nM)</div>",
        unsafe_allow_html=True,
    )
    C_l = st.number_input(
        "CL", label_visibility="collapsed",
        min_value=0.0, max_value=1e6, value=1.0, step=0.1, format="%.4g"
    )

    st.divider()
    st.markdown("<span class='sidebar-section-label'>Protein concentration range (nM)</span>",
                unsafe_allow_html=True)
    col_lo, col_hi = st.columns(2)
    with col_lo:
        st.markdown(
            "<div style='font-size:0.78rem; color:#aaaaaa !important; margin-bottom:1px;'>Min</div>",
            unsafe_allow_html=True,
        )
        c_min = st.number_input(
            "Min", label_visibility="collapsed",
            min_value=1e-6, max_value=1e6, value=1.0, step=1.0, format="%.4g"
        )
    with col_hi:
        st.markdown(
            "<div style='font-size:0.78rem; color:#aaaaaa !important; margin-bottom:1px;'>Max</div>",
            unsafe_allow_html=True,
        )
        c_max = st.number_input(
            "Max", label_visibility="collapsed",
            min_value=1e-6, max_value=1e9, value=1000.0, step=100.0, format="%.4g"
        )

    st.divider()
    run_btn = st.button("▶  Run simulation", use_container_width=True)


# ── Main area ──────────────────────────────────────────────────────────────────
EQ_SUBTITLES = {
    "Dimer":    "Dimer ⇌ Monomer equilibrium",
    "Trimer":   "Trimer ⇌ Monomer equilibrium",
    "Tetramer": "Tetramer ⇌ Dimer ⇌ Monomer equilibrium",
}

st.markdown(
    "<div class='page-header'>"
    "<div class='page-title'>Protein Oligomerization Equilibria</div>"
    "<div class='page-byline'>by Fluorescence Correlation Spectroscopy</div>"
    f"<div class='page-subtitle'>{EQ_SUBTITLES.get(model, '')}</div>"
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
    for e in errors:
        st.error(e)
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

res = st.session_state["last_result"]
C, tau, species = res["C"], res["tau"], res["species"]

# Plot
fig = make_figure(C, tau, species, res["model"])
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# Download
df_data = {"Concentration (nM)": C, "tau_app": tau}
df_data.update(species)
df = pd.DataFrame(df_data)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇  Download data as CSV",
    data=csv,
    file_name=f"fcs_{res['model'].lower()}_simulation.csv",
    mime="text/csv",
)
