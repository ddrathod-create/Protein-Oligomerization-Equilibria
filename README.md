# 🔬 Protein Oligomerization Simulator

An interactive web tool for simulating fluorescence correlation spectroscopy (FCS) titration curves for three oligomerization equilibria: monomer–dimer, monomer–trimer, and monomer–dimer–tetramer.

> *This tool is intended to facilitate the implementation of quantitative FCS-based oligomerization studies and to promote the use of physically accurate binding models over empirical approximations that may result in inaccurate or misleading parameter estimates.*

---

## Overview

FCS measures fluorescence intensity fluctuations as labeled molecules diffuse through a femtoliter-sized confocal observation volume. The temporal behavior of these fluctuations, captured by the autocorrelation function, encodes the translational diffusion coefficients of the fluorescent species in the sample. Since the diffusion coefficient of a globular protein scales approximately with the cube root of its molecular mass, FCS can, in principle, distinguish between oligomeric states and report on the degree of dissociation as a function of concentration.
 
A key complication is that the autocorrelation decay of a mixture of oligomeric species is experimentally indistinguishable from that of a single species. The measured quantity is therefore an apparent diffusion time (τₐₚₚ) that reflects the weighted average of all species present, where the weighting depends on both the concentrations and relative brightnesses of each species. Because larger oligomers carry more fluorescent labels and contribute more strongly to the autocorrelation signal, simple intuitive interpretations of τₐₚₚ can be seriously misleading without a proper mathematical framework.
 
This tool is based on a rigorous mathematical treatment that establishes analytical relationships between the experimentally measured τₐₚₚ values and the thermodynamic parameters governing protein oligomerization, including dissociation equilibrium constants for three different oligomerization cases: dimer-monomer, trimer-monomer and tetramer-dimer-monomer [1,2]. It computes the predicted **normalized apparent diffusion time** τₙ = τₐₚₚ / τₘ as a function of total protein concentration, given user-specified dissociation constants (Kd) and experimental parameters, where τₘ is the diffusion time of the intact oligomeric species of stoichiometry m.

---

## Original Code

This webapp is based on the `proteinequilibriafn.py` file, maintaining all the original functionality while adding an interactive web interface.

---

## Equilibria Cases

**Dimer-Monomer**

```
D ⇌ 2M        (Kd)
```

**Trimer-Monomer**

```
T ⇌ 3M        (Kd)
```

**Tetramer-Dimer-Monomer**

```
T₄ ⇌ 2D ⇌ 4M        (Kd1 for T₄→D , Kd2 for D→M )
```

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| Kd | Dissociation constant for the monomer–oligomer equilibrium (nM); for the trimer case this is an effective Kd in nM units|
| Kd1 | Dissociation constant for the dimer-to-tetramer step (nM) |
| Kd2 | Dissociation constant for the monomer-to-dimer step (nM) |
| *f* | Labeling efficiency (fraction of molecules carrying a fluorescent label) |
| CL | Concentration of labeled protein in terms of the highest oligomer (nM) |
| Conc. range | Total protein concentration in terms of the highest oligomer range for the simulation (nM) |

The tool outputs:
- **Upper panel:** τₐₚₚ / τₘ vs. protein concentration (log scale), with a secondary *x*-axis showing total monomer concentration
- **Lower panel:** Fractional species concentrations vs. protein concentration
- **CSV download:** All plotted values in a .csv file 

---
 
## Installation
 
**1. Install dependencies**
```bash
pip install streamlit numpy matplotlib pandas
```
 
**2. Run the app**
```bash
streamlit run simulationforproteinequilibria.py
```
 
The app will open automatically in your browser at `http://localhost:8501`.
  
---

## Usage

1. Select an **equilibrium model** from the sidebar dropdown.
2. Enter the dissociation constant(s) and experimental parameters (*f*, CL).
3. Set the **concentration range** to match the span of your titration experiment.
4. Click **Run Simulation** to update the plots.
5. Use **Download CSV** to export the simulated curves.

> **Tip:** The plots auto-refresh when you switch equilibrium models. For all other parameter changes, click *Run Simulation* to apply.

---

## References

1. Kanno, D. M., & Levitus, M. (2014). Protein oligomerization equilibria and kinetics investigated
   by fluorescence correlation spectroscopy: A mathematical treatment.
   *The Journal of Physical Chemistry B*, 118(43), 12404–12415. https://doi.org/10.1021/jp507741r

2. **[Author(s), Title, Journal, Year, DOI: placeholder]**

---

## Citation

If you use this tool in your work, please cite reference [2] above.

---

## License

[MIT / GPLv3 / other: add your license here]
