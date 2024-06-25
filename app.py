import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Menu, messagebox, filedialog, Canvas, Button
import numpy as np
import cv2

#from transformations import Transformations

class App:
    def __init__(self, master=None):
        self.list_of_images = []
        self.current_image_index = -1
        self.toplevel = None
        self.toplevel_sheet = None
        self.canvas = None
        self.master = master
        self.photo = None

        self.master.title('Modsen')
        self.master.state('zoomed')

        self.master.grid_columnconfigure(0, weight=1)

        # Create "Menu"
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # Create "File"
        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label='Choose directory', command=self.open_dir)
        file_menu.add_separator()
        menubar.add_cascade(label='File', menu=file_menu)

        # Create "Help"
        help_menu = Menu(menubar, tearoff=False)
        help_menu.add_command(label='About', command=self.show_about)
        menubar.add_cascade(label='Help', menu=help_menu)

        self.image_label = tk.Label(self.master)
        self.image_label.pack()  # Add the label to the GUI layout

        # Create Scale Button
        self.scale_button = Button(self.master, text="Scale", command=self.scale_image_dialog)
        self.scale_button.pack(side="left", padx=5)

        # Create Rotate Button
        self.rotate_button = Button(self.master, text="Rotate", command=self.rotate_image_dialog)
        self.rotate_button.pack(side="left", padx=5)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if file_path and self.photo:
            # Convert the PhotoImage to a PIL Image object
            pil_image = ImageTk.getimage(self.photo)

            # Convert the image to RGB mode
            if pil_image.mode == 'RGBA':
                pil_image = pil_image.convert('RGB')

            # Save the image using PIL
            pil_image.save(file_path)

            messagebox.showinfo('Save', 'Image saved successfully.')
        else:
            messagebox.showwarning('Save', 'No image to save.')

    def open_dir(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Use PIL to open and display the image
            image = Image.open(file_path)
            #image = image.resize((800, 800))  # Resize the image to fit the GUI

            # Create the PhotoImage with the correct dimensions
            self.photo = ImageTk.PhotoImage(image)

            # Configure the image_label with the PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def show_about(self):
        messagebox.showinfo('About', 'Modsen - Image Editing App')

    def scale_image_dialog(self):
        scale_factor = float(input("Enter the scale factor (e.g., 0.5 for half size, 2 for double size): "))
        self.scale_image(scale_factor)

    def rotate_image_dialog(self):
        angle = float(input("Enter the rotation angle in degrees: "))
        self.rotate_image(angle)

    def scale_image(self, scale_factor):
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Resize the image using PIL
            scaled_image = pil_image.resize((int(pil_image.width * scale_factor), int(pil_image.height * scale_factor)))

            # Update the PhotoImage with the scaled image
            self.photo = ImageTk.PhotoImage(scaled_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def rotate_image(self, angle):
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Rotate the image using PIL
            rotated_image = pil_image.rotate(angle)

            # Update the PhotoImage with the rotated image
            self.photo = ImageTk.PhotoImage(rotated_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection
