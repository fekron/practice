import os
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageDraw, ImageFont
from tkinter import Menu, messagebox, filedialog, Canvas, Button, simpledialog, colorchooser
import random
import numpy as np
import cv2


class App:
    """
    The main application class for the Modsen image editing app.
    """

    def __init__(self, master=None):
        """
        Initialize the application.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
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

        # Create Brightness Button
        self.brightness_button = Button(self.master, text="Brightness", command=self.change_brightness_dialog)
        self.brightness_button.pack(side="left", padx=5, pady=5)

        # Create Crop Button
        self.crop_button = Button(self.master, text="Crop", command=self.crop_image_dialog)
        self.crop_button.pack(side="left", padx=5)

        # Create Reflect Button
        self.reflect_button = Button(self.master, text="Reflect", command=self.reflect_image_dialog)
        self.reflect_button.pack(side="left", padx=5)

        # Create Noise Button
        self.noise_button = Button(self.master, text="Noise", command=self.add_noise_dialog)
        self.noise_button.pack(side="left", padx=5)

        # Create Contrast Button
        self.contrast_button = Button(self.master, text="Contrast", command=self.change_contrast_dialog)
        self.contrast_button.pack(side="left", padx=5)

        # Create Random Crop Button
        self.random_crop_button = Button(self.master, text="Random Crop", command=self.random_crop_dialog)
        self.random_crop_button.pack(side="left", padx=5)

        # Create Add Text Button
        self.add_text_button = Button(self.master, text="Add text", command=self.add_text_dialog)
        self.add_text_button.pack(side="left", padx=5)

    def save_image(self):
        """
        Save the currently displayed image.

        Prompts the user to choose a file path and saves the image as a JPG file.

        Raises:
            tk.messagebox.showwarning: If there is no image to save.
            tk.messagebox.showinfo: If the image is saved successfully.
        """
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
        """
        Open a file dialog to choose an image file and display it.

        Uses PIL to open and display the selected image file.

        Raises:
            tk.messagebox.showinfo: If the About dialog is shown.
        """
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
        """
        Show an information messagebox with details about the application.
        """
        messagebox.showinfo('About', 'Modsen - Image Editing App')

    def scale_image(self, scale_factor):
        """
        Scale the currently displayed image by the given scale factor.

        Args:
            scale_factor (float): The scale factor to apply to the image.
        """
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
        """
        Rotate the currently displayed image by the given angle.

        Args:
            angle (float): The rotation angle in degrees.
        """
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

    def scale_image_dialog(self):
        """
        Prompt the user for a scale factor and scale the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Scale Image")

        # Create a scale factor entry field
        scale_label = tk.Label(self.toplevel, text="Scale Factor:")
        scale_label.pack(side="left", padx=5, pady=5)
        scale_entry = tk.Entry(self.toplevel)
        scale_entry.pack(side="left", padx=5, pady=5)
        scale_entry.focus_set()

        # Create a label for scale factor ranges
        scale_range_text = "Scale by the given factor, f.e. 0.5 to halve it, 2 to double"
        scale_range_label = tk.Label(self.toplevel, text=scale_range_text)
        scale_range_label.pack(padx=5, pady=5)

        # Create a scale button
        scale_button = tk.Button(self.toplevel, text="Scale",
                                 command=lambda: self.scale_image(float(scale_entry.get())))
        scale_button.pack(side="left", padx=5, pady=5)

    def rotate_image_dialog(self):
        """
        Prompt the user for a rotation angle and rotate the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Rotate Image")

        # Create a rotation angle entry field
        angle_label = tk.Label(self.toplevel, text="Rotation Angle:")
        angle_label.pack(side="left", padx=5, pady=5)
        angle_entry = tk.Entry(self.toplevel)
        angle_entry.pack(side="left", padx=5, pady=5)
        angle_entry.focus_set()

        # Create a label for rotate info
        rotate_text = "Rotate by the given angle (in degrees)"
        rotate_label = tk.Label(self.toplevel, text=rotate_text)
        rotate_label.pack(padx=5, pady=5)

        # Create a rotate button
        rotate_button = tk.Button(self.toplevel, text="Rotate", command=lambda: self.rotate_image(float(angle_entry.get())))
        rotate_button.pack(side="left", padx=5, pady=5)

    def change_brightness_dialog(self):
        """
        Prompt the user for a brightness factor and change the image brightness accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Change Brightness")

        # Create a brightness factor entry field
        brightness_label = tk.Label(self.toplevel, text="Brightness Factor:")
        brightness_label.pack(side="left", padx=5, pady=5)
        brightness_entry = tk.Entry(self.toplevel)
        brightness_entry.pack(side="left", padx=5, pady=5)
        brightness_entry.focus_set()

        # Create a label for brightness info
        brightness_text = "Less than 1.0 decrease brightness, more than 1.0 increase"
        brightness_text_label = tk.Label(self.toplevel, text=brightness_text)
        brightness_text_label.pack(padx=5, pady=5)

        # Create a change brightness button
        brightness_button = tk.Button(self.toplevel, text="Change Brightness",
                                      command=lambda: self.change_brightness(float(brightness_entry.get())))
        brightness_button.pack(side="left", padx=5, pady=5)

    def change_brightness(self, brightness_factor):
        """
        Change the brightness of the currently displayed image by the given factor.

        Args:
            brightness_factor (float): The brightness factor to apply to the image.
                                      Values less than 1.0 decrease brightness, and values greater than 1.0 increase brightness.
        """
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Create an ImageEnhance object and apply brightness enhancement
            enhancer = ImageEnhance.Brightness(pil_image)
            enhanced_image = enhancer.enhance(brightness_factor)

            # Update the PhotoImage with the enhanced image
            self.photo = ImageTk.PhotoImage(enhanced_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def crop_image_dialog(self):
        """
        Prompt the user for crop coordinates and crop the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Crop Image")

        # Create crop coordinate entry fields
        x_label = tk.Label(self.toplevel, text="X:")
        x_label.pack(side="left", padx=5, pady=5)
        x_entry = tk.Entry(self.toplevel)
        x_entry.pack(side="left", padx=5, pady=5)
        x_entry.focus_set()

        y_label = tk.Label(self.toplevel, text="Y:")
        y_label.pack(side="left", padx=5, pady=5)
        y_entry = tk.Entry(self.toplevel)
        y_entry.pack(side="left", padx=5, pady=5)

        width_label = tk.Label(self.toplevel, text="Width:")
        width_label.pack(side="left", padx=5, pady=5)
        width_entry = tk.Entry(self.toplevel)
        width_entry.pack(side="left", padx=5, pady=5)

        height_label = tk.Label(self.toplevel, text="Height:")
        height_label.pack(side="left", padx=5, pady=5)
        height_entry = tk.Entry(self.toplevel)
        height_entry.pack(side="left", padx=5, pady=5)

        # Create a crop button
        crop_button = tk.Button(self.toplevel, text="Crop",
                                command=lambda: self.crop_image(int(x_entry.get()), int(y_entry.get()),
                                                                int(width_entry.get()), int(height_entry.get())))
        crop_button.pack(side="left", padx=5, pady=5)

    def crop_image(self, x, y, width, height):
        """
        Crop the currently displayed image based on the given coordinates and dimensions.

        Args:
            x (int): The x-coordinate of the top-left corner of the crop area.
            y (int): The y-coordinate of the top-left corner of the crop area.
            width (int): The width of the crop area.
            height (int): The height of the crop area.
        """
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Crop the image
            cropped_image = pil_image.crop((x, y, x + width, y + height))

            # Update the PhotoImage with the cropped image
            self.photo = ImageTk.PhotoImage(cropped_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def reflect_image_dialog(self):
        """
        Prompt the user for reflection type and reflect the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Reflect Image")

        # Create reflection type radio buttons
        reflection_var = tk.StringVar()
        reflection_var.set("horizontal")
        horizontal_radio = tk.Radiobutton(self.toplevel, text="Horizontal", variable=reflection_var, value="horizontal")
        horizontal_radio.pack(side="left", padx=5, pady=5)
        vertical_radio = tk.Radiobutton(self.toplevel, text="Vertical", variable=reflection_var, value="vertical")
        vertical_radio.pack(side="left", padx=5, pady=5)

        # Create a reflect button
        reflect_button = tk.Button(self.toplevel, text="Reflect",
                                   command=lambda: self.reflect_image(reflection_var.get()))
        reflect_button.pack(side="left", padx=5, pady=5)

    def reflect_image(self, reflection_type):
        """
        Reflect the currently displayed image based on the given reflection type.

        Args:
            reflection_type (str): The reflection type. Possible values: "horizontal" or "vertical".
        """
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Reflect the image
            if reflection_type == "horizontal":
                reflected_image = ImageOps.mirror(pil_image)
            elif reflection_type == "vertical":
                reflected_image = ImageOps.flip(pil_image)
            else:
                return

            # Update the PhotoImage with the reflected image
            self.photo = ImageTk.PhotoImage(reflected_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def add_noise_dialog(self):
        """
        Prompt the user for the noise intensity and add noise to the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Add Noise")

        # Create noise intensity entry field
        intensity_label = tk.Label(self.toplevel, text="Noise Intensity:")
        intensity_label.pack(side="left", padx=5, pady=5)
        intensity_entry = tk.Entry(self.toplevel)
        intensity_entry.pack(side="left", padx=5, pady=5)
        intensity_entry.focus_set()

        # Create a label for noise info
        brightness_text = "Add noise based on the given intensity, between 0 and 1"
        brightness_text_label = tk.Label(self.toplevel, text=brightness_text)
        brightness_text_label.pack(padx=5, pady=5)

        # Create add noise button
        noise_button = tk.Button(self.toplevel, text="Add Noise", command=lambda: self.add_noise(intensity_entry.get()))
        noise_button.pack(side="left", padx=5, pady=5)

    def add_noise(self, intensity):
        """
        Add random noise to the currently displayed image based on the given intensity.

        Args:
            intensity (str): The intensity of the noise. A higher value results in more intense noise.
        """
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Convert the intensity to a float value between 0 and 1
            # To see the better result use very low intensity, f.e. 0.001
            intensity = float(intensity)

            # Calculate the maximum pixel value based on the image mode
            max_pixel_value = 255 if pil_image.mode == "RGB" else 65535

            # Loop through each pixel and add noise
            for x in range(pil_image.width):
                for y in range(pil_image.height):
                    pixel = pil_image.getpixel((x, y))

                    # Generate random noise for each color channel
                    noise = tuple(
                        min(max(int(p + random.uniform(-intensity, intensity) * max_pixel_value), 0), max_pixel_value)
                        for p in pixel
                    )

                    pil_image.putpixel((x, y), noise)

            # Update the PhotoImage with the modified image
            self.photo = ImageTk.PhotoImage(pil_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def change_contrast_dialog(self):
        """
        Prompt the user for the contrast level and change the contrast of the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Change Contrast")

        # Create contrast level entry field
        level_label = tk.Label(self.toplevel, text="Contrast Level:")
        level_label.pack(side="left", padx=5, pady=5)
        level_entry = tk.Entry(self.toplevel)
        level_entry.pack(side="left", padx=5, pady=5)
        level_entry.focus_set()

        # Create a label for contrast info
        brightness_text = "Less than 1.0 decrease the contrast, more than 1.0 increase"
        brightness_text_label = tk.Label(self.toplevel, text=brightness_text)
        brightness_text_label.pack(padx=5, pady=5)

        # Create change contrast button
        contrast_button = tk.Button(self.toplevel, text="Change Contrast",
                                    command=lambda: self.change_contrast(level_entry.get()))
        contrast_button.pack(side="left", padx=5, pady=5)

    def change_contrast(self, level):
        """
        Change the contrast of the currently displayed image based on the given contrast level.

        Args:
            level (str): The contrast level. 1.0 represents the original contrast.
                          Values less than 1.0 decrease the contrast, and values greater than 1.0 increase the contrast.
        """
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Convert the contrast level to a float value
            level = float(level)

            # Create an enhancer object for contrast adjustment
            enhancer = ImageEnhance.Contrast(pil_image)

            # Adjust the contrast
            adjusted_image = enhancer.enhance(level)

            # Update the PhotoImage with the adjusted image
            self.photo = ImageTk.PhotoImage(adjusted_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def random_crop_dialog(self):
        """
        Prompt the user for the crop size and randomly crop the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Random Crop")

        # Create crop size entry fields
        width_label = tk.Label(self.toplevel, text="Width:")
        width_label.pack(side="left", padx=5, pady=5)
        width_entry = tk.Entry(self.toplevel)
        width_entry.pack(side="left", padx=5, pady=5)
        width_entry.focus_set()

        height_label = tk.Label(self.toplevel, text="Height:")
        height_label.pack(side="left", padx=5, pady=5)
        height_entry = tk.Entry(self.toplevel)
        height_entry.pack(side="left", padx=5, pady=5)

        # Create random crop button
        crop_button = tk.Button(self.toplevel, text="Random Crop",
                                command=lambda: self.random_crop(width_entry.get(), height_entry.get()))
        crop_button.pack(side="left", padx=5, pady=5)

    def random_crop(self, width, height):
        """
        Randomly crop the currently displayed image based on the given width and height.

        Args:
            width (str): The width of the crop area.
            height (str): The height of the crop area.
        """
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Convert the width and height to integers
            width = int(width)
            height = int(height)

            # Calculate the maximum crop positions
            max_x = pil_image.width - width
            max_y = pil_image.height - height

            if max_x < 0 or max_y < 0:
                # Crop size is larger than the image, do not perform cropping
                return

            # Generate random crop positions
            x = np.random.randint(0, max_x)
            y = np.random.randint(0, max_y)

            # Crop the image
            cropped_image = pil_image.crop((x, y, x + width, y + height))

            # Update the PhotoImage with the cropped image
            self.photo = ImageTk.PhotoImage(cropped_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection

    def add_text_dialog(self):
        """
        Prompt the user for the text content, position, font size, and color, and add text to the image accordingly.
        """
        # Create a top-level dialog window
        self.toplevel = tk.Toplevel(self.master)
        self.toplevel.title("Add Text")

        # Create text content entry field
        content_label = tk.Label(self.toplevel, text="Text Content:")
        content_label.pack(side="left", padx=5, pady=5)
        content_entry = tk.Entry(self.toplevel)
        content_entry.pack(side="left", padx=5, pady=5)
        content_entry.focus_set()

        # Create text position entry fields
        position_label = tk.Label(self.toplevel, text="Text Position:")
        position_label.pack(side="left", padx=5, pady=5)

        x_label = tk.Label(self.toplevel, text="X:")
        x_label.pack(side="left", padx=5, pady=5)
        x_entry = tk.Entry(self.toplevel)
        x_entry.pack(side="left", padx=5, pady=5)

        y_label = tk.Label(self.toplevel, text="Y:")
        y_label.pack(side="left", padx=5, pady=5)
        y_entry = tk.Entry(self.toplevel)
        y_entry.pack(side="left", padx=5, pady=5)

        # Create font size entry field
        size_label = tk.Label(self.toplevel, text="Font Size:")
        size_label.pack(side="left", padx=5, pady=5)
        size_entry = tk.Entry(self.toplevel)
        size_entry.pack(side="left", padx=5, pady=5)

        # Create color picker button
        color_button = tk.Button(self.toplevel, text="Choose Color", command=self.choose_text_color)
        color_button.pack(side="left", padx=5, pady=5)

        # Create add text button
        text_button = tk.Button(self.toplevel, text="Add Text",
                                command=lambda: self.add_text(content_entry.get(), x_entry.get(), y_entry.get(),
                                                              size_entry.get()))
        text_button.pack(side="left", padx=5, pady=5)

    def choose_text_color(self):
        """
        Open a color picker dialog and set the selected color as the text color.
        """
        color = tk.colorchooser.askcolor()
        if color:
            self.text_color = color[1]  # Get the hex color value

    def add_text(self, content, x, y, size):
        """
        Add text to the currently displayed image based on the given content, position, font size, and color.

        Args:
            content (str): The text content.
            x (str): The X-coordinate of the text position.
            y (str): The Y-coordinate of the text position.
            size (str): The font size.
        """
        if self.photo:
            # Get the PIL Image object from the PhotoImage
            pil_image = ImageTk.getimage(self.photo)

            # Convert the position, size, and color values
            x = int(x)
            y = int(y)
            size = int(size)
            color = self.text_color if hasattr(self, "text_color") else "black"

            # Create a PIL ImageDraw object
            draw = ImageDraw.Draw(pil_image)

            # Create a PIL ImageFont object with the specified font size
            font = ImageFont.truetype("arial.ttf", size)

            # Draw the text on the image
            draw.text((x, y), content, fill=color, font=font)

            # Update the PhotoImage with the modified image
            self.photo = ImageTk.PhotoImage(pil_image)

            # Configure the image_label with the updated PhotoImage
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo  # Keep a reference to the image to prevent garbage collection