from models.book import Book
from models.library import Library

# Path to the CSV file
csv_file = "/Users/juanmateo/Desktop/Library app/Library-App/data/books.csv"

# Create library and load books from the CSV file
my_library = Library("Andreas Library", csv_file)
# new_book = ("", "Paulo Coelho", ["Adventure"], "Available")


# print(my_library.list_books())

print("the next reandom book is..........:")
print(my_library.pick_random_book()) 

# print("the next reandom book is:")
# print(my_library.pick_random_book()) 