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
        self.root.title("Raman Spectroscopy & Crystal Imaging Platform")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f5f5f5")
        
        # Variables to store the currently active file paths
        self.current_txt_path = None
        self.current_img_path = None
        
        # ------------------ GUI Layout Construction ------------------
        
        # Left sidebar control panel
        self.control_frame = tk.Frame(root, width=250, bg="#e0e0e0", padx=15, pady=15, bd=2, relief=tk.GROOVE)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Control panel title header
        self.lbl_title = tk.Label(self.control_frame, text="Control Panel", font=("Arial", 14, "bold"), bg="#e0e0e0")
        self.lbl_title.pack(pady=(0, 20))
        
        # Button to trigger the Raman spectrum text file dialog
        self.btn_load = tk.Button(self.control_frame, text="Load Raman Spectrum (TXT)", command=self.load_spectrum, 
                                  font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=25, height=2, bd=3)
        self.btn_load.pack(pady=10)
        
        # Button to display the corresponding crystal microscope image
        self.btn_show_img = tk.Button(self.control_frame, text="Show Crystal Image", command=self.show_crystal_image, 
                                      font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=25, height=2, bd=3, state=tk.DISABLED)
        self.btn_show_img.pack(pady=10)
        
        # Visual frame to exhibit the status of the current working sample
        self.status_frame = tk.LabelFrame(self.control_frame, text="Current Sample Status", font=("Arial", 9, "italic"), bg="#e0e0e0", padx=5, pady=5)
        self.status_frame.pack(pady=30, fill=tk.X)
        
        self.lbl_status = tk.Label(self.status_frame, text="No file loaded", font=("Arial", 10), wraplength=200, bg="#e0e0e0", fg="#d32f2f")
        self.lbl_status.pack(pady=10)
        
        # Right workspace panel for embedding the Matplotlib graph canvas
        self.plot_frame = tk.Frame(root, bg="white", bd=2, relief=tk.SUNKEN)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initializing the Matplotlib figure and embedding it into Tkinter
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_spectrum(self):
        """Launches file browser, parses the numerical Raman text data, and plots the raw spectrum."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
            
        self.current_txt_path = file_path
        base_name = os.path.basename(file_path)
        pure_name = os.path.splitext(base_name)[0]
        
        # 1. Ingest and parse the structural numerical columns from the text file
        try:
            # Parses data using a whitespace/tab regex separator (sep=r'\s+') assuming no header row
            data = pd.read_csv(file_path, sep=r'\s+', header=None, names=['Wavenumber', 'Intensity'])
            
            # Flush the previous frame, draw the active spectrum, and style the graph canvas
            self.ax.clear()
            self.ax.plot(data['Wavenumber'], data['Intensity'], color='#e0115f', linewidth=1.5, label="Raman Intensity")
            self.ax.set_title(f"Raman Spectrum: {pure_name}", fontdict={'fontsize': 12, 'weight': 'bold'})
            self.ax.set_xlabel("Wavenumber (cm$^{-1}$)", fontdict={'fontsize': 10})
            self.ax.set_ylabel("Intensity (a.u.)", fontdict={'fontsize': 10})
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.legend()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Data Error", f"Could not parse the Raman data file.\nMake sure it contains two numerical columns.\n\nError details: {str(e)}")
            return

        # 2. Automatically check for a matching .jpg image name within the source directory
        dir_name = os.path.dirname(file_path)
        potential_img = os.path.join(dir_name, f"{pure_name}.jpg")
        
        if os.path.exists(potential_img):
            self.current_img_path = potential_img
            self.btn_show_img.config(state=tk.NORMAL, bg="#2196F3")
            self.lbl_status.config(text=f"Loaded:\n{pure_name}\n\n✓ Crystal image linked successfully.", fg="#388E3C")
        else:
            self.current_img_path = None
            self.btn_show_img.config(state=tk.DISABLED, bg="#b0bec5")
            self.lbl_status.config(text=f"Loaded:\n{pure_name}\n\n⚠ Corresponding image (.jpg) not found in folder.", fg="#F57C00")

    def show_crystal_image(self):
        """Spawns a new Toplevel visual node window rendering the paired crystal microscopy image file."""
        if not self.current_img_path:
            messagebox.showerror("Error", "No corresponding crystal image available.")
            return
            
        # Instantiate a detached modal layout frame for the picture
        img_window = tk.Toplevel(self.root)
        img_window.title(f"Crystal Image View - {os.path.basename(self.current_img_path)}")
        img_window.geometry("550x480")
        img_window.configure(bg="white")
        
        # Leverage Pillow framework components to scale and map the image payload
        try:
            img = Image.open(self.current_img_path)
            # Perform a proportional high-fidelity resize constraint to fit inside the modal
            img = img.resize((520, 420), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            
            lbl_img = tk.Label(img_window, image=img_tk, bg="white")
            lbl_img.image = img_tk  # Persistent structural reference allocation to avoid garbage collection disposal
            lbl_img.pack(padx=15, pady=15)
            
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not open image file.\nError details: {str(e)}")

# Application Orchestration Entry Point
if __name__ == "__main__":
    root = tk.Tk()
    app = RamanCrystalApp(root)
    root.mainloop()
