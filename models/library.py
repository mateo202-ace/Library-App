import os
import csv
import random
from models.book import Book

class Library:

    def __init__(self, name, csv_file="C:\\Users\\juan.mateo\\Security-Projects\\Security-Projects\\book-Library\\data\\books.csv"):
        # initializes a library, creates the name and the empty library

        self.name = name
        self.csv_file = csv_file
        self.books = self.load_books()  # Auto loads books on startup

    def load_books(self):
        # loads books from a CSV file into the library
        books = []
        if not os.path.exists(self.csv_file):
            print(f"⚠️ Warning: {self.csv_file} not found. Starting with an empty library")
            return books

        try:
            with open(self.csv_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(
                        row["Book Name:"].strip(),
                        row["Author"].strip(),
                        row["Genre - Theme - Type"].strip().split(" - "),  # Convert Genre into a list
                        row["Status:"].strip(),
                    )
                    books.append(book)

        except KeyError as k:
            print(f"⚠️ Key error: {k} in CSV file.")
        except Exception as e:
            print(f"⚠️ Warning: {e}")

        return books

    def save_books_to_csv(self):
        # Saves the current books list to the CSV file
        try:
            with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
                fieldnames = ["Book Name:", "Author", "Genre - Theme - Type", "Status:"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for book in self.books:
                    writer.writerow(
                        {
                            "Book Name:": book.title,
                            "Author": book.author,
                            "Genre - Theme - Type": " - ".join(book.genre),
                            "Status:": book.status,
                        }
                    )
        except Exception as e:
            print(f"⚠️ Error saving books to CSV: {e}")

    def add_book(self, book):
        # adds a book to the library
        self.books.append(book)
        self.save_books_to_csv()

    def remove_book(self, title):
        # loops through the Library Removes book by title

        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                self.save_books_to_csv()
                return True
        return False

    def move_to_dnf_list(self):
        # looks for books in main Library that are DID NOT FINISH and moved them to a DNF lsit and removes them from main libarys
        did_not_finish = [book for book in self.books if book.status == "Did not Finished"]

        if not did_not_finish:
            return "No books that you did not finish"

        dnf_csv_file = "C:\\Users\\juan.mateo\\Security-Projects\\Security-Projects\\book-Library\\data\\dnf_books.csv"

        # saves DNF books to new CSV file
        try:
            with open(dnf_csv_file, "w", newline="", encoding="utf-8") as file:
                fieldnames = ["Book Name:", "Author", "Genre - Theme - Type", "Status:"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for book in did_not_finish:
                    writer.writerow(
                        {
                            "Book Name:": book.title,
                            "Author": book.author,
                            "Genre - Theme - Type": " - ".join(book.genre),
                            "Status:": book.status,
                        }
                    )
            # Removes book from main library
            self.books = [book for book in self.books if book.status != "Did not Finished"]
            self.save_books_to_csv()

        except Exception as e:
            return f"⚠️ Error saving DNF books: {e}"

        return f"Moved {len(did_not_finish)} book(s) to the DNF list."

    def pick_random_book(self):
        # filters through books and checks which ones are marked To Be Read
        to_be_read_books = [book for book in self.books if book.status == "To Be Read"]
        if to_be_read_books:
            return random.choice(to_be_read_books)
        else:
            return "📖 No books available!"

    def list_books(self):
        # list books on readable format
        return "\n".join(str(book) for book in self.books) if self.books else "No books in this library"

    def list_dnf_list(self):
        # lists books in the DNF library
        dnf_csv_file = "C:\\Users\\juan.mateo\\Security-Projects\\Security-Projects\\book-Library\\data\\dnf_books.csv"

        if not os.path.exists(dnf_csv_file):
            return "No DNF books Recorded"

        books = []
        try:
            with open(dnf_csv_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(
                        row["Book Name:"].strip(),
                        row["Author"].strip(),
                        row["Genre - Theme - Type"].strip().split(" - "),
                        row["Status:"].strip(),
                    )
                    books.append(book)
        except Exception as e:
            return f"⚠️ Error reading DNF books: {e}"

        return ("\n".join(str(book) for book in books) if books else "No books in the DNF list.")


