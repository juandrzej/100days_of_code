import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermark Tool")
        self.root.geometry("800x600")

        # Variables
        self.original_image = None
        self.watermarked_image = None
        self.preview_image = None
        self.watermark_text = tk.StringVar(value="www.yourwebsite.com")
        self.watermark_position = tk.StringVar(value="bottom-right")
        self.watermark_opacity = tk.IntVar(value=128)
        self.watermark_size = tk.IntVar(value=36)
        self.watermark_color = "#FFFFFF"
        self.logo_path = None

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame, text="Image Watermark Tool", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Left panel for controls
        control_frame = ttk.LabelFrame(
            main_frame, text="Watermark Settings", padding="10"
        )
        control_frame.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10)
        )

        # Image upload section
        ttk.Label(control_frame, text="1. Upload Image:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        upload_btn = ttk.Button(
            control_frame, text="Browse Image", command=self.upload_image
        )
        upload_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Watermark type selection
        ttk.Label(control_frame, text="2. Watermark Type:").grid(
            row=2, column=0, sticky=tk.W, pady=(20, 5)
        )

        self.watermark_type = tk.StringVar(value="text")
        text_radio = ttk.Radiobutton(
            control_frame,
            text="Text",
            variable=self.watermark_type,
            value="text",
            command=self.toggle_watermark_type,
        )
        text_radio.grid(row=3, column=0, sticky=tk.W)

        logo_radio = ttk.Radiobutton(
            control_frame,
            text="Logo",
            variable=self.watermark_type,
            value="logo",
            command=self.toggle_watermark_type,
        )
        logo_radio.grid(row=4, column=0, sticky=tk.W)

        # Text watermark settings
        self.text_frame = ttk.LabelFrame(
            control_frame, text="Text Settings", padding="5"
        )
        self.text_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(self.text_frame, text="Text:").grid(row=0, column=0, sticky=tk.W)
        text_entry = ttk.Entry(
            self.text_frame, textvariable=self.watermark_text, width=20
        )
        text_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(self.text_frame, text="Font Size:").grid(
            row=2, column=0, sticky=tk.W, pady=(10, 0)
        )
        size_scale = ttk.Scale(
            self.text_frame,
            from_=12,
            to=72,
            variable=self.watermark_size,
            orient=tk.HORIZONTAL,
            command=self.update_preview,
        )
        size_scale.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)

        size_label = ttk.Label(self.text_frame, text="36")
        size_label.grid(row=4, column=0, sticky=tk.W)

        # Update size label when scale changes
        def update_size_label(*args):
            size_label.config(text=str(self.watermark_size.get()))

        self.watermark_size.trace("w", update_size_label)

        ttk.Label(self.text_frame, text="Color:").grid(
            row=5, column=0, sticky=tk.W, pady=(10, 0)
        )
        color_btn = ttk.Button(
            self.text_frame, text="Choose Color", command=self.choose_color
        )
        color_btn.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=2)

        # Logo watermark settings
        self.logo_frame = ttk.LabelFrame(
            control_frame, text="Logo Settings", padding="5"
        )
        self.logo_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=10)

        logo_btn = ttk.Button(
            self.logo_frame, text="Browse Logo", command=self.upload_logo
        )
        logo_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)

        self.logo_label = ttk.Label(self.logo_frame, text="No logo selected")
        self.logo_label.grid(row=1, column=0, sticky=tk.W, pady=2)

        # Common settings
        ttk.Label(control_frame, text="3. Position:").grid(
            row=7, column=0, sticky=tk.W, pady=(20, 5)
        )
        position_combo = ttk.Combobox(
            control_frame,
            textvariable=self.watermark_position,
            values=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
            state="readonly",
        )
        position_combo.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=2)
        position_combo.bind("<<ComboboxSelected>>", self.update_preview)

        ttk.Label(control_frame, text="4. Opacity:").grid(
            row=9, column=0, sticky=tk.W, pady=(20, 5)
        )
        opacity_scale = ttk.Scale(
            control_frame,
            from_=50,
            to=255,
            variable=self.watermark_opacity,
            orient=tk.HORIZONTAL,
            command=self.update_preview,
        )
        opacity_scale.grid(row=10, column=0, sticky=(tk.W, tk.E), pady=2)

        opacity_label = ttk.Label(control_frame, text="128")
        opacity_label.grid(row=11, column=0, sticky=tk.W)

        # Update opacity label when scale changes
        def update_opacity_label(*args):
            opacity_label.config(text=str(self.watermark_opacity.get()))

        self.watermark_opacity.trace("w", update_opacity_label)

        # Buttons
        preview_btn = ttk.Button(
            control_frame, text="Preview Watermark", command=self.update_preview
        )
        preview_btn.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=(20, 5))

        save_btn = ttk.Button(
            control_frame, text="Save Watermarked Image", command=self.save_image
        )
        save_btn.grid(row=13, column=0, sticky=(tk.W, tk.E), pady=5)

        # Right panel for image preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.image_label = ttk.Label(preview_frame, text="No image selected")
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        # Initially hide logo frame
        self.toggle_watermark_type()

    def toggle_watermark_type(self):
        if self.watermark_type.get() == "text":
            self.text_frame.grid()
            self.logo_frame.grid_remove()
        else:
            self.text_frame.grid_remove()
            self.logo_frame.grid()

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")],
        )

        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image)
                messagebox.showinfo("Success", "Image uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")

    def upload_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")],
        )

        if file_path:
            self.logo_path = file_path
            filename = os.path.basename(file_path)
            self.logo_label.config(text=f"Logo: {filename}")

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Watermark Color")
        if color[1]:
            self.watermark_color = color[1]
            self.update_preview()

    def display_image(self, image):
        # Resize image to fit in preview
        display_size = (400, 300)
        image_copy = image.copy()
        image_copy.thumbnail(display_size, Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(image_copy)
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo

    def get_watermark_position(self, image_size, watermark_size):
        img_width, img_height = image_size
        wm_width, wm_height = watermark_size

        positions = {
            "top-left": (20, 20),
            "top-right": (img_width - wm_width - 20, 20),
            "bottom-left": (20, img_height - wm_height - 20),
            "bottom-right": (img_width - wm_width - 20, img_height - wm_height - 20),
            "center": ((img_width - wm_width) // 2, (img_height - wm_height) // 2),
        }

        return positions.get(self.watermark_position.get(), positions["bottom-right"])

    def create_text_watermark(self, image):
        # Create a transparent overlay
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", self.watermark_size.get())
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", self.watermark_size.get())
            except:
                font = ImageFont.load_default()

        # Get text dimensions
        text = self.watermark_text.get()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate position
        position = self.get_watermark_position(image.size, (text_width, text_height))

        # Convert hex color to RGB and add alpha
        color = tuple(int(self.watermark_color[i : i + 2], 16) for i in (1, 3, 5))
        color_with_alpha = color + (self.watermark_opacity.get(),)

        # Draw text
        draw.text(position, text, font=font, fill=color_with_alpha)

        # Composite the overlay onto the original image
        watermarked = Image.alpha_composite(image.convert("RGBA"), overlay)
        return watermarked.convert("RGB")

    def create_logo_watermark(self, image):
        if not self.logo_path:
            messagebox.showerror("Error", "Please select a logo first!")
            return image

        try:
            # Open logo
            logo = Image.open(self.logo_path)

            # Convert to RGBA if not already
            if logo.mode != "RGBA":
                logo = logo.convert("RGBA")

            # Resize logo if it's too big (max 20% of image width)
            max_width = image.width // 5
            if logo.width > max_width:
                ratio = max_width / logo.width
                new_height = int(logo.height * ratio)
                logo = logo.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Apply opacity to logo
            logo_with_opacity = Image.new("RGBA", logo.size, (255, 255, 255, 0))
            for x in range(logo.width):
                for y in range(logo.height):
                    r, g, b, a = logo.getpixel((x, y))
                    if a > 0:  # Only modify non-transparent pixels
                        new_alpha = int(a * (self.watermark_opacity.get() / 255))
                        logo_with_opacity.putpixel((x, y), (r, g, b, new_alpha))

            # Calculate position
            position = self.get_watermark_position(image.size, logo.size)

            # Create composite image
            image_rgba = image.convert("RGBA")
            image_rgba.paste(logo_with_opacity, position, logo_with_opacity)

            return image_rgba.convert("RGB")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply logo watermark: {str(e)}")
            return image

    def update_preview(self, *args):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return

        try:
            if self.watermark_type.get() == "text":
                self.watermarked_image = self.create_text_watermark(self.original_image)
            else:
                self.watermarked_image = self.create_logo_watermark(self.original_image)

            self.display_image(self.watermarked_image)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create watermark: {str(e)}")

    def save_image(self):
        if not self.watermarked_image:
            messagebox.showwarning(
                "Warning", "Please create a watermark preview first!"
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Watermarked Image",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                self.watermarked_image.save(file_path, quality=95)
                messagebox.showinfo(
                    "Success", f"Image saved successfully to:\n{file_path}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

