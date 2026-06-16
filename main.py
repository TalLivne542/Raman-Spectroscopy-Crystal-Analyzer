import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class RamanCrystalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Raman Spectroscopy & Crystal Imaging Platform")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f5f5f5")
        
        # Structure to hold multiple loaded datasets: { pure_name: (dataframe, img_path) }
        self.loaded_samples = {}
        
        # ------------------ GUI Layout Construction ------------------
        
        # Left sidebar control panel
        self.control_frame = tk.Frame(root, width=300, bg="#e0e0e0", padx=15, pady=15, bd=2, relief=tk.GROOVE)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Control panel title header
        self.lbl_title = tk.Label(self.control_frame, text="Control Panel", font=("Arial", 14, "bold"), bg="#e0e0e0")
        self.lbl_title.pack(pady=(0, 15))
        
        # Button to load a Raman spectrum file
        self.btn_load = tk.Button(self.control_frame, text="➕ Load Raman Spectrum (TXT)", command=self.load_spectrum, 
                                  font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=28, height=2, bd=3)
        self.btn_load.pack(pady=5)
        
        # Button to display the crystal image of the selected sample
        self.btn_show_img = tk.Button(self.control_frame, text="📷 Show Selected Crystal Image", command=self.show_crystal_image, 
                                      font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=28, height=2, bd=3, state=tk.DISABLED)
        self.btn_show_img.pack(pady=5)
        
        # Button to clear all loaded samples
        self.btn_clear = tk.Button(self.control_frame, text="🗑️ Clear All Spectra", command=self.clear_all, 
                                   font=("Arial", 9, "bold"), bg="#f44336", fg="white", width=28, height=1, bd=2)
        self.btn_clear.pack(pady=5)
        
        # --- Section: Display Mode Selection ---
        self.mode_frame = tk.LabelFrame(self.control_frame, text="Display Configuration", font=("Arial", 10, "bold"), bg="#e0e0e0", padx=5, pady=5)
        self.mode_frame.pack(pady=15, fill=tk.X)
        
        self.plot_mode = tk.StringVar(value="overlay")
        tk.Radiobutton(self.mode_frame, text="Overlay (Same Y-Axis)", variable=self.plot_mode, value="overlay", 
                       bg="#e0e0e0", font=("Arial", 9), command=self.replot_data).pack(anchor=tk.W, pady=2)
        tk.Radiobutton(self.mode_frame, text="Stacked (Y-Offset Separation)", variable=self.plot_mode, value="stacked", 
                       bg="#e0e0e0", font=("Arial", 9), command=self.replot_data).pack(anchor=tk.W, pady=2)
        
        # --- Section: Wavenumber Range Crop/Zoom ---
        self.range_frame = tk.LabelFrame(self.control_frame, text="Wavenumber Range (X-Axis Crop)", font=("Arial", 10, "bold"), bg="#e0e0e0", padx=5, pady=5)
        self.range_frame.pack(pady=15, fill=tk.X)
        
        tk.Label(self.range_frame, text="Min X (cm⁻¹):", bg="#e0e0e0", font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W, padx=2, pady=5)
        self.entry_min_x = tk.Entry(self.range_frame, width=8, font=("Arial", 9))
        self.entry_min_x.grid(row=0, column=1, padx=2, pady=5)
        
        tk.Label(self.range_frame, text="Max X (cm⁻¹):", bg="#e0e0e0", font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W, padx=2, pady=5)
        self.entry_max_x = tk.Entry(self.range_frame, width=8, font=("Arial", 9))
        self.entry_max_x.grid(row=1, column=1, padx=2, pady=5)
        
        self.btn_apply_range = tk.Button(self.range_frame, text="Apply Range Filter", command=self.replot_data, font=("Arial", 9, "bold"), bg="#9C27B0", fg="white")
        self.btn_apply_range.grid(row=2, column=0, columnspan=2, pady=8, sticky=tk.EW)
        
        # --- Section: Loaded Samples Listbox ---
        self.list_frame = tk.LabelFrame(self.control_frame, text="Active Samples Pool", font=("Arial", 10, "bold"), bg="#e0e0e0", padx=5, pady=5)
        self.list_frame.pack(pady=15, fill=tk.BOTH, expand=True)
        
        self.samples_listbox = tk.Listbox(self.list_frame, font=("Arial", 9), selectmode=tk.SINGLE)
        self.samples_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.samples_listbox.bind('<<ListboxSelect>>', self.on_sample_selected)
        
        scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.samples_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.samples_listbox.config(yscrollcommand=scrollbar.set)
        
        # Right workspace panel for embedding the Matplotlib graph canvas
        self.plot_frame = tk.Frame(root, bg="white", bd=2, relief=tk.SUNKEN)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initializing the Matplotlib figure and embedding it into Tkinter
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_spectrum(self):
        """Launches file browser, parses data, and appends the sample into the active working repository."""
        file_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_paths:
            return
            
        for file_path in file_paths:
            base_name = os.path.basename(file_path)
            pure_name = os.path.splitext(base_name)[0]
            
            # Avoid duplicate loading allocation
            if pure_name in self.loaded_samples:
                continue
                
            try:
                # Ingest the structural numerical columns from the text file
                data = pd.read_csv(file_path, sep=r'\s+', header=None, names=['Wavenumber', 'Intensity'])
                
                # Check for a matching .jpg image name within the source directory
                dir_name = os.path.dirname(file_path)
                potential_img = os.path.join(dir_name, f"{pure_name}.jpg")
                img_path = potential_img if os.path.exists(potential_img) else None
                
                # Store sample metadata payload
                self.loaded_samples[pure_name] = (data, img_path)
                self.samples_listbox.insert(tk.END, pure_name)
                
            except Exception as e:
                messagebox.showerror("Data Error", f"Could not parse file: {base_name}\nDetails: {str(e)}")
        
        self.replot_data()

    def replot_data(self):
        """Clears the canvas workspace, updates data layouts based on Overlay/Stacked states and X crop ranges."""
        self.ax.clear()
        
        if not self.loaded_samples:
            self.canvas.draw()
            return
            
        # Extract user-defined crop/zoom range configurations
        try:
            min_x_val = float(self.entry_min_x.get()) if self.entry_min_x.get().strip() else None
            max_x_val = float(self.entry_max_x.get()) if self.entry_max_x.get().strip() else None
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for the X-Axis bounds.")
            return

        current_mode = self.plot_mode.get()
        offset_multiplier = 0
        
        # Calculate maximum amplitude reference to generate proportional stacking offsets dynamically
        max_intensity_global = 0
        if current_mode == "stacked":
            for pure_name, (data, _) in self.loaded_samples.items():
                max_intensity_global = max(max_intensity_global, data['Intensity'].max())
            # Offset distance equals 80% of global peak intensity
            offset_multiplier = max_intensity_global * 0.8

        # Iterate and render all stored active datasets
        for idx, (pure_name, (data, _)) in enumerate(self.loaded_samples.items()):
            # Apply the continuous sub-segment filter boundaries if requested
            filtered_data = data.copy()
            if min_x_val is not None:
                filtered_data = filtered_data[filtered_data['Wavenumber'] >= min_x_val]
            if max_x_val is not None:
                filtered_data = filtered_data[filtered_data['Wavenumber'] <= max_x_val]
                
            # Compute dynamic vertical displacement spacing shifting
            y_shift = idx * offset_multiplier if current_mode == "stacked" else 0
            shifted_intensity = filtered_data['Intensity'] + y_shift
            
            self.ax.plot(filtered_data['Wavenumber'], shifted_intensity, linewidth=1.5, label=pure_name)
            
        # Polish layout canvas design styling
        self.ax.set_title("Raman Spectroscopy Multi-Sample Analysis", fontdict={'fontsize': 12, 'weight': 'bold'})
        self.ax.set_xlabel("Wavenumber (cm$^{-1}$)", fontdict={'fontsize': 10})
        self.ax.set_ylabel("Intensity (a.u.)" if current_mode == "overlay" else "Intensity + Offset Stacked (a.u.)", fontdict={'fontsize': 10})
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.legend(loc='upper right', fontsize=8)
        
        self.canvas.draw()

    def on_sample_selected(self, event):
        """Monitors user interactions inside the active pool listbox to trigger image rendering states."""
        selection = self.samples_listbox.curselection()
        if not selection:
            return
            
        selected_name = self.samples_listbox.get(selection[0])
        _, img_path = self.loaded_samples[selected_name]
        
        if img_path:
            self.btn_show_img.config(state=tk.NORMAL, bg="#2196F3")
        else:
            self.btn_show_img.config(state=tk.DISABLED, bg="#b0bec5")

    def show_crystal_image(self):
        """Spawns a modal view node containing the microscope image matching the selected active pool string."""
        selection = self.samples_listbox.curselection()
        if not selection:
            return
            
        selected_name = self.samples_listbox.get(selection[0])
        _, img_path = self.loaded_samples[selected_name]
        
        if not img_path:
            messagebox.showerror("Error", "No linked crystal image available for this sample.")
            return
            
        img_window = tk.Toplevel(self.root)
        img_window.title(f"Crystal View - {selected_name}")
        img_window.geometry("550x480")
        img_window.configure(bg="white")
        
        try:
            img = Image.open(img_path)
            img = img.resize((520, 420), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            
            lbl_img = tk.Label(img_window, image=img_tk, bg="white")
            lbl_img.image = img_tk  # Keep memory references active
            lbl_img.pack(padx=15, pady=15)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load image payload:\n{str(e)}")

    def clear_all(self):
        """Resets the collection repository objects."""
        self.loaded_samples.clear()
        self.samples_listbox.delete(0, tk.END)
        self.btn_show_img.config(state=tk.DISABLED, bg="#b0bec5")
        self.replot_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = RamanCrystalApp(root)
    root.mainloop()
