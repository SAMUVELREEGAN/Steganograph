from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from stegano import lsb

# Create the main application window
root = Tk()
root.title("Steganography Tool")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

# Global variables
image_preview = None
canvas_file_path = None  # Global variable to store file path for canvas

# Function to open an image
def open_image():
    global image_preview, canvas_file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_path:
        return

    # Open the image
    image = Image.open(file_path)

    # Resize the image to fit within 300x300 box
    max_size = (300, 300)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)  # Resize image maintaining aspect ratio

    # Convert image to ImageTk format
    img = ImageTk.PhotoImage(image)

    # Update the image label with the opened image
    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.image = img  # Store the reference to avoid garbage collection
    canvas_file_path = file_path  # Store the file path for later use

    # Enable Hide Data button
    hide_data_button.config(state=NORMAL)

# Function to open a text file
def open_text_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            message_box.delete("1.0", END)
            message_box.insert(END, content)

# Function to hide data in an image
def hide_data():
    global canvas_file_path
    message = message_box.get("1.0", END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message to hide.")
        return

    if canvas_file_path:  # For images
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not save_path:
            return
        try:
            lsb.hide(canvas_file_path, message).save(save_path)
            messagebox.showinfo("Success", "Message hidden successfully in the image!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Function to show data from an image
def show_data():
    global canvas_file_path
    if canvas_file_path:  # For images
        try:
            hidden_message = lsb.reveal(canvas_file_path)
            if hidden_message:
                message_box.delete("1.0", END)
                message_box.insert(END, hidden_message)
            else:
                message_box.delete("1.0", END)
                message_box.insert(END, "No hidden message found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Header Label
header_label = Label(root, text="Steganography Mini Project", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
header_label.pack(pady=20)

# Canvas for displaying the image with fixed size (300x300)
canvas_frame = Frame(root, bg="#f0f0f0", relief=RIDGE, borderwidth=2)
canvas = Canvas(canvas_frame, width=300, height=200)
canvas.pack()
canvas_frame.pack(pady=20)

# Single Text Box for both entering and displaying messages
message_label = Label(root, text="Message Box:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
message_label.pack(pady=10)

message_box = Text(root, height=8, width=60, font=("Arial", 12), wrap=WORD, relief=SOLID, borderwidth=1)
message_box.pack(pady=10)

# Buttons for main actions
button_frame = Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

open_image_button = Button(button_frame, text="Open Image", command=open_image, bg="#4CAF50", fg="white", font=("Arial", 12), width=15)
open_image_button.grid(row=0, column=0, padx=10, pady=5)

open_text_file_button = Button(button_frame, text="Open Text File", command=open_text_file, bg="#FF5722", fg="white", font=("Arial", 12), width=15)
open_text_file_button.grid(row=0, column=1, padx=10, pady=5)

hide_data_button = Button(button_frame, text="Hide Data", command=hide_data, bg="#2196F3", fg="white", font=("Arial", 12), width=15, state=NORMAL)
hide_data_button.grid(row=1, column=0, padx=10, pady=5)

show_data_button = Button(button_frame, text="Show Data", command=show_data, bg="#FF9800", fg="white", font=("Arial", 12), width=15)
show_data_button.grid(row=1, column=1, padx=10, pady=5)

# Footer Label
footer_label = Label(root, text="Developed by Vimal Raj", font=("Arial", 10), bg="#f0f0f0", fg="#666")
footer_label.pack(pady=10)

# Start the application
root.mainloop()
