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

### Research Objective & Time-Dependency
Because the transition from the unstable dihydrate phase to the stable anhydrous phase is a **function of time**, comparing the fresh mixture (Sample 2) with the aged mixture (Sample 3) allows us to monitor and characterize the phase transformation process.

### Micro-Raman Spectroscopy Workflow
To differentiate between the co-existing phases within the mixed samples, **Micro-Raman Spectroscopy** was utilized:
1. **Spectral Acquisition:** A focused laser was fired at the exact same crystal to acquire its distinct Raman spectrum (Raman Shift vs. Intensity).
2. **Microscopy Imaging:** A high-resolution digital photograph was captured for each targeted crystal to document its visual appearance.


### Project Goal
The primary objective of this software platform is to provide an intuitive and comprehensive analytical tool for processing and visualizing Raman spectra corresponding to Uric Acid polymorphs (Anhydrous and Dihydrate). To facilitate advanced spectral interpretation, the application offers versatile display configurations, enabling researchers to seamlessly alternate between an overlay view for relative intensity comparison and a vertically offset stacked view for isolated sample inspection. Furthermore, the platform integrates dynamic feature analysis, allowing users to define and crop specific Raman shift windows (wavenumber ranges) to focus on critical regions, select and toggle the visibility of individual active plots during live analysis, and instantly pinpoint the exact Raman shift values of major spectral peaks while interactively regulating the threshold of displayed peaks. By pairing these robust spectral manipulation utilities with an automated cross-referencing feature that displays the linked microscopic crystal morphology (.jpg) of any selected spectrum, the software automates the tracking of polymorphic identities and transformations within a single unified workspace.

### How to Run the Code (in Terminal)?

```
python main.py
```
