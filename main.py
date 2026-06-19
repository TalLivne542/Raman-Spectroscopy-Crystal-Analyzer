import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import scipy.signal

class RamanCrystalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Raman Spectroscopy & Crystal Imaging Platform")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f5f5f5")
        
        # Structure to hold multiple loaded datasets: { pure_name: (dataframe, img_path) }
        self.loaded_samples = {}
        self.sample_visibility = {}
        self.selected_sample_name = None
        
        # ------------------ GUI Layout Construction ------------------
        
        # Left sidebar control panel
        self.control_frame = tk.Frame(root, width=340, bg="#e0e0e0", padx=15, pady=15, bd=2, relief=tk.GROOVE)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Control panel title header
        self.lbl_title = tk.Label(self.control_frame, text="Control Panel", font=("Arial", 16, "bold"), bg="#e0e0e0")
        self.lbl_title.pack(pady=(0, 15))
        
        # Button to load a Raman spectrum file
        self.btn_load = tk.Button(self.control_frame, text="➕ Load Raman Spectrum (TXT)", command=self.load_spectrum, 
                                  font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", height=2, bd=3)
        self.btn_load.pack(fill=tk.X, pady=5)
        
        # Button to display the crystal image of the selected sample
        self.btn_show_img = tk.Button(self.control_frame, text="📷 Show Selected Crystal Image", command=self.show_crystal_image, 
                                      font=("Arial", 11, "bold"), bg="#2196F3", fg="white", height=2, bd=3, state=tk.DISABLED)
        self.btn_show_img.pack(fill=tk.X, pady=5)
        
        # Button to clear all loaded samples
        self.btn_clear = tk.Button(self.control_frame, text="🗑️ Clear All Spectra", command=self.clear_all, 
                                   font=("Arial", 10, "bold"), bg="#f44336", fg="white", height=1, bd=2)
        self.btn_clear.pack(fill=tk.X, pady=5)
        
        # --- Section: Display Mode Selection ---
        self.mode_frame = tk.LabelFrame(self.control_frame, text="Display Configuration", font=("Arial", 12, "bold"), bg="#e0e0e0", padx=5, pady=5)
        self.mode_frame.pack(pady=8, fill=tk.X)
        
        self.plot_mode = tk.StringVar(value="overlay")
        tk.Radiobutton(self.mode_frame, text="Overlay (Same Y-Axis)", variable=self.plot_mode, value="overlay", 
                       bg="#e0e0e0", font=("Arial", 11), command=self.replot_data).pack(anchor=tk.W, pady=2)
        tk.Radiobutton(self.mode_frame, text="Stacked (Y-Offset Separation)", variable=self.plot_mode, value="stacked", 
                       bg="#e0e0e0", font=("Arial", 11), command=self.replot_data).pack(anchor=tk.W, pady=2)
        
        # --- Section: Wavenumber Range Crop/Zoom ---
        self.range_frame = tk.LabelFrame(self.control_frame, text="Wavenumber Range (X-Axis Crop)", font=("Arial", 12, "bold"), bg="#e0e0e0", padx=5, pady=5)
        self.range_frame.pack(pady=8, fill=tk.X)
        
        tk.Label(self.range_frame, text="Min X (cm⁻¹):", bg="#e0e0e0", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, padx=2, pady=5)
        self.entry_min_x = tk.Entry(self.range_frame, width=8, font=("Arial", 11))
        self.entry_min_x.grid(row=0, column=1, padx=2, pady=5)
        
        tk.Label(self.range_frame, text="Max X (cm⁻¹):", bg="#e0e0e0", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, padx=2, pady=5)
        self.entry_max_x = tk.Entry(self.range_frame, width=8, font=("Arial", 11))
        self.entry_max_x.grid(row=1, column=1, padx=2, pady=5)
        
        self.btn_apply_range = tk.Button(self.range_frame, text="Apply Range Filter", command=self.replot_data, font=("Arial", 10, "bold"), bg="#9C27B0", fg="white")
        self.btn_apply_range.grid(row=2, column=0, columnspan=2, pady=8, sticky=tk.EW)
        
        # --- Section: Peak Detection Configuration ---
        self.peaks_frame = tk.LabelFrame(self.control_frame, text="Peak Detection", font=("Arial", 12, "bold"), bg="#e0e0e0", padx=5, pady=5)
        self.peaks_frame.pack(pady=8, fill=tk.X)
        
        self.show_peaks = tk.BooleanVar(value=True)
        tk.Checkbutton(self.peaks_frame, text="Label Dominant Peaks", variable=self.show_peaks, 
                       bg="#e0e0e0", font=("Arial", 11), command=self.replot_data).pack(anchor=tk.W, pady=2)
                       
        peaks_count_frame = tk.Frame(self.peaks_frame, bg="#e0e0e0")
        peaks_count_frame.pack(fill=tk.X, pady=2)
        tk.Label(peaks_count_frame, text="Max Peaks:", bg="#e0e0e0", font=("Arial", 11)).pack(side=tk.LEFT, padx=2)
        self.entry_peaks_count = tk.Entry(peaks_count_frame, width=5, font=("Arial", 11))
        self.entry_peaks_count.insert(0, "5")
        self.entry_peaks_count.pack(side=tk.LEFT, padx=2)
        
        prom_frame = tk.Frame(self.peaks_frame, bg="#e0e0e0")
        prom_frame.pack(fill=tk.X, pady=2)
        tk.Label(prom_frame, text="Min Prom (%):", bg="#e0e0e0", font=("Arial", 11)).pack(side=tk.LEFT, padx=2)
        self.entry_prominence = tk.Entry(prom_frame, width=5, font=("Arial", 11))
        self.entry_prominence.insert(0, "5")
        self.entry_prominence.pack(side=tk.LEFT, padx=2)
        
        self.btn_apply_peaks = tk.Button(self.peaks_frame, text="Update Peaks", command=self.replot_data, font=("Arial", 10, "bold"), bg="#FF9800", fg="white")
        self.btn_apply_peaks.pack(fill=tk.X, pady=4)
        
        # --- Section: Active Samples Pool (Scrollable List with Checkboxes) ---
        self.list_frame = tk.LabelFrame(self.control_frame, text="Active Samples Pool", font=("Arial", 12, "bold"), bg="#e0e0e0", padx=5, pady=5)
        self.list_frame.pack(pady=8, fill=tk.BOTH, expand=True)
        
        # Scrollable Canvas container
        self.pool_canvas = tk.Canvas(self.list_frame, bg="#e0e0e0", bd=0, highlightthickness=0)
        self.pool_scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.pool_canvas.yview)
        self.scrollable_pool_frame = tk.Frame(self.pool_canvas, bg="#e0e0e0")
        
        self.scrollable_pool_frame.bind(
            "<Configure>",
            lambda e: self.pool_canvas.configure(
                scrollregion=self.pool_canvas.bbox("all")
            )
        )
        
        self.pool_canvas_window = self.pool_canvas.create_window((0, 0), window=self.scrollable_pool_frame, anchor="nw")
        self.pool_canvas.configure(yscrollcommand=self.pool_scrollbar.set)
        
        # Adjust inner frame width dynamically
        self.list_frame.bind("<Configure>", self.on_list_frame_configure)
        
        self.pool_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pool_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
                self.sample_visibility[pure_name] = tk.BooleanVar(value=True)
                self.selected_sample_name = pure_name
                
            except Exception as e:
                messagebox.showerror("Data Error", f"Could not parse file: {base_name}\nDetails: {str(e)}")
        
        self.update_active_pool_ui()
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

        # Extract peak detection options
        annotate_peaks = self.show_peaks.get()
        try:
            max_peaks = int(self.entry_peaks_count.get())
        except ValueError:
            max_peaks = 5
        try:
            min_prominence_pct = float(self.entry_prominence.get())
        except ValueError:
            min_prominence_pct = 5.0

        # Iterate and render all stored active datasets
        plot_idx = 0
        for pure_name, (data, _) in self.loaded_samples.items():
            # Skip if hidden
            if pure_name in self.sample_visibility and not self.sample_visibility[pure_name].get():
                continue
                
            # Apply the continuous sub-segment filter boundaries if requested
            filtered_data = data.copy()
            if min_x_val is not None:
                filtered_data = filtered_data[filtered_data['Wavenumber'] >= min_x_val]
            if max_x_val is not None:
                filtered_data = filtered_data[filtered_data['Wavenumber'] <= max_x_val]
                
            # Compute dynamic vertical displacement spacing shifting
            y_shift = plot_idx * offset_multiplier if current_mode == "stacked" else 0
            shifted_intensity = filtered_data['Intensity'] + y_shift
            
            line, = self.ax.plot(filtered_data['Wavenumber'], shifted_intensity, linewidth=1.5, label=pure_name)
            line_color = line.get_color()
            
            # --- Peak Detection and Annotation ---
            if annotate_peaks and len(filtered_data) > 0:
                y_vals = filtered_data['Intensity'].values
                x_vals = filtered_data['Wavenumber'].values
                
                # Dynamic prominence threshold based on visible intensity range
                y_range = y_vals.max() - y_vals.min()
                prominence_val = y_range * (min_prominence_pct / 100.0) if y_range > 0 else 1.0
                
                # Detect peaks
                peaks, properties = scipy.signal.find_peaks(y_vals, prominence=prominence_val)
                
                if len(peaks) > 0:
                    prominences = properties.get('prominences', [0] * len(peaks))
                    # Pair peaks with their prominence
                    peaks_with_prom = list(zip(peaks, prominences))
                    # Sort by prominence descending
                    peaks_with_prom.sort(key=lambda x: x[1], reverse=True)
                    
                    # Take top N peaks
                    top_peaks = peaks_with_prom[:max_peaks]
                    
                    # Sort by index to draw left-to-right
                    top_peaks.sort(key=lambda x: x[0])
                    
                    for peak_idx, prom in top_peaks:
                        pk_x = x_vals[peak_idx]
                        pk_y_raw = y_vals[peak_idx]
                        pk_y_shifted = pk_y_raw + y_shift
                        
                        # Draw marker on peak
                        self.ax.plot(pk_x, pk_y_shifted, 'o', color=line_color, markersize=5, markerfacecolor='white', markeredgewidth=1.5)
                        
                        # Add wavenumber annotation with a small styled box
                        self.ax.annotate(f"{pk_x:.0f}", 
                                         xy=(pk_x, pk_y_shifted),
                                         xytext=(0, 6),
                                         textcoords="offset points",
                                         ha='center', 
                                         va='bottom',
                                         fontsize=8, 
                                         weight='bold', 
                                         color=line_color,
                                         bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=line_color, lw=0.5, alpha=0.85))
            
            plot_idx += 1
            
        # Polish layout canvas design styling
        self.ax.set_title("Raman Spectroscopy Multi-Sample Analysis", fontdict={'fontsize': 12, 'weight': 'bold'})
        self.ax.set_xlabel("Wavenumber (cm$^{-1}$)", fontdict={'fontsize': 10})
        self.ax.set_ylabel("Intensity (a.u.)" if current_mode == "overlay" else "Intensity + Offset Stacked (a.u.)", fontdict={'fontsize': 10})
        self.ax.grid(True, linestyle='--', alpha=0.5)
        
        # Position the legend outside of the plotting grid to the right, and increase font size
        self.ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0, fontsize=12)
        
        self.fig.tight_layout()
        self.canvas.draw()

    def on_list_frame_configure(self, event):
        # Resize the internal frame to fill the canvas width
        self.pool_canvas.itemconfig(self.pool_canvas_window, width=max(event.width - 25, 100))

    def update_active_pool_ui(self):
        # Clear current widgets
        for child in self.scrollable_pool_frame.winfo_children():
            child.destroy()
            
        # Re-populate list of items
        for pure_name in self.loaded_samples.keys():
            if pure_name not in self.sample_visibility:
                self.sample_visibility[pure_name] = tk.BooleanVar(value=True)
                
            row_bg = "#c5cae9" if pure_name == self.selected_sample_name else "#e0e0e0"
            row_frame = tk.Frame(self.scrollable_pool_frame, bg=row_bg, pady=2)
            row_frame.pack(fill=tk.X, expand=True, pady=1)
            
            # Checkbutton for plot visibility
            chk = tk.Checkbutton(row_frame, variable=self.sample_visibility[pure_name], 
                                 command=self.replot_data, bg=row_bg, activebackground=row_bg, 
                                 highlightthickness=0, bd=0)
            chk.pack(side=tk.LEFT, padx=4)
            
            # Text label for selecting sample name
            lbl_font = ("Arial", 10, "bold") if pure_name == self.selected_sample_name else ("Arial", 10)
            lbl = tk.Label(row_frame, text=pure_name, bg=row_bg, fg="#000000", font=lbl_font, anchor=tk.W, cursor="hand2")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            
            # Click events
            def make_click_handler(name):
                return lambda e: self.select_sample(name)
            lbl.bind("<Button-1>", make_click_handler(pure_name))
            row_frame.bind("<Button-1>", make_click_handler(pure_name))
            
            # Delete button (red X icon button)
            del_btn = tk.Button(row_frame, text="❌", bg="#f44336", fg="white", font=("Arial", 9, "bold"),
                                bd=0, activebackground="#d32f2f", activeforeground="white", width=2, height=1,
                                command=lambda name=pure_name: self.remove_sample(name), cursor="hand2")
            del_btn.pack(side=tk.RIGHT, padx=4)
            
        self.update_image_button_state()

    def select_sample(self, name):
        self.selected_sample_name = name
        self.update_active_pool_ui()

    def update_image_button_state(self):
        if self.selected_sample_name and self.selected_sample_name in self.loaded_samples:
            _, img_path = self.loaded_samples[self.selected_sample_name]
            if img_path:
                self.btn_show_img.config(state=tk.NORMAL, bg="#2196F3")
                return
        self.btn_show_img.config(state=tk.DISABLED, bg="#b0bec5")

    def remove_sample(self, name):
        """Removes a single specific sample from the datasets."""
        if name in self.loaded_samples:
            del self.loaded_samples[name]
        if name in self.sample_visibility:
            del self.sample_visibility[name]
        if self.selected_sample_name == name:
            self.selected_sample_name = None
            
        self.update_active_pool_ui()
        self.replot_data()

    def show_crystal_image(self):
        """Spawns a modal view node containing the microscope image matching the selected active pool string."""
        if not self.selected_sample_name:
            return
            
        _, img_path = self.loaded_samples[self.selected_sample_name]
        
        if not img_path:
            messagebox.showerror("Error", "No linked crystal image available for this sample.")
            return
            
        img_window = tk.Toplevel(self.root)
        img_window.title(f"Crystal View - {self.selected_sample_name}")
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
        self.sample_visibility.clear()
        self.selected_sample_name = None
        self.update_active_pool_ui()
        self.replot_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = RamanCrystalApp(root)
    root.mainloop()
