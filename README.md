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
1. **Optical Visual Inspection:** Using the integrated optical microscope of the Raman system, specific individual crystals were targeted based on their morphology.
2. **Microscopy Imaging:** A high-resolution digital photograph was captured for each targeted crystal to document its visual appearance.
3. **Spectral Acquisition:** A focused laser was fired at the exact same crystal to acquire its distinct Raman spectrum (Raman Shift vs. Intensity).

### Project Goal
By linking the visual crystal morphology (images) with their corresponding vibrational fingerprints (Raman spectra), this software helps researchers visually and spectrally map out which crystals are Anhydrous and which are Dihydrate, making the tracking of polymorphic transformations immediate and automated.

### Instructions on How to Run the Code

To execute the Raman spectroscopy and crystal imaging application locally, first verify that all necessary visualization and data processing modules are installed by running pip install numpy pandas matplotlib pillow in your terminal environment. Once the framework dependencies are successfully provisioned, navigate to the project root directory where your dataset and code reside, and initiate the main execution interface by running the command python main.py. Upon initialization, the graphical user interface (GUI) will launch, allowing you to load and navigate through the spectral data text files to plot the respective Raman spectrum dynamically. To view the physical structural properties of the analyzed sample, simply select the desired spectrum and click the designated display button within the interface to instantly render and map the corresponding high-resolution crystal microscope image (.jpg).
