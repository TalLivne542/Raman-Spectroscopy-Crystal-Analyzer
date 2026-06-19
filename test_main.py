import unittest
import os
import pandas as pd
import tkinter as tk
from main import RamanCrystalApp  # Imports your main application class

class TestRamanCrystalApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Creates dummy data files before running any tests."""
        cls.test_txt_path = "Test_Sample_A.txt"
        cls.test_jpg_path = "Test_Sample_A.jpg"
        
        # Create a mock 2-column dataframe mimicking Raman data
        mock_data = {
            'Wavenumber': [100.0, 200.0, 300.0, 400.0, 500.0],
            'Intensity': [10.0, 50.0, 150.0, 30.0, 5.0]
        }
        df = pd.DataFrame(mock_data)
        # Save to space-separated text file without headers
        df.to_csv(cls.test_txt_path, sep=' ', header=False, index=False)
        
        # Create an empty file to mimic the corresponding image payload
        with open(cls.test_jpg_path, 'w') as f:
            f.write("mock image data")

    @classmethod
    def tearDownClass(cls):
        """Cleans up the generated dummy data files after all tests finish."""
        if os.path.exists(cls.test_txt_path):
            os.remove(cls.test_txt_path)
        if os.path.exists(cls.test_jpg_path):
            os.remove(cls.test_jpg_path)

    def setUp(self):
        """Initializes the Tkinter root environment before each test method."""
        self.root = tk.Tk()
        self.app = RamanCrystalApp(self.root)

    def tearDown(self):
        """Destroys the Tkinter window workspace after each test execution."""
        self.root.destroy()

    def test_initial_state(self):
        """Verifies that the application launches with an empty data repository state."""
        self.assertEqual(len(self.app.loaded_samples), 0)
        self.assertEqual(self.app.samples_listbox.size(), 0)
        self.assertEqual(self.app.btn_show_img['state'], tk.DISABLED or 'disabled')

    def test_clear_all_functionality(self):
        """Validates that the repository purge correctly flushes stored sample objects."""
        # Inject mock state data manually into the repository frame
        mock_df = pd.DataFrame({'Wavenumber': [100], 'Intensity': [10]})
        self.app.loaded_samples["Test_Sample_A"] = (mock_df, self.test_jpg_path)
        self.app.samples_listbox.insert(tk.END, "Test_Sample_A")
        
        # Execute flushing procedure
        self.app.clear_all()
        
        # Assert empty structural footprint states
        self.assertEqual(len(self.app.loaded_samples), 0)
        self.assertEqual(self.app.samples_listbox.size(), 0)

if __name__ == '__main__':
    unittest.main()
