## 🔬 Scientific Background & Purpose

This project focuses on the solid-state phase transitions of **Uric Acid**.

### The Samples & Thermodynamic Phases
Uric acid primarily exists in two crystalline phases:
1. **Anhydrous Uric Acid:** The thermodynamically stable phase under ambient conditions.
2. **Uric Acid Dihydrate:** A metastable phase that tends to transform into the anhydrous form over time.

In this study, a dataset of 3 distinct sample groups was analyzed:
* **Sample 1 (100% Anhydrous):** A pure control sample whose phase was fully verified via Powder X-ray Diffraction (PXRD).
* **Sample 2 (Fresh Mixture):** A newly prepared sample on the day of the Raman analysis. PXRD confirmed it contains a mixture of both Anhydrous and Dihydrate phases.
* **Sample 3 (Aged Mixture):** A sample prepared several days prior to the analysis. PXRD also confirmed a mixture of both phases.

### Project Objective & Context
The primary objective of this software platform is to provide an intuitive, comprehensive, and interactive analytical tool for processing and visualizing Raman spectra corresponding to Uric Acid polymorphs. Because the thermodynamic transition from the unstable dihydrate phase to the stable anhydrous phase is a dynamic function of time, comparing fresh and aged chemical mixtures allows researchers to actively monitor and characterize the phase transformation process.

To facilitate this spectral interpretation, the application offers an advanced workspace where users can seamlessly alternate between an overlay view for relative intensity comparison and a vertically offset stacked view for isolated sample inspection. Furthermore, the platform integrates dynamic analysis features, allowing users to define and crop specific Raman shift windows (wavenumber ranges) to focus on critical chemical regions, toggle the visibility of individual active plots during live analysis, and instantly pinpoint the exact Raman shift values of major spectral peaks while interactively regulating the peak threshold display. By pairing these robust spectral manipulation utilities with an automated cross-referencing feature that displays the linked microscopic crystal morphology (.jpg) of any selected spectrum, the software streamlines and automates the tracking of polymorphic identities and transformations within a single unified platform.


### How to Run the Code (in Terminal)?

```
python main.py
```
