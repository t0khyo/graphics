import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCropperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Cropper")

        self.image_path = None
        self.image = None
        self.rect = None
        self.preview_image = None

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Load Image button
        load_button = tk.Button(self.master, text="Load Image", command=self.load_image)
        load_button.pack(pady=10)

        # Display the loaded image
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Crop Image button
        crop_button = tk.Button(self.master, text="Crop Image", command=self.crop_image)
        crop_button.pack(pady=10)

        # Run the Tkinter main loop
        self.master.mainloop()

    def load_image(self):
        # Open a file dialog to choose an image file
        file_path = filedialog.askopenfilename()

        if file_path:
            try:
                # Load the image using Pillow
                self.image = Image.open(file_path)

                # Resize the image to fit within the screen dimensions
                screen_width = self.master.winfo_screenwidth()
                screen_height = self.master.winfo_screenheight()

                if self.image.width > screen_width or self.image.height > screen_height:
                    self.image.thumbnail((screen_width, screen_height))

                # Display the image on the Tkinter canvas
                photo = ImageTk.PhotoImage(self.image)
                self.canvas.config(width=photo.width(), height=photo.height())
                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.canvas.image = photo

                # Save the image path for later use
                self.image_path = file_path

                # Remove any existing rectangle and preview image
                if self.rect:
                    self.canvas.delete(self.rect)
                if self.preview_image:
                    self.canvas.delete(self.preview_image)

                # Bind mouse events for drawing rectangle
                self.canvas.bind("<ButtonPress-1>", self.on_press)
                self.canvas.bind("<B1-Motion>", self.on_drag)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {e}")

    def crop_image(self):
        if self.image_path is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        if not self.rect:
            messagebox.showerror("Error", "Please draw a rectangle.")
            return

        # Get the coordinates of the drawn rectangle
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # Crop the image using the coordinates of the drawn rectangle
        try:
            cropped_image = self.image.crop((x1, y1, x2, y2))

            # Display the cropped image on the Tkinter canvas
            photo = ImageTk.PhotoImage(cropped_image)
            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

            # Save the cropped image if needed
            cropped_image.save("output_cropped_image.jpg")

            # Remove the rectangle and preview image
            self.canvas.delete(self.rect)
            self.canvas.delete(self.preview_image)
        except Exception as e:
            messagebox.showerror("Error", f"Error cropping image: {e}")

    def on_press(self, event):
        # Get the starting coordinates of the rectangle
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # Remove any existing rectangle and preview image
        if self.rect:
            self.canvas.delete(self.rect)
        if self.preview_image:
            self.canvas.delete(self.preview_image)

        # Create a new rectangle
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_drag(self, event):
        # Update the coordinates of the rectangle as the user drags the mouse
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

        # Update the preview image dynamically
        preview_cropped_image = self.image.crop((self.start_x, self.start_y, cur_x, cur_y))
        preview_photo = ImageTk.PhotoImage(preview_cropped_image)

        # Display the preview image on the Tkinter canvas
        if self.preview_image:
            self.canvas.delete(self.preview_image)
        self.preview_image = self.canvas.create_image(self.start_x, self.start_y, anchor=tk.NW, image=preview_photo)
        self.canvas.preview_image = preview_photo

# Create the main application window
root = tk.Tk()
app = ImageCropperApp(root)

# Run the Tkinter main loop
root.mainloop()
