import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import cv2
from PIL import Image
from PIL import ImageTk

from image_processing import (
    read_image,
    preprocess_image
)

from ocr_engine import (
    extract_text,
    detect_text_boxes
)


class OCRApplication:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI Image & Text Recognition System"
        )

        self.root.geometry(
            "1100x700"
        )

        self.root.configure(
            bg="white"
        )

        self.image_path = None
        self.original_image = None

        self.create_title()

        self.create_buttons()

        self.create_image_area()

        self.create_text_area()


    # --------------------------------
    # TITLE
    # --------------------------------

    def create_title(self):

        title = tk.Label(
            self.root,
            text="AI IMAGE & TEXT RECOGNITION",
            font=("Arial", 22, "bold"),
            bg="white"
        )

        title.pack(
            pady=15
        )


    # --------------------------------
    # BUTTONS
    # --------------------------------

    def create_buttons(self):

        button_frame = tk.Frame(
            self.root,
            bg="white"
        )

        button_frame.pack(
            pady=10
        )


        upload_button = tk.Button(
            button_frame,
            text="Upload Image",
            command=self.upload_image,
            width=15,
            height=2
        )

        upload_button.grid(
            row=0,
            column=0,
            padx=5
        )


        recognize_button = tk.Button(
            button_frame,
            text="Recognize Text",
            command=self.recognize_text,
            width=15,
            height=2
        )

        recognize_button.grid(
            row=0,
            column=1,
            padx=5
        )


        detect_button = tk.Button(
            button_frame,
            text="Detect Text Boxes",
            command=self.detect_boxes,
            width=15,
            height=2
        )

        detect_button.grid(
            row=0,
            column=2,
            padx=5
        )


        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            width=15,
            height=2
        )

        clear_button.grid(
            row=0,
            column=3,
            padx=5
        )


        save_button = tk.Button(
            button_frame,
            text="Save Text",
            command=self.save_text,
            width=15,
            height=2
        )

        save_button.grid(
            row=0,
            column=4,
            padx=5
        )


    # --------------------------------
    # IMAGE AREA
    # --------------------------------

    def create_image_area(self):

        self.image_label = tk.Label(
            self.root,
            text="Image Preview",
            width=60,
            height=15,
            bg="lightgray"
        )

        self.image_label.pack(
            pady=10
        )


    # --------------------------------
    # TEXT AREA
    # --------------------------------

    def create_text_area(self):

        text_frame = tk.Frame(
            self.root,
            bg="white"
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        self.text_box = tk.Text(
            text_frame,
            wrap="word",
            font=("Arial", 13)
        )

        self.text_box.pack(
            fill="both",
            expand=True
        )


    # --------------------------------
    # UPLOAD IMAGE
    # --------------------------------

    def upload_image(self):

        path = filedialog.askopenfilename(

            title="Select Image",

            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png"),
                ("All Files", "*.*")
            ]
        )


        if path == "":
            return


        self.image_path = path

        self.original_image = cv2.imread(
            path
        )


        if self.original_image is None:

            messagebox.showerror(
                "Error",
                "Unable to load image"
            )

            return


        self.display_image(
            self.original_image
        )


    # --------------------------------
    # DISPLAY IMAGE
    # --------------------------------

    def display_image(self, image):

        image_rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        pil_image = Image.fromarray(
            image_rgb
        )


        pil_image.thumbnail(
            (800, 350)
        )


        photo = ImageTk.PhotoImage(
            pil_image
        )


        self.image_label.configure(
            image=photo,
            text=""
        )


        self.image_label.image = photo


    # --------------------------------
    # OCR
    # --------------------------------

    def recognize_text(self):

        if self.image_path is None:

            messagebox.showwarning(
                "Warning",
                "Please upload an image first"
            )

            return


        try:

            image = read_image(
                self.image_path
            )


            processed = preprocess_image(
                image
            )


            text = extract_text(
                processed
            )


            self.text_box.delete(
                "1.0",
                tk.END
            )


            self.text_box.insert(
                tk.END,
                text
            )


        except Exception as error:

            messagebox.showerror(
                "OCR Error",
                str(error)
            )


    # --------------------------------
    # DETECT BOXES
    # --------------------------------

    def detect_boxes(self):

        if self.image_path is None:

            messagebox.showwarning(
                "Warning",
                "Please upload an image"
            )

            return


        try:

            image = read_image(
                self.image_path
            )


            boxes = detect_text_boxes(
                image
            )


            output = image.copy()


            for box in boxes:

                x = box["x"]
                y = box["y"]

                w = box["width"]
                h = box["height"]

                cv2.rectangle(
                    output,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )


                cv2.putText(
                    output,
                    box["text"],
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1
                )


            self.display_image(
                output
            )


        except Exception as error:

            messagebox.showerror(
                "Detection Error",
                str(error)
            )


    # --------------------------------
    # SAVE TEXT
    # --------------------------------

    def save_text(self):

        text = self.text_box.get(
            "1.0",
            tk.END
        )


        if text.strip() == "":

            messagebox.showwarning(
                "Warning",
                "No text available"
            )

            return


        path = filedialog.asksaveasfilename(

            defaultextension=".txt",

            filetypes=[
                ("Text File", "*.txt")
            ]
        )


        if path:

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(text)


            messagebox.showinfo(
                "Success",
                "Text saved successfully"
            )


    # --------------------------------
    # CLEAR
    # --------------------------------

    def clear_all(self):

        self.image_path = None

        self.original_image = None


        self.image_label.configure(
            image="",
            text="Image Preview"
        )


        self.text_box.delete(
            "1.0",
            tk.END
        )


# --------------------------------
# RUN APPLICATION
# --------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    application = OCRApplication(
        root
    )

    root.mainloop()