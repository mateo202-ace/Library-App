from datetime import datetime
from typing import List, Optional

class Book:
    def __init__(self, title: str, author: str, genre: List[str], status: str = "To Be Read", 
                 rating: int = 0, review: str = "", total_pages: int = 0, 
                 pages_read: int = 0, date_started: str = "", date_finished: str = "",
                 reading_time_minutes: int = 0, isbn: str = "", cover_url: str = ""):
        self.title = title
        self.author = author
        self.genre = genre if isinstance(genre, list) else [genre]
        self.status = status
        self.rating = rating  # 0-5 stars
        self.review = review
        self.total_pages = total_pages
        self.pages_read = pages_read
        self.date_started = date_started
        self.date_finished = date_finished
        self.reading_time_minutes = reading_time_minutes
        self.isbn = isbn
        self.cover_url = cover_url

    def mark_as_finished(self, finish_date: str = None):
        self.status = "Finished"
        if finish_date:
            self.date_finished = finish_date
        else:
            self.date_finished = datetime.now().strftime("%Y-%m-%d")
        if self.total_pages > 0:
            self.pages_read = self.total_pages

    def mark_as_to_be_read(self):
        self.status = "To Be Read"
        self.date_started = ""
        self.date_finished = ""
        self.pages_read = 0

    def mark_as_dnf(self, dnf_date: str = None):
        self.status = "Did Not Finish"
        if dnf_date:
            self.date_finished = dnf_date
        else:
            self.date_finished = datetime.now().strftime("%Y-%m-%d")
    
    def start_reading(self, start_date: str = None):
        if start_date:
            self.date_started = start_date
        else:
            self.date_started = datetime.now().strftime("%Y-%m-%d")
    
    def update_progress(self, pages_read: int, reading_time_minutes: int = 0):
        self.pages_read = min(pages_read, self.total_pages) if self.total_pages > 0 else pages_read
        self.reading_time_minutes += reading_time_minutes
    
    def set_rating(self, rating: int):
        self.rating = max(0, min(5, rating))  # Ensure rating is between 0-5
    
    def set_review(self, review: str):
        self.review = review
    
    def get_progress_percentage(self) -> float:
        if self.total_pages <= 0:
            return 0.0
        return min(100.0, (self.pages_read / self.total_pages) * 100)
    
    def get_reading_time_hours(self) -> float:
        return self.reading_time_minutes / 60.0 if self.reading_time_minutes > 0 else 0.0
    
    def is_currently_reading(self) -> bool:
        return self.date_started != "" and self.date_finished == "" and self.status not in ["Finished", "Did Not Finish"]

    def __str__(self):
        progress = f" ({self.get_progress_percentage():.1f}%)" if self.total_pages > 0 else ""
        rating_stars = "★" * self.rating + "☆" * (5 - self.rating) if self.rating > 0 else "No rating"
        return f"{self.title} by {self.author} | {' • '.join(self.genre)} | {self.status}{progress} | {rating_stars}"
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'genre': ' - '.join(self.genre),
            'status': self.status,
            'rating': self.rating,
            'review': self.review,
            'total_pages': self.total_pages,
            'pages_read': self.pages_read,
            'date_started': self.date_started,
            'date_finished': self.date_finished,
            'reading_time_minutes': self.reading_time_minutes,
            'isbn': self.isbn,
            'cover_url': self.cover_url
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get('title', ''),
            author=data.get('author', ''),
            genre=data.get('genre', '').split(' - ') if data.get('genre') else [],
            status=data.get('status', 'To Be Read'),
            rating=int(data.get('rating', 0)),
            review=data.get('review', ''),
            total_pages=int(data.get('total_pages', 0)),
            pages_read=int(data.get('pages_read', 0)),
            date_started=data.get('date_started', ''),
            date_finished=data.get('date_finished', ''),
            reading_time_minutes=int(data.get('reading_time_minutes', 0)),
            isbn=data.get('isbn', ''),
            cover_url=data.get('cover_url', '')
        )
