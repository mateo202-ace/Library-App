from hmac import new
from models.book import Book
from models.library import Library

# Path to the CSV file
csv_file = "/Users/juanmateo/Desktop/Library app/Library-App/data/books.csv"

# Create library and load books from the CSV file
my_library = Library("Andreas Library", csv_file)

books_to_add = [
    ("The Shadows", "Alex North", "Dark - Mysterious - Suspense", "To Be Read"),
    ("Baby X", "Kira Peikoff", "Thriller - Suspense - Dark", "To Be Read"),
    ("I Only Read Murder", "Ian Ferguson, Will Ferguson", "Mysterious - Suspense", "To Be Read"),
    ("What the Hell Did I Just Read", "David Wong, Jason Pargin", "Dark - Mysterious - Suspense", "To Be Read"),
    ("Sheets", "Brenna Thummler", "Moving - Young Adult reading", "To Be Read"),
    ("Delicates", "Brenna Thummler", "Moving - Young Adult reading", "To Be Read"),
    ("Uzumaki", "Junji Ito", "Dark - Mysterious - Suspense - Manga", "To Be Read"),
    ("The Nice House on the Lake Vol. 1", "James Tynion IV", "Horror - Suspense - Comic", "To Be Read"),
    ("The Nice House on the Lake Vol. 2", "James Tynion IV", "Horror - Suspense - Comic", "To Be Read"),
    ("Deadly Class Vol. 1: Reagan Youth", "Rick Remender", "Horror - Suspense - Comic", "To Be Read"),
    ("Deadly Class Vol. 2: Kids of the Black Hole", "Rick Remender", "Horror - Suspense - Comic", "To Be Read"),
    ("The Department of Truth #1", "James Tynion IV", "Horror - Suspense - Comic", "To Be Read"),
    ("The Department of Truth #2", "James Tynion IV", "Horror - Suspense - Comic", "To Be Read"),
]

# # Add each book to the library
# for title, author, genre, status in books_to_add:
#     genres = genre.split(" - ")  # Split genres into a list
#     new_book = Book(title, author, genres, status)
#     my_library.add_book(new_book)
#     print(f"✅ Added: {title} by {author}")

# List all books in the library to confirm they were added
#print("\nBooks in the library:")
print(my_library.list_books())

results = my_library.move_to_dnf_list()
print(results)

# print("the next reandom book is..........:")
# print(my_library.pick_random_book()) 

# print("the next reandom book is:")
# print(my_library.pick_random_book()) 