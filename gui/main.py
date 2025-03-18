
from models.book import Book
from models.library import Library
import tkinter as tk
from tkinter import messagebox

# Create library and load books
my_library = Library("Andreas Library")

def list_books():
    books = my_library.list_dnf_list()
    books_str = "\n".join(books)
    messagebox.showinfo("Books in Library", books_str)

# Create the main window
root = tk.Tk()
root.title("Book Library")

# Create a button to list books
list_books_button = tk.Button(root, text="List Books", command=list_books)
list_books_button.pack(pady=20)

# Run the application
root.mainloop()