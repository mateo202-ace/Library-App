import os
import csv
import json
import random
from datetime import datetime
from typing import List, Dict, Optional
from .book import Book

class Library:
    def __init__(self, name: str, csv_file: str):
        self.name = name
        self.csv_file = csv_file
        self.json_file = csv_file.replace('.csv', '_extended.json')
        self.books = self.load_books()

    def load_books(self) -> List[Book]:
        books = []
        
        # Try to load from extended JSON first (has all new features)
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for book_data in data.get('books', []):
                        books.append(Book.from_dict(book_data))
                return books
            except Exception as e:
                print(f"⚠️ Error loading JSON file: {e}")
        
        # Fallback to CSV (legacy format)
        if os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Create book with legacy CSV format
                        book = Book(
                            title=row.get("Book Name:", "").strip(),
                            author=row.get("Author", "").strip(),
                            genre=row.get("Genre - Theme - Type", "").strip().split(" - "),
                            status=row.get("Status:", "To Be Read").strip(),
                            rating=int(row.get("Rating", 0)),
                            review=row.get("Review", ""),
                            total_pages=int(row.get("Total Pages", 0)),
                            pages_read=int(row.get("Pages Read", 0)),
                            date_started=row.get("Date Started", ""),
                            date_finished=row.get("Date Finished", ""),
                            reading_time_minutes=int(row.get("Reading Time", 0)),
                            isbn=row.get("ISBN", ""),
                            cover_url=row.get("Cover URL", "")
                        )
                        books.append(book)
                        
                # Save to new JSON format
                self.books = books
                self.save_books_to_json()
                        
            except KeyError as k:
                print(f"⚠️ Key error: {k} in CSV file. Using basic format.")
                # Try basic CSV format
                try:
                    with open(self.csv_file, newline="", encoding="utf-8") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            book = Book(
                                title=row["Book Name:"].strip(),
                                author=row["Author"].strip(),
                                genre=row["Genre - Theme - Type"].strip().split(" - "),
                                status=row["Status:"].strip(),
                            )
                            books.append(book)
                except Exception as e:
                    print(f"⚠️ Warning: {e}")
            except Exception as e:
                print(f"⚠️ Warning: {e}")
        
        if not books:
            print(f"⚠️ Warning: No book files found. Starting with an empty library")
            
        return books

    def save_books_to_json(self):
        try:
            data = {
                'library_name': self.name,
                'last_updated': datetime.now().isoformat(),
                'books': [book.to_dict() for book in self.books]
            }
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving books to JSON: {e}")

    def save_books_to_csv(self):
        # Keep CSV for backward compatibility
        try:
            with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
                fieldnames = [
                    "Book Name:", "Author", "Genre - Theme - Type", "Status:",
                    "Rating", "Review", "Total Pages", "Pages Read", 
                    "Date Started", "Date Finished", "Reading Time", "ISBN", "Cover URL"
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for book in self.books:
                    writer.writerow({
                        "Book Name:": book.title,
                        "Author": book.author,
                        "Genre - Theme - Type": " - ".join(book.genre),
                        "Status:": book.status,
                        "Rating": book.rating,
                        "Review": book.review,
                        "Total Pages": book.total_pages,
                        "Pages Read": book.pages_read,
                        "Date Started": book.date_started,
                        "Date Finished": book.date_finished,
                        "Reading Time": book.reading_time_minutes,
                        "ISBN": book.isbn,
                        "Cover URL": book.cover_url
                    })
        except Exception as e:
            print(f"⚠️ Error saving books to CSV: {e}")

    def save_books(self):
        self.save_books_to_json()
        self.save_books_to_csv()

    def add_book(self, book: Book):
        self.books.append(book)
        self.save_books()

    def remove_book(self, title: str) -> bool:
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def update_book(self, book: Book):
        self.save_books()

    def get_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def pick_random_book(self) -> str:
        to_be_read_books = [book for book in self.books if book.status == "To Be Read"]
        if to_be_read_books:
            return random.choice(to_be_read_books)
        else:
            return "📖 No books available!"

    def get_currently_reading(self) -> List[Book]:
        return [book for book in self.books if book.is_currently_reading()]

    def get_books_by_status(self, status: str) -> List[Book]:
        return [book for book in self.books if book.status == status]

    def get_books_by_rating(self, rating: int) -> List[Book]:
        return [book for book in self.books if book.rating == rating]

    def get_reading_statistics(self) -> Dict:
        total_books = len(self.books)
        finished_books = len([b for b in self.books if b.status == "Finished"])
        currently_reading = len(self.get_currently_reading())
        to_be_read = len([b for b in self.books if b.status == "To Be Read"])
        dnf_books = len([b for b in self.books if b.status == "Did Not Finish"])
        
        total_pages_read = sum(b.pages_read for b in self.books if b.pages_read > 0)
        total_reading_time = sum(b.reading_time_minutes for b in self.books)
        
        # Genre statistics
        genre_counts = {}
        for book in self.books:
            for genre in book.genre:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        # Rating statistics
        rated_books = [b for b in self.books if b.rating > 0]
        avg_rating = sum(b.rating for b in rated_books) / len(rated_books) if rated_books else 0
        
        return {
            'total_books': total_books,
            'finished_books': finished_books,
            'currently_reading': currently_reading,
            'to_be_read': to_be_read,
            'dnf_books': dnf_books,
            'total_pages_read': total_pages_read,
            'total_reading_time_hours': total_reading_time / 60,
            'genre_counts': genre_counts,
            'average_rating': avg_rating,
            'rated_books_count': len(rated_books)
        }

    def search_books(self, query: str) -> List[Book]:
        query_lower = query.lower()
        results = []
        for book in self.books:
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or
                any(query_lower in genre.lower() for genre in book.genre) or
                query_lower in book.review.lower()):
                results.append(book)
        return results

    def get_books_by_genre(self, genre: str) -> List[Book]:
        return [book for book in self.books if any(genre.lower() in g.lower() for g in book.genre)]

    def list_books(self) -> str:
        return "\n".join(str(book) for book in self.books) if self.books else "No books in this library"