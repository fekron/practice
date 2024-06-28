import unittest
import os
from unittest.mock import patch
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
from app import App, tk


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary test image file
        cls.test_image_path = 'test_image.jpg'
        test_image = Image.new('RGB', (100, 100), color='red')
        test_image.save(cls.test_image_path)

    @classmethod
    def tearDownClass(cls):
        # Remove the temporary test image file
        os.remove(cls.test_image_path)

    def setUp(self):
        # Create an instance of the application
        self.app = App(tk.Tk())

    def tearDown(self):
        # Destroy the application instance
        self.app.master.destroy()

    def test_open_dir(self):
        # Mock the file dialog to return the test image file path
        with patch('tkinter.filedialog.askopenfilename', return_value=self.test_image_path):
            self.app.open_dir()

        # Check if the image label has been updated with the loaded image
        self.assertIsNotNone(self.app.photo)

    def test_save_image(self):
        # Open the test image
        self.app.open_dir()

        # Mock the file dialog to return a test save file path
        with patch('tkinter.filedialog.asksaveasfilename', return_value='test_save.jpg'):
            with patch('PIL.Image.Image.save') as mock_save:
                self.app.save_image()

        # Check if the save file dialog was called
        self.assertTrue(mock_save.called)

    def test_save_image_no_image(self):
        # Mock the message box to check if the warning is shown
        with patch.object(messagebox, 'showwarning') as mock_showwarning:
            self.app.save_image()

        # Check if the warning message box was shown
        self.assertTrue(mock_showwarning.called)

    def test_scale_image(self):
        # Open the test image
        self.app.open_dir()

        # Scale the image
        scale_factor = 0.5
        self.app.scale_image(scale_factor)

        # Get the scaled image size
        scaled_image_size = (
            int(self.app.photo.width() * scale_factor),
            int(self.app.photo.height() * scale_factor)
        )

        # Check if the image label has been updated with the scaled image
        self.assertEqual(scaled_image_size, (self.app.photo.width(), self.app.photo.height()))

    def test_rotate_image(self):
        # Open the test image
        self.app.open_dir()

        # Rotate the image
        angle = 45
        self.app.rotate_image(angle)

        # Check if the image label has been updated with the rotated image
        self.assertEqual(angle, self.app.photo.angle)

    def test_show_about(self):
        # Mock the message box to check if the information dialog is shown
        with patch.object(messagebox, 'showinfo') as mock_showinfo:
            self.app.show_about()

        # Check if the information dialog was shown
        self.assertTrue(mock_showinfo.called)


if __name__ == '__main__':
    unittest.main()