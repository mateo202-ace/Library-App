from hmac import new
from models.book import Book
from models.library import Library

# Path to the CSV file
csv_file = "/Users/juanmateo/Desktop/Library app/Library-App/data/books.csv"

# Create library and load books from the CSV file
my_library = Library("Andreas Library", csv_file)

books_to_add = [
    ("The Deepest Lake", "Andromeda Romano-Lax", "Dark - Mysterious - Thriller", "To Be Read"),
    ("NightWatching", "Tracy Sierra", "Thriller - Mystery", "To Be Read"),
    ("Listen For The Lie", "Amy Tintera", "Mysterious - Thriller", "To Be Read"),
    ("Midnight at the Bright Ideas Bookstore", "Matthew Sullivan", "Dark - Mysterious", "To Be Read"),
    ("Serial Killer Support Group", "Saratoga Schaefer", "Mysterious - Thriller - Suspense", "To Be Read"),
    ("Home is Where the Bodies Are", "Jeneva Rose", "Mysterious - Thriller - Suspense", "To Be Read"),
]

# # Add each book to the library
#for title, author, genre, status in books_to_add:
    #genres = genre.split(" - ")  # Split genres into a list
    #new_book = Book(title, author, genres, status)
    #my_library.add_book(new_book)
    #print(f"✅ Added: {title} by {author}")

# List all books in the library to confirm they were added
#print("\nBooks in the library:")
#print(my_library.list_books())

#results = my_library.move_to_dnf_list()
#print(results)

print("the next reandom book is..........:")
print(my_library.pick_random_book()) 

# print("the next reandom book is:")
# print(my_library.pick_random_book()) 