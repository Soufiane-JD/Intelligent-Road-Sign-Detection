import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from DatabaseManager import DatabaseManager
import os
# Initialize Firebase Admin SDK
manager = DatabaseManager("database.json", "database.appspot.com")


# Tkinter App
class SignManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sign Management System')
        self.geometry('400x300')

        self.sign_id_label = tk.Label(self, text="Sign ID:")
        self.sign_id_label.grid(row=0, column=0)
        self.sign_id_entry = tk.Entry(self)
        self.sign_id_entry.grid(row=0, column=1)

        self.description_label = tk.Label(self, text="Description:")
        self.description_label.grid(row=1, column=0)
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=1, column=1)

        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_sign_image)
        self.upload_button.grid(row=2, column=0, columnspan=2)

        self.add_button = tk.Button(self, text="Add Sign", command=self.add_sign)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.get_button = tk.Button(self, text="Get Sign", command=self.display_sign)
        self.get_button.grid(row=4, column=0, columnspan=2)

        self.image_label = tk.Label(self)
        self.image_label.grid(row=5, column=0, columnspan=2)

    def upload_sign_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            blob_name = os.path.basename(file_path)
            url = manager.upload_image(file_path, blob_name)
            if url:
                messagebox.showinfo("Success", "Image uploaded successfully!")
                self.image_path = url
            else:
                messagebox.showerror("Error", "Failed to upload image.")

    def add_sign(self):
        sign_id = self.sign_id_entry.get().lower()
        description = self.description_entry.get()
        if hasattr(self, 'image_path'):
            image_path = self.image_path
            if manager.add_sign(sign_id, description, image_path):
                messagebox.showinfo("Success", "Sign added successfully!")
            else:
                messagebox.showerror("Error", "Failed to add sign.")
        else:
            messagebox.showwarning("Warning", "Please upload an image first.")

    def display_sign(self):
        sign_id = self.sign_id_entry.get().lower()
        sign = manager.get_sign(sign_id)
        if sign:
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, sign['description'])
            response = requests.get(sign['image_path'], stream=True)
            image = Image.open(response.raw)
            image = ImageTk.PhotoImage(image)
            self.image_label.config(image=image)
            self.image_label.image = image
        else:
            messagebox.showerror("Error", "Sign not found.")


if __name__ == "__main__":
    app = SignManagementApp()
    app.mainloop()
