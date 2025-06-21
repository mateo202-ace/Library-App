import flet as ft
import os
import sys
from datetime import datetime
from typing import Optional

# Add src to path
sys.path.append('src')
from models.book import Book
from models.library import Library
from utils.book_api import BookAPI
from utils.export_utils import export_to_csv, export_reading_report, export_to_json

class ReadWiseApp:
    def __init__(self):
        self.csv_file = "/Users/juanmateo/Desktop/Library app/ReadWise/src/data/books.csv"
        self.dnf_csv_file = "/Users/juanmateo/Desktop/Library app/ReadWise/src/data/dnf_books.csv"
        self.library = Library("ReadWise Library", self.csv_file, self.dnf_csv_file)
        self.selected_book: Optional[Book] = None
        self.current_view = "library"
        
    def main(self, page: ft.Page):
        page.title = "📚 ReadWise - Smart Reading Management"
        page.window.width = 1400
        page.window.height = 900
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        
        # Create main components
        self.create_components(page)
        
        # Navigation rail (same as enhanced version but renamed)
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.LIBRARY_BOOKS_OUTLINED,
                    selected_icon=ft.Icons.LIBRARY_BOOKS,
                    label="Library"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CLOSE_OUTLINED,
                    selected_icon=ft.Icons.CLOSE,
                    label="DNF Books"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    selected_icon=ft.Icons.ANALYTICS,
                    label="Statistics"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.IMPORT_EXPORT_OUTLINED,
                    selected_icon=ft.Icons.IMPORT_EXPORT,
                    label="Import/Export"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings"
                ),
            ],
            on_change=self.nav_change,
        )
        
        # Content area
        self.content_area = ft.Container(expand=True)
        
        # Main layout
        page.add(
            ft.Row([
                self.nav_rail,
                ft.VerticalDivider(width=1),
                self.content_area,
            ], expand=True)
        )
        
        # Show library view initially
        self.show_library_view_without_refresh()
        page.update()
        self.refresh_book_list()
        
    def create_components(self, page):
        # Book list
        self.book_list = ft.ListView(expand=1, spacing=10, padding=20)
        
        # Search and filters
        self.search_field = ft.TextField(
            label="Search books...",
            width=300,
            on_change=self.search_books,
            prefix_icon=ft.Icons.SEARCH,
        )
        
        self.status_filter = ft.Dropdown(
            label="Status",
            width=150,
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("To Be Read"),
                ft.dropdown.Option("Finished"),
                ft.dropdown.Option("Did Not Finish"),
                ft.dropdown.Option("Currently Reading"),
            ],
            value="All",
            on_change=self.filter_books,
        )
        
        self.rating_filter = ft.Dropdown(
            label="Rating",
            width=120,
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("5 ★"),
                ft.dropdown.Option("4 ★"),
                ft.dropdown.Option("3 ★"),
                ft.dropdown.Option("2 ★"),
                ft.dropdown.Option("1 ★"),
                ft.dropdown.Option("Unrated"),
            ],
            value="All",
            on_change=self.filter_books,
        )
        
        # Add/Edit book dialog components
        self.create_book_dialog_components(page)
        
    def create_book_dialog_components(self, page):
        self.title_field = ft.TextField(label="Book Title", width=400)
        self.author_field = ft.TextField(label="Author", width=400)
        self.genre_field = ft.TextField(label="Genres (separate with ' - ')", width=400)
        self.isbn_field = ft.TextField(label="ISBN (optional)", width=400)
        self.total_pages_field = ft.TextField(label="Total Pages", width=200, value="0")
        
        self.status_dropdown = ft.Dropdown(
            label="Status",
            width=200,
            options=[
                ft.dropdown.Option("To Be Read"),
                ft.dropdown.Option("Finished"),
                ft.dropdown.Option("Did Not Finish"),
            ],
            value="To Be Read",
        )
        
        # Rating
        self.rating_slider = ft.Slider(
            min=0, max=5, divisions=5, value=0,
            label="Rating: {value} stars",
            width=300
        )
        
        # Review
        self.review_field = ft.TextField(
            label="Review/Notes",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=400
        )
        
        self.add_book_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add New Book"),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([self.title_field]),
                    ft.Row([self.author_field]),
                    ft.Row([self.genre_field]),
                    ft.Row([self.isbn_field, ft.ElevatedButton("Lookup ISBN", on_click=self.lookup_isbn)]),
                    ft.Row([self.total_pages_field, self.status_dropdown]),
                    ft.Row([self.rating_slider]),
                    ft.Row([self.review_field]),
                ], tight=True),
                width=500,
                height=400,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_add_dialog),
                ft.ElevatedButton("Add Book", on_click=self.add_book),
            ],
        )
        
        page.overlay.append(self.add_book_dialog)
    
    def nav_change(self, e):
        """Handle navigation changes"""
        selected_index = e.control.selected_index
        
        if selected_index == 0:
            self.current_view = "library"
            self.show_library_view()
        elif selected_index == 1:
            self.current_view = "dnf"
            self.show_dnf_view()
        elif selected_index == 2:
            self.current_view = "statistics"
            self.show_statistics_view()
        elif selected_index == 3:
            self.current_view = "import_export"
            self.show_import_export_view()
        elif selected_index == 4:
            self.current_view = "settings"
            self.show_settings_view()
            
        self.content_area.page.update()
    
    def show_library_view_without_refresh(self):
        """Set up library view without refreshing book list"""
        header = ft.Container(
            content=ft.Column([
                ft.Text("📚 My Library", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([
                    self.search_field,
                    self.status_filter,
                    self.rating_filter,
                    ft.ElevatedButton(
                        "Add Book",
                        icon=ft.Icons.ADD,
                        on_click=self.show_add_book_dialog,
                    ),
                ], spacing=10),
            ], spacing=10),
            padding=20,
            margin=ft.margin.only(bottom=10)
        )
        
        self.content_area.content = ft.Column([
            header,
            ft.Container(content=self.book_list, expand=True)
        ])
    
    def show_library_view(self):
        """Show library view and refresh"""
        self.show_library_view_without_refresh()
        self.refresh_book_list()
    
    def show_dnf_view(self):
        """Show DNF books"""
        dnf_books = self.library.dnf_books
        
        header = ft.Container(
            content=ft.Column([
                ft.Text("📖 Did Not Finish", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(f"{len(dnf_books)} books you didn't finish", size=16, color=ft.Colors.GREY_600),
                ft.Divider(),
            ], spacing=10),
            padding=20,
            margin=ft.margin.only(bottom=10)
        )
        
        dnf_list = ft.ListView(expand=1, spacing=10, padding=20)
        
        for book in dnf_books:
            dnf_list.controls.append(self.create_book_card(book))
        
        if not dnf_books:
            dnf_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=64, color=ft.Colors.GREEN),
                        ft.Text("No DNF books!", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("You finish everything you start!", size=14, color=ft.Colors.GREY_600),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        
        self.content_area.content = ft.Column([
            header,
            ft.Container(content=dnf_list, expand=True)
        ])
    
    def show_statistics_view(self):
        """Show reading statistics"""
        stats = self.library.get_reading_statistics()
        
        # Create stat cards
        stat_cards = ft.Row([
            self.create_stat_card("Total Books", str(stats['total_books']), ft.Icons.LIBRARY_BOOKS),
            self.create_stat_card("Finished", str(stats['finished_books']), ft.Icons.CHECK_CIRCLE),
            self.create_stat_card("Currently Reading", str(stats['currently_reading']), ft.Icons.MENU_BOOK),
            self.create_stat_card("DNF Books", str(stats['dnf_books']), ft.Icons.CLOSE),
        ], spacing=20)
        
        # Genre breakdown
        sorted_genres = sorted(stats['genre_counts'].items(), key=lambda x: x[1], reverse=True)[:10]
        genre_list = ft.Column([
            ft.Row([
                ft.Text(genre, size=14),
                ft.Container(expand=True),
                ft.Text(f"{count} books", size=14, color=ft.Colors.BLUE),
            ]) for genre, count in sorted_genres
        ])
        
        self.content_area.content = ft.Column([
            ft.Container(
                content=ft.Text("📊 Reading Statistics", size=28, weight=ft.FontWeight.BOLD),
                padding=20,
                margin=ft.margin.only(bottom=20)
            ),
            stat_cards,
            ft.Container(height=20),
            ft.Container(
                content=ft.Column([
                    ft.Text("📚 Top Genres", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    genre_list,
                ]),
                padding=20,
            ),
        ], scroll=ft.ScrollMode.AUTO)
    
    def show_import_export_view(self):
        """Show import/export options"""
        self.content_area.content = ft.Container(
            content=ft.Column([
                ft.Text("📤 Import/Export", size=28, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        "Export to CSV",
                        icon=ft.Icons.DOWNLOAD,
                        on_click=self.export_csv,
                    ),
                    ft.ElevatedButton(
                        "Export Reading Report",
                        icon=ft.Icons.DESCRIPTION,
                        on_click=self.export_report,
                    ),
                    ft.ElevatedButton(
                        "Export to JSON",
                        icon=ft.Icons.CODE,
                        on_click=self.export_json,
                    ),
                ], spacing=10),
            ]),
            padding=40,
        )
    
    def show_settings_view(self):
        """Show settings"""
        self.content_area.content = ft.Container(
            content=ft.Column([
                ft.Text("⚙️ Settings", size=28, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.Text("ReadWise - Smart Reading Management", size=18),
                ft.Text("Version 2.0", size=14, color=ft.Colors.GREY_600),
            ]),
            padding=40,
        )
    
    def create_stat_card(self, title: str, value: str, icon):
        """Create a statistics card"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=32, color=ft.Colors.BLUE),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                ft.Text(title, size=14),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            width=200,
            height=120,
            alignment=ft.alignment.center,
        )
    
    def create_book_card(self, book):
        """Create a book card"""
        # Status color mapping
        status_colors = {
            "To Be Read": ft.Colors.ORANGE,
            "Currently Reading": ft.Colors.BLUE,
            "Finished": ft.Colors.GREEN,
            "Did Not Finish": ft.Colors.RED,
        }
        
        # Rating stars
        rating_stars = "★" * book.rating + "☆" * (5 - book.rating) if book.rating > 0 else "Not rated"
        
        # Progress for currently reading books
        progress_widget = None
        if book.status == "Currently Reading" and book.total_pages > 0:
            progress = book.get_progress_percentage() / 100
            progress_widget = ft.Column([
                ft.Text(f"Progress: {book.get_progress_percentage():.1f}%", size=12),
                ft.ProgressBar(value=progress, color=ft.Colors.BLUE),
            ], spacing=5)
        
        # Book info section
        book_info = [
            ft.Text(book.title, size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"by {book.author}", size=14, color=ft.Colors.GREY_600, italic=True),
            ft.Text(" • ".join(book.genre), size=12, color=ft.Colors.BLUE),
            ft.Row([
                ft.Text("Status:", size=12),
                ft.Container(
                    content=ft.Text(book.status, size=12, color=ft.Colors.WHITE),
                    bgcolor=status_colors.get(book.status, ft.Colors.GREY),
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    border_radius=8,
                )
            ]),
            ft.Text(f"Rating: {rating_stars}", size=12, color=ft.Colors.ORANGE),
        ]
        
        if progress_widget:
            book_info.append(progress_widget)
        
        if book.total_pages > 0:
            book_info.append(ft.Text(f"Pages: {book.pages_read}/{book.total_pages}", size=12))
        
        if book.review and len(book.review.strip()) > 0:
            book_info.append(
                ft.Text(
                    f"Review: {book.review[:100]}{'...' if len(book.review) > 100 else ''}",
                    size=12,
                    color=ft.Colors.GREY_600,
                    max_lines=2,
                )
            )
        
        # Add edit button
        edit_button = ft.ElevatedButton(
            text="Edit",
            icon=ft.Icons.EDIT,
            on_click=lambda e: self.show_edit_book_dialog(book),
            height=30,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=12)
            )
        )
        
        book_info.append(ft.Container(
            content=edit_button,
            margin=ft.margin.only(top=10)
        ))
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column(book_info, spacing=8),
                padding=20,
            ),
            elevation=2,
        )
    
    def refresh_book_list(self):
        """Refresh the book list display"""
        # Apply filters
        books_to_show = self.library.books.copy()
        
        # Search filter
        if self.search_field.value:
            search_query = self.search_field.value.lower()
            books_to_show = [
                book for book in books_to_show
                if (search_query in book.title.lower() or
                    search_query in book.author.lower() or
                    any(search_query in genre.lower() for genre in book.genre))
            ]
        
        # Status filter
        if self.status_filter.value and self.status_filter.value != "All":
            books_to_show = [book for book in books_to_show if book.status == self.status_filter.value]
        
        # Rating filter
        if self.rating_filter.value and self.rating_filter.value != "All":
            if self.rating_filter.value == "Unrated":
                books_to_show = [book for book in books_to_show if book.rating == 0]
            else:
                rating = int(self.rating_filter.value[0])
                books_to_show = [book for book in books_to_show if book.rating == rating]
        
        # Clear and populate book list
        self.book_list.controls.clear()
        
        if not books_to_show:
            self.book_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=64, color=ft.Colors.GREY_400),
                        ft.Text("No books found", size=18, color=ft.Colors.GREY_600),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        else:
            for book in books_to_show:
                self.book_list.controls.append(self.create_book_card(book))
        
        if self.book_list.page:
            self.book_list.page.update()
    
    def search_books(self, e):
        """Handle search input"""
        self.refresh_book_list()
    
    def filter_books(self, e):
        """Handle filter changes"""
        self.refresh_book_list()
    
    def show_add_book_dialog(self, e):
        """Show add book dialog"""
        self.clear_add_book_fields()
        self.add_book_dialog.open = True
        self.content_area.page.update()
    
    def close_add_dialog(self, e):
        """Close add book dialog"""
        self.add_book_dialog.open = False
        self.content_area.page.update()
    
    def add_book(self, e):
        """Add a new book"""
        try:
            # Get genre list
            genres = [g.strip() for g in self.genre_field.value.split(' - ') if g.strip()]
            if not genres:
                genres = ["Unknown"]
            
            # Create new book
            new_book = Book(
                title=self.title_field.value.strip(),
                author=self.author_field.value.strip(),
                genre=genres,
                status=self.status_dropdown.value,
                rating=int(self.rating_slider.value),
                review=self.review_field.value.strip(),
                total_pages=int(self.total_pages_field.value) if self.total_pages_field.value.isdigit() else 0,
                isbn=self.isbn_field.value.strip()
            )
            
            # Add to library
            self.library.add_book(new_book)
            
            # Close dialog and refresh
            self.close_add_dialog(e)
            self.refresh_book_list()
                
        except Exception as ex:
            print(f"Error adding book: {ex}")
    
    def lookup_isbn(self, e):
        """Look up book by ISBN"""
        if not self.isbn_field.value.strip():
            return
            
        try:
            book_data = BookAPI.lookup_isbn(self.isbn_field.value.strip())
            if book_data:
                # Fill in the fields
                self.title_field.value = book_data.get('title', '')
                self.author_field.value = book_data.get('author', '')
                self.genre_field.value = ' - '.join(book_data.get('genres', ['Unknown']))
                self.total_pages_field.value = str(book_data.get('pages', 0))
                
                # Update the page
                self.content_area.page.update()
            
        except Exception as ex:
            print(f"ISBN lookup error: {ex}")
    
    def clear_add_book_fields(self):
        """Clear all add book dialog fields"""
        self.title_field.value = ""
        self.author_field.value = ""
        self.genre_field.value = ""
        self.isbn_field.value = ""
        self.total_pages_field.value = "0"
        self.status_dropdown.value = "To Be Read"
        self.rating_slider.value = 0
        self.review_field.value = ""
    
    def show_edit_book_dialog(self, book):
        """Show edit book dialog"""
        try:
            print(f"Edit button clicked for: {book.title}")
            self.selected_book = book
            self.original_status = book.status
            
            # Create separate fields for editing to avoid conflicts
            edit_title_field = ft.TextField(label="Title", width=400, value=book.title)
            edit_author_field = ft.TextField(label="Author", width=400, value=book.author)
            edit_genre_field = ft.TextField(label="Genres (separate with ' - ')", width=400, 
                                           value=" - ".join(book.genre) if book.genre else "")
            edit_isbn_field = ft.TextField(label="ISBN (optional)", width=400, value=book.isbn or "")
            edit_total_pages_field = ft.TextField(label="Total Pages", width=200, value=str(book.total_pages))
            
            edit_status_dropdown = ft.Dropdown(
                label="Status",
                width=200,
                value=book.status,
                options=[
                    ft.dropdown.Option("To Be Read"),
                    ft.dropdown.Option("Finished"),
                    ft.dropdown.Option("Currently Reading"),
                    ft.dropdown.Option("Did Not Finish"),
                ]
            )
            
            edit_rating_slider = ft.Slider(
                min=0, max=5, divisions=5, width=350,
                label="Rating: {value}",
                value=float(book.rating)
            )
            
            edit_review_field = ft.TextField(
                label="Review (optional)",
                multiline=True,
                min_lines=3,
                max_lines=5,
                width=500,
                value=book.review or ""
            )
            
            # Store references for save function
            self.edit_fields = {
                'title': edit_title_field,
                'author': edit_author_field,
                'genre': edit_genre_field,
                'isbn': edit_isbn_field,
                'total_pages': edit_total_pages_field,
                'status': edit_status_dropdown,
                'rating': edit_rating_slider,
                'review': edit_review_field
            }
            
            edit_form = ft.Column([
                ft.Row([
                    ft.Column([
                        edit_title_field,
                        edit_author_field,
                        edit_genre_field,
                        edit_isbn_field,
                    ], expand=True),
                    ft.Column([
                        edit_total_pages_field,
                        edit_status_dropdown,
                        ft.Text("Rating:", size=14, weight=ft.FontWeight.BOLD),
                        edit_rating_slider,
                    ], expand=True),
                ]),
                ft.Container(height=10),
                edit_review_field,
            ], spacing=10)
            
            self.edit_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit Book"),
                content=ft.Container(
                    content=edit_form,
                    width=500,
                    height=600,
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=self.close_edit_dialog),
                    ft.ElevatedButton("Save Changes", on_click=self.save_book_edit),
                ],
            )
            
            print("Creating edit overlay...")
            # Use a simple overlay approach that definitely works
            edit_overlay = ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Edit Book", size=24, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    on_click=self.close_edit_dialog
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            edit_form,
                            ft.Row([
                                ft.ElevatedButton("Save Changes", on_click=self.save_book_edit),
                                ft.TextButton("Cancel", on_click=self.close_edit_dialog),
                            ], alignment=ft.MainAxisAlignment.END)
                        ], spacing=20, scroll=ft.ScrollMode.AUTO),
                        padding=20,
                        width=700,
                        height=600
                    ),
                    elevation=10
                ),
                bgcolor=ft.Colors.BLACK54,  # Semi-transparent background
                alignment=ft.alignment.center,
                width=self.content_area.page.window.width,
                height=self.content_area.page.window.height
            )
            
            # Store reference and add to page overlay
            self.edit_overlay = edit_overlay
            self.content_area.page.overlay.append(edit_overlay)
            self.content_area.page.update()
            print("Edit overlay should be visible now")
            
        except Exception as ex:
            print(f"Error in show_edit_book_dialog: {ex}")
            import traceback
            traceback.print_exc()
    
    def save_book_edit(self, e):
        """Save book edits with DNF detection"""
        try:
            # Use edit fields instead of add fields
            if not self.edit_fields['title'].value.strip() or not self.edit_fields['author'].value.strip():
                return
            
            # Store old status for comparison
            old_status = self.original_status
            new_status = self.edit_fields['status'].value
            
            # Update book properties
            self.selected_book.title = self.edit_fields['title'].value.strip()
            self.selected_book.author = self.edit_fields['author'].value.strip()
            self.selected_book.genre = [g.strip() for g in self.edit_fields['genre'].value.split(" - ") if g.strip()]
            self.selected_book.status = new_status
            self.selected_book.rating = int(self.edit_fields['rating'].value)
            self.selected_book.review = self.edit_fields['review'].value.strip()
            self.selected_book.total_pages = int(self.edit_fields['total_pages'].value) if self.edit_fields['total_pages'].value.isdigit() else 0
            self.selected_book.isbn = self.edit_fields['isbn'].value.strip()
            
            # Check for status changes and handle library transfers
            if old_status != "Did Not Finish" and new_status == "Did Not Finish":
                # Moving from main library to DNF
                self.library.move_to_dnf(self.selected_book)
            elif old_status == "Did Not Finish" and new_status != "Did Not Finish":
                # Moving from DNF back to main library
                self.library.move_from_dnf(self.selected_book)
            else:
                # Status didn't change libraries, just update
                self.library.update_book(self.selected_book)
            
            # Close dialog and refresh
            try:
                self.content_area.page.overlay.remove(self.edit_overlay)
            except:
                self.content_area.page.overlay.clear()
            self.content_area.page.update()
            self.refresh_book_list()
            
        except Exception as ex:
            print(f"Error editing book: {ex}")
            # Don't close dialog on error so user can try again
    
    def close_edit_dialog(self, e):
        """Close edit dialog"""
        try:
            self.content_area.page.overlay.remove(self.edit_overlay)
            self.content_area.page.update()
        except:
            # Fallback - clear all overlays
            self.content_area.page.overlay.clear()
            self.content_area.page.update()
    
    def export_csv(self, e):
        """Export to CSV"""
        try:
            filename = f"readwise_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            if export_to_csv(self.library.books, filename):
                print(f"Exported to {filename}")
            else:
                print("Export failed")
        except Exception as ex:
            print(f"Export error: {ex}")
    
    def export_report(self, e):
        """Export reading report"""
        try:
            filename = f"reading_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            if export_reading_report(self.library, filename):
                print(f"Report exported to {filename}")
            else:
                print("Report export failed")
        except Exception as ex:
            print(f"Report error: {ex}")
    
    def export_json(self, e):
        """Export to JSON"""
        try:
            filename = f"readwise_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if export_to_json(self.library, filename):
                print(f"Backed up to {filename}")
            else:
                print("Backup failed")
        except Exception as ex:
            print(f"Backup error: {ex}")

def main(page: ft.Page):
    app = ReadWiseApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)