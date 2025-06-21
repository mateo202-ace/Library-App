import requests
import json
from typing import Dict, Optional, List

class BookAPI:
    @staticmethod
    def lookup_isbn(isbn: str) -> Optional[Dict]:
        """
        Look up book information by ISBN using Open Library API
        """
        try:
            # Clean ISBN
            isbn = isbn.replace('-', '').replace(' ', '')
            
            # Try Open Library API
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                isbn_key = f"ISBN:{isbn}"
                
                if isbn_key in data:
                    book_data = data[isbn_key]
                    
                    # Extract information
                    title = book_data.get('title', '')
                    authors = [author.get('name', '') for author in book_data.get('authors', [])]
                    author = ', '.join(authors) if authors else ''
                    
                    # Get cover image
                    cover_url = ''
                    if 'cover' in book_data and 'large' in book_data['cover']:
                        cover_url = book_data['cover']['large']
                    elif 'cover' in book_data and 'medium' in book_data['cover']:
                        cover_url = book_data['cover']['medium']
                    
                    # Get page count
                    pages = book_data.get('number_of_pages', 0)
                    
                    # Get subjects as genres
                    subjects = book_data.get('subjects', [])
                    genres = [subject.get('name', '') for subject in subjects[:5]]  # Limit to 5 genres
                    
                    return {
                        'title': title,
                        'author': author,
                        'isbn': isbn,
                        'pages': pages,
                        'cover_url': cover_url,
                        'genres': genres if genres else ['Unknown']
                    }
            
            # Fallback to Google Books API
            return BookAPI.lookup_google_books(isbn)
            
        except Exception as e:
            print(f"Error looking up ISBN {isbn}: {e}")
            return None
    
    @staticmethod
    def lookup_google_books(isbn: str) -> Optional[Dict]:
        """
        Fallback to Google Books API
        """
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('totalItems', 0) > 0:
                    book = data['items'][0]['volumeInfo']
                    
                    title = book.get('title', '')
                    authors = book.get('authors', [])
                    author = ', '.join(authors) if authors else ''
                    
                    # Get cover image
                    cover_url = ''
                    if 'imageLinks' in book:
                        cover_url = book['imageLinks'].get('large', 
                                   book['imageLinks'].get('medium', 
                                   book['imageLinks'].get('thumbnail', '')))
                    
                    pages = book.get('pageCount', 0)
                    genres = book.get('categories', ['Unknown'])
                    
                    return {
                        'title': title,
                        'author': author,
                        'isbn': isbn,
                        'pages': pages,
                        'cover_url': cover_url,
                        'genres': genres
                    }
            
        except Exception as e:
            print(f"Error with Google Books API for ISBN {isbn}: {e}")
            
        return None

    @staticmethod
    def search_books(query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for books by title/author
        """
        try:
            # Use Google Books API for search
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('items', []):
                    book = item['volumeInfo']
                    
                    # Get ISBN
                    isbn = ''
                    for identifier in book.get('industryIdentifiers', []):
                        if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                            isbn = identifier.get('identifier', '')
                            break
                    
                    result = {
                        'title': book.get('title', ''),
                        'author': ', '.join(book.get('authors', [])),
                        'isbn': isbn,
                        'pages': book.get('pageCount', 0),
                        'cover_url': book.get('imageLinks', {}).get('thumbnail', ''),
                        'genres': book.get('categories', ['Unknown'])
                    }
                    results.append(result)
                
                return results
                
        except Exception as e:
            print(f"Error searching books: {e}")
            
        return []