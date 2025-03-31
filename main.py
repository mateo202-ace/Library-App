from hmac import new
from models.book import Book
from models.library import Library

# Path to the CSV file
csv_file = "/Users/juanmateo/Desktop/Library app/Library-App/data/books.csv"

# Create library and load books from the CSV file
my_library = Library("Andreas Library", csv_file)



def adding_books():
    booksyntax = ["Book Name", "Author", "Genre - Theme - Type", "Status"]
    newbook = []

    while True:
        print(f"this is the book formatting {booksyntax}" )
        enter_book = input("What book would you like to enter into your library (or Type 'exit' to exit): ")
        
        if enter_book == "exit":
            print("Come back any time to add more books!!!")
            break

        
        book_title = input("Book Title: ")
        book_author = input("Author: ")
        book_genre = input("Genre: ")

        valid_status = ["Status: To Be Read, Finished, Did Not Finish"]

        book_status = input("Status: ")
        if book_status not in valid_status:
            print("Invalid Status please set one of the provided statuses")

        
        newbook = [book_title, book_author, book_genre, book_status]
        my_library.add_book(newbook)



# print(my_library.list_books())

print("the next reandom book is..........:")
print(my_library.pick_random_book()) 

# print("the next reandom book is:")
# print(my_library.pick_random_book()) 