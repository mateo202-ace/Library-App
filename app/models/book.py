# this class stores book info and sees if it as been read or not and has an easy print string


class Book:
    def __init__(self, title, author, genre, status="To Be Read"):
        # Initializes a book object

        self.title = title
        self.author = author
        self.genre = (
            genre if isinstance(genre, list) else [genre]
        )  # Ensures genre is always a list
        self.status = status

    def mark_as_finished(self):
        # marks book as unread
        self.status = "Finished"

    def mark_as_to_be_read(self):
        self.status = "To Be Read"

    def mark_as_dnf(self):
        self.status = "Did Not Finished"

    def __str__(self):
        status = f"Status [{self.status}]"
        return f"{self.title} by {self.author} Its a:{self.genre} {status}"
