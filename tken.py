import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import messagebox

# Path to Tesseract executable (replace with your path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract_executable>'

def read_id_card(image_path):
    # Load the image
    image = Image.open(image_path)
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image)
    return text

def fill_form(data):
    # Create a simple form using tkinter
    root = tk.Tk()
    root.title("ID Card Form")
    
    # Function to submit the form
    def submit_form():
        # Display a message box with the form data
        messagebox.showinfo("Form Data", f"Form submitted with data:\n\n{data}")
        root.destroy()
    
    # Display the extracted data in a text widget
    text_widget = tk.Text(root)
    text_widget.insert(tk.END, data)
    text_widget.pack()
    
    # Submit button
    submit_button = tk.Button(root, text="Submit", command=submit_form)
    submit_button.pack()
    
    root.mainloop()

# Example usage
image_path = 'path_to_your_id_card_image.jpg'
data = read_id_card(image_path)
fill_form(data)
