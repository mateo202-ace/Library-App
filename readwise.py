import flet as ft
import os
import sys
import json
from datetime import datetime
from typing import Optional

# Add src to path
sys.path.append('src')
from models.book import Book
from models.library import Library
from models.library_manager import LibraryManager
from utils.book_api import BookAPI

class ReadWiseApp:
    def __init__(self):
        self.data_path = "/Users/juanmateo/Desktop/Library app/ReadWise/src/data"
        self.library_manager = LibraryManager(self.data_path)
        self.selected_book: Optional[Book] = None
        self.current_view = "library"
        self.select_mode = False
        self.selected_books = set()
        
        # Theme system
        self.themes = {
            "light": {
                "name": "Light",
                "primary": "#404040",     # Dark grey
                "secondary": "#f5f5f5",   # Very light grey
                "background": "#ffffff",  # Pure white
                "surface": "#ffffff",     # White surface
                "text": "#1a1a1a",        # Almost black
                "accent": "#2a2a2a",      # Dark grey accent
                "border": "#e0e0e0",      # Light grey border
                "success": "#404040",     # Dark grey
                "warning": "#666666",     # Medium grey
                "danger": "#1a1a1a"       # Almost black
            },
            "dark": {
                "name": "Dark", 
                "primary": "#808080",     # Medium grey
                "secondary": "#2a2a2a",   # Dark grey
                "background": "#1a1a1a",  # Almost black
                "surface": "#2a2a2a",     # Dark grey surface
                "text": "#f0f0f0",        # Light grey text
                "accent": "#666666",      # Medium grey accent
                "border": "#404040",      # Dark border
                "success": "#808080",     # Medium grey
                "warning": "#a0a0a0",     # Light grey
                "danger": "#f0f0f0"       # Light grey
            }
        }
        self.current_theme = self.load_theme_preference()
        
    def load_theme_preference(self):
        """Load saved theme preference"""
        settings_file = os.path.join(self.data_path, "settings.json")
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    return settings.get("theme", "light")
        except:
            pass
        return "light"
    
    def save_theme_preference(self, theme_id):
        """Save theme preference to settings"""
        settings_file = os.path.join(self.data_path, "settings.json")
        settings = {}
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
        except:
            pass
        
        settings["theme"] = theme_id
        try:
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving theme: {e}")
    
    def get_theme_colors(self):
        """Get current theme colors"""
        return self.themes.get(self.current_theme, self.themes["light"])
    
    def apply_theme(self, page):
        """Apply current theme to the page"""
        theme_colors = self.get_theme_colors()
        
        # Update page theme mode based on theme
        if self.current_theme == "dark":
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            
        # Apply custom color theme
        page.bgcolor = theme_colors["background"]
        
        # Update navigation rail colors
        if hasattr(self, 'nav_rail'):
            self.nav_rail.bgcolor = theme_colors["surface"]
            
        # Update top bar colors  
        if hasattr(self, 'top_bar'):
            self.top_bar.bgcolor = theme_colors["secondary"]
        
        page.update()
    
    def change_theme(self, theme_id):
        """Change the current theme"""
        if theme_id in self.themes:
            self.current_theme = theme_id
            self.save_theme_preference(theme_id)
            if hasattr(self, 'page'):
                # Update theme colors for existing components
                theme_colors = self.get_theme_colors()
                
                # Update top bar
                self.top_bar.content.controls[0].value = "📚"
                self.top_bar.content.controls[3].color = theme_colors["text"]
                self.top_bar.bgcolor = theme_colors["secondary"]
                
                # Update nav rail
                self.nav_rail.bgcolor = theme_colors["surface"]
                
                # Apply theme and force refresh
                self.apply_theme(self.page)
                
                # Refresh current view to apply new colors
                if self.current_view == "library":
                    self.show_library_view()
                elif self.current_view == "statistics":
                    self.show_statistics_view()
                elif self.current_view == "settings":
                    self.show_settings_view()
                elif self.current_view == "dnf":
                    self.show_dnf_view()
                
                # Force page update
                self.page.update()
        
    def main(self, page: ft.Page):
        self.page = page  # Store page reference for theme changes
        page.title = "📚 ReadWise - Smart Reading Management"
        page.window.width = 1400
        page.window.height = 900
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        
        # Get theme colors first
        theme_colors = self.get_theme_colors()
        
        # Create main components
        self.create_components(page)
        
        # Create library dropdown options
        self.update_library_dropdown_options()
        
        # Simple navigation: Statistics | Settings (library selector handles library/DNF)
        self.nav_rail = ft.NavigationRail(
            selected_index=None,  # No initial selection
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=120,
            min_extended_width=200,
            bgcolor=theme_colors["surface"],
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    selected_icon=ft.Icons.ANALYTICS,
                    label="Statistics"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings"
                ),
            ],
            on_change=self.nav_change,
        )
        
        # Library dropdown in top bar
        self.library_dropdown = ft.Dropdown(
            width=200,
            value=self.library_manager.current_library_id,
            on_change=self.library_change,
            bgcolor=theme_colors["surface"],
            color=theme_colors["text"],
            border_color=theme_colors["border"],
        )
        
        # Top bar with library selector
        
        self.top_bar = ft.Container(
            content=ft.Row([
                ft.Text("📚", size=24),
                self.library_dropdown,
                ft.Container(expand=True),  # Spacer
                ft.Text("📚 ReadWise", size=18, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=theme_colors["secondary"],
        )
        
        # Content area
        self.content_area = ft.Container(expand=True)
        
        # Apply initial theme
        self.apply_theme(page)
        
        # Main layout
        page.add(
            ft.Column([
                self.top_bar,
                ft.Row([
                    self.nav_rail,
                    ft.VerticalDivider(width=1),
                    self.content_area,
                ], expand=True),
            ], expand=True)
        )
        
        # Update dropdown options with actual data
        self.update_library_dropdown_options()
        
        # Show library view initially  
        self.current_view = "library"
        self.show_library_view()
        page.update()
        
    def create_components(self, page):
        # Book list
        self.book_list = ft.ListView(expand=1, spacing=10, padding=20)
        
        # Search and filters
        # These will be themed in show_library_view_without_refresh
        self.search_field = None
        self.status_filter = None  
        self.rating_filter = None
        self.sort_dropdown = None
        
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
                    ft.Container(height=20),  # Add space before buttons
                ], tight=True),
                width=500,
                height=445,  # Increase dialog height to accommodate spacing
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
            self.current_view = "statistics"
            self.show_statistics_view()
        elif selected_index == 1:
            self.current_view = "settings"
            self.show_settings_view()
            
        self.content_area.page.update()
    
    def update_library_dropdown_options(self):
        """Update the library dropdown with current libraries + DNF"""
        libraries = self.library_manager.get_library_list()
        options = []
        
        # Add existing libraries
        for lib in libraries:
            options.append(ft.dropdown.Option(
                key=lib["id"],
                text=f"📚 {lib['name']}"
            ))
        
        # Add DNF Books option (global)
        options.append(ft.dropdown.Option(
            key="__dnf__",
            text="🚫 Did Not Finish"
        ))
        
        # Add "New Library" option at the bottom
        if len(libraries) < 5:  # Max 5 libraries
            options.append(ft.dropdown.Option(
                key="__new__",
                text="➕ New Library"
            ))
        
        # Add "Manage Libraries" option
        options.append(ft.dropdown.Option(
            key="__manage__",
            text="⚙️ Manage Libraries"
        ))
        
        if hasattr(self, 'library_dropdown'):
            self.library_dropdown.options = options
    
    def library_change(self, e):
        """Handle library dropdown changes"""
        selected_value = e.control.value
        
        if selected_value == "__new__":
            self.show_create_library_dialog()
            # Reset dropdown to current library
            e.control.value = self.library_manager.current_library_id
            self.content_area.page.update()
        elif selected_value == "__dnf__":
            # Show DNF view
            self.current_view = "dnf"
            self.show_dnf_view()
            self.content_area.page.update()
        elif selected_value == "__manage__":
            self.show_manage_libraries_dialog()
            # Reset dropdown to current library
            e.control.value = self.library_manager.current_library_id
            self.content_area.page.update()
        else:
            # Switch to selected library
            if self.library_manager.switch_library(selected_value):
                self.current_view = "library"
                self.show_library_view()
                self.content_area.page.update()
    
    def show_create_library_dialog(self):
        """Show dialog to create a new library using overlay approach"""
        library_name_field = ft.TextField(
            label="Library Name",
            width=300,
            autofocus=True
        )
        
        def create_library(e):
            if library_name_field.value.strip():
                lib_id = self.library_manager.create_library(library_name_field.value.strip())
                if lib_id:
                    # Switch to new library
                    self.library_manager.switch_library(lib_id)
                    # Update dropdown options
                    self.update_library_dropdown_options()
                    self.library_dropdown.value = lib_id
                    # Show the new library
                    self.current_view = "library"
                    self.show_library_view()
                # Close dialog
                try:
                    self.content_area.page.overlay.remove(self.create_library_overlay)
                except:
                    self.content_area.page.overlay.clear()
                self.content_area.page.update()
        
        def close_dialog(e):
            try:
                self.content_area.page.overlay.remove(self.create_library_overlay)
            except:
                self.content_area.page.overlay.clear()
            self.content_area.page.update()
        
        # Create overlay with the same approach as edit dialogs
        self.create_library_overlay = ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Create New Library", size=20, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                on_click=close_dialog
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        library_name_field,
                        ft.Text("Max 5 libraries allowed", size=12, color=ft.Colors.GREY_600),
                        ft.Row([
                            ft.ElevatedButton("Create", on_click=create_library),
                            ft.TextButton("Cancel", on_click=close_dialog),
                        ], alignment=ft.MainAxisAlignment.END)
                    ], spacing=20),
                    padding=20,
                    width=400,
                    height=240
                ),
                elevation=10
            ),
            bgcolor=ft.Colors.BLACK54,  # Semi-transparent background
            alignment=ft.alignment.center,
            width=self.content_area.page.window.width,
            height=self.content_area.page.window.height
        )
        
        self.content_area.page.overlay.append(self.create_library_overlay)
        self.content_area.page.update()
    
    def show_manage_libraries_dialog(self):
        """Show dialog to manage libraries (rename, delete)"""
        libraries = self.library_manager.get_library_list()
        
        # Create library list with options
        library_items = []
        for lib in libraries:
            lib_id = lib["id"]
            lib_name = lib["name"]
            
            # Don't allow deletion if it's the only library
            can_delete = len(libraries) > 1
            
            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED if can_delete else ft.Colors.GREY,
                disabled=not can_delete,
                tooltip="Delete library" if can_delete else "Cannot delete the only library",
                on_click=lambda e, library_id=lib_id, library_name=lib_name: self.confirm_delete_library(library_id, library_name)
            )
            
            library_items.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LIBRARY_BOOKS, color=ft.Colors.BLUE),
                            ft.Text(lib_name, size=16, expand=True),
                            delete_button,
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15,
                    ),
                    elevation=1,
                )
            )
        
        def close_dialog(e):
            try:
                self.content_area.page.overlay.remove(self.manage_libraries_overlay)
            except:
                self.content_area.page.overlay.clear()
            self.content_area.page.update()
        
        # Create overlay
        self.manage_libraries_overlay = ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Manage Libraries", size=20, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                on_click=close_dialog
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=10),
                        ft.Column(library_items, spacing=10, scroll=ft.ScrollMode.AUTO),
                        ft.Container(height=20),
                        ft.Row([
                            ft.TextButton("Close", on_click=close_dialog),
                        ], alignment=ft.MainAxisAlignment.END)
                    ], spacing=10),
                    padding=20,
                    width=500,
                    height=400
                ),
                elevation=10
            ),
            bgcolor=ft.Colors.BLACK54,
            alignment=ft.alignment.center,
            width=self.content_area.page.window.width,
            height=self.content_area.page.window.height
        )
        
        self.content_area.page.overlay.append(self.manage_libraries_overlay)
        self.content_area.page.update()
    
    def confirm_delete_library(self, library_id, library_name):
        """Show confirmation dialog before deleting library"""
        def delete_confirmed(e):
            self.delete_library(library_id)
            # Close confirmation dialog
            try:
                self.content_area.page.overlay.remove(self.confirm_delete_overlay)
            except:
                pass
            self.content_area.page.update()
        
        def cancel_delete(e):
            try:
                self.content_area.page.overlay.remove(self.confirm_delete_overlay)
            except:
                self.content_area.page.overlay.clear()
            self.content_area.page.update()
        
        # Create confirmation dialog
        self.confirm_delete_overlay = ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.WARNING, size=48, color=ft.Colors.ORANGE),
                        ft.Text("Delete Library?", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Are you sure you want to delete '{library_name}'?", size=18),
                        ft.Text("This action cannot be undone. All books in this library will be permanently deleted.", 
                               size=15, color=ft.Colors.RED),
                        ft.Container(height=20),
                        ft.Row([
                            ft.ElevatedButton(
                                "Delete", 
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.RED,
                                on_click=delete_confirmed
                            ),
                            ft.TextButton("Cancel", on_click=cancel_delete),
                        ], alignment=ft.MainAxisAlignment.END)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                    padding=30,
                    width=400,
                    height=320
                ),
                elevation=10
            ),
            bgcolor=ft.Colors.BLACK54,
            alignment=ft.alignment.center,
            width=self.content_area.page.window.width,
            height=self.content_area.page.window.height
        )
        
        self.content_area.page.overlay.append(self.confirm_delete_overlay)
        self.content_area.page.update()
    
    def delete_library(self, library_id):
        """Delete a library after confirmation"""
        if self.library_manager.delete_library(library_id):
            # Update dropdown and switch to a remaining library
            libraries = self.library_manager.get_library_list()
            if libraries:
                # Switch to first available library
                self.library_manager.switch_library(libraries[0]["id"])
                self.update_library_dropdown_options()
                self.library_dropdown.value = libraries[0]["id"]
                self.show_library_view()
            
            # Close manage dialog
            try:
                self.content_area.page.overlay.remove(self.manage_libraries_overlay)
            except:
                self.content_area.page.overlay.clear()
            self.content_area.page.update()
    
    def show_library_view_without_refresh(self):
        """Set up library view without refreshing book list"""
        theme_colors = self.get_theme_colors()
        
        # Create themed search and filter components
        self.search_field = ft.TextField(
            label="Search books...",
            width=500,
            on_change=self.search_books,
            prefix_icon=ft.Icons.SEARCH,
            bgcolor=theme_colors["surface"],
            color=theme_colors["text"],
            border_color=theme_colors["border"],
            focused_border_color=theme_colors["accent"],
        )
        
        # Custom label containers for better visibility
        status_container = ft.Column([
            ft.Text("Status", size=12, color=theme_colors["text"], weight=ft.FontWeight.W_500),
            ft.Dropdown(
                width=200,
                options=[
                    ft.dropdown.Option("All"),
                    ft.dropdown.Option("To Be Read"),
                    ft.dropdown.Option("Finished"),
                    ft.dropdown.Option("Currently Reading"),
                ],
                value="All",
                on_change=self.filter_books,
                bgcolor=theme_colors["surface"],
                color=theme_colors["text"],
                border_color=theme_colors["border"],
            )
        ], spacing=5)
        
        rating_container = ft.Column([
            ft.Text("Rating", size=12, color=theme_colors["text"], weight=ft.FontWeight.W_500),
            ft.Dropdown(
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
                bgcolor=theme_colors["surface"],
                color=theme_colors["text"],
                border_color=theme_colors["border"],
            )
        ], spacing=5)
        
        sort_container = ft.Column([
            ft.Text("Sort By", size=12, color=theme_colors["text"], weight=ft.FontWeight.W_500),
            ft.Dropdown(
                width=160,
                options=[
                    ft.dropdown.Option("Status"),
                    ft.dropdown.Option("Name (A-Z)"),
                    ft.dropdown.Option("Author"),
                    ft.dropdown.Option("Genre"),
                    ft.dropdown.Option("Rating"),
                    ft.dropdown.Option("Date Added"),
                ],
                value="Status",
                on_change=self.sort_books,
                bgcolor=theme_colors["surface"],
                color=theme_colors["text"],
                border_color=theme_colors["border"],
            )
        ], spacing=5)
        
        # Store references to the actual dropdowns for the filter functions
        self.status_filter = status_container.controls[1]
        self.rating_filter = rating_container.controls[1]
        self.sort_dropdown = sort_container.controls[1]
        
        header = ft.Container(
            content=ft.Column([
                ft.Text("📚 My Library", size=28, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                ft.Divider(color=theme_colors["primary"]),
                ft.Row([
                    self.search_field,
                    status_container,
                    rating_container,
                    sort_container,
                    ft.ElevatedButton(
                        "Add Book",
                        icon=ft.Icons.ADD,
                        on_click=self.show_add_book_dialog,
                        bgcolor=theme_colors["primary"],
                        color=theme_colors["background"],
                    ),
                ], spacing=10),
            ], spacing=10),
            padding=20,
            margin=ft.margin.only(bottom=10),
            bgcolor=theme_colors["background"]
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
        dnf_books = self.library_manager.get_dnf_books()
        
        header = ft.Container(
            content=ft.Column([
                ft.Text("📖 Did Not Finish", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(f"{len(dnf_books)} books you didn't finish", size=16, color=ft.Colors.GREY_600),
                ft.Divider(),
            ], spacing=10),
            padding=20,
            margin=ft.margin.only(bottom=1)
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
        current_library = self.library_manager.get_current_library()
        if not current_library:
            return
        stats = current_library.get_reading_statistics()
        theme_colors = self.get_theme_colors()
        
        # Modern stat icons
        stat_icons = {
            "total": "📚",
            "finished": "✅",
            "reading": "📖",
            "dnf": "❌"
        }
        
        # Create modern stat cards
        stat_cards = ft.Row([
            self.create_stat_card_with_emoji("Total Books", str(stats['total_books']), stat_icons["total"]),
            self.create_stat_card_with_emoji("Finished", str(stats['finished_books']), stat_icons["finished"]),
            self.create_stat_card_with_emoji("Currently Reading", str(stats['currently_reading']), stat_icons["reading"]),
            self.create_stat_card_with_emoji("DNF Books", str(stats['dnf_books']), stat_icons["dnf"]),
        ], spacing = 20)
        
        # Create colorful genre breakdown with progress bars
        sorted_genres = sorted(stats['genre_counts'].items(), key=lambda x: x[1], reverse=True)[:10]
        max_count = max([count for _, count in sorted_genres]) if sorted_genres else 1
        
        # Genre colors that work with all themes
        genre_colors = [
            ft.Colors.RED_400, ft.Colors.BLUE_400, ft.Colors.GREEN_400, ft.Colors.PURPLE_400,
            ft.Colors.ORANGE_400, ft.Colors.TEAL_400, ft.Colors.PINK_400, ft.Colors.INDIGO_400,
            ft.Colors.LIME_400, ft.Colors.CYAN_400
        ]
        
        genre_items = []
        for i, (genre, count) in enumerate(sorted_genres):
            color = genre_colors[i % len(genre_colors)]
            progress = count / max_count
            
            genre_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(genre, size=14, color=theme_colors["text"], weight=ft.FontWeight.W_500),
                                expand=True
                            ),
                            ft.Text(f"{count}", size=14, color=color, weight=ft.FontWeight.BOLD),
                        ]),
                        ft.Container(height=5),
                        ft.ProgressBar(
                            value=progress,
                            color=color,
                            bgcolor=theme_colors["surface"],
                            height=6
                        ),
                    ], spacing=2),
                    padding=ft.padding.symmetric(vertical=8, horizontal=12),
                    margin=ft.margin.symmetric(vertical=2),
                    bgcolor=theme_colors["surface"],
                    border_radius=8,
                    border=ft.border.all(1, color),
                )
            )
        
        # Create reading streak and quick stats
        quick_stats = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("📈", size=24),
                    ft.Text("Reading", size=12, color=theme_colors["accent"]),
                    ft.Text("Progress", size=12, color=theme_colors["accent"]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=theme_colors["surface"],
                border_radius=10,
                border=ft.border.all(2, theme_colors["primary"]),
                width=100
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("🎯", size=24),
                    ft.Text(f"{stats['finished_books']}", size=18, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                    ft.Text("Completed", size=10, color=theme_colors["accent"]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=theme_colors["surface"],
                border_radius=10,
                border=ft.border.all(2, ft.Colors.GREEN),
                width=100
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("🔥", size=24),
                    ft.Text(f"{stats['currently_reading']}", size=18, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                    ft.Text("Active", size=10, color=theme_colors["accent"]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=theme_colors["surface"],
                border_radius=10,
                border=ft.border.all(2, ft.Colors.ORANGE),
                width=100
            ),
        ], spacing=15)
        
        self.content_area.content = ft.Container(
            content=ft.Column([
                # Header with gradient-like effect
                ft.Container(
                    content=ft.Row([
                        ft.Text("📊 Reading Statistics", size=28, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.AUTO_GRAPH, size=32, color=theme_colors["primary"]),
                    ]),
                    padding=25,
                    margin=ft.margin.only(bottom=20),
                    bgcolor=theme_colors["secondary"],
                    border_radius=15,
                    border=ft.border.all(2, theme_colors["primary"])
                ),
                
                # Main stat cards
                stat_cards,
                ft.Container(height=20),
                
                # Quick stats row
                quick_stats,
                ft.Container(height=20),
                
                # Enhanced genre breakdown
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("📚 Genre Breakdown", size=20, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                            ft.Container(expand=True),
                            ft.Text("Top 10", size=12, color=theme_colors["accent"]),
                        ]),
                        ft.Container(height=15),
                        ft.Column(genre_items, spacing=5),
                    ]),
                    padding=25,
                    bgcolor=theme_colors["background"],
                    border_radius=15,
                    border=ft.border.all(2, theme_colors["accent"])
                ),
            ], spacing=15),
            padding=20,
            bgcolor=theme_colors["background"]
        )
    
    def show_settings_view(self):
        """Show settings with theme selector"""
        theme_colors = self.get_theme_colors()
        
        # Create theme selector dropdown
        theme_options = [
            ft.dropdown.Option(key=theme_id, text=theme_data["name"])
            for theme_id, theme_data in self.themes.items()
        ]
        
        theme_dropdown = ft.Dropdown(
            label="Choose Theme",
            width=300,
            value=self.current_theme,
            options=theme_options,
            on_change=self.on_theme_change,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            border_color=theme_colors["primary"],
        )
        
        self.content_area.content = ft.Container(
            content=ft.Column([
                ft.Text("⚙️ Settings", size=28, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                ft.Container(height=20),
                
                # Theme selection section
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎨 Appearance", size=20, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                            ft.Container(height=10),
                            theme_dropdown,
                            ft.Container(height=10),
                            ft.Text("Choose your house colors or classic light/dark theme", 
                                   size=12, color=theme_colors["accent"]),
                        ], spacing=10),
                        padding=20,
                        bgcolor=theme_colors["surface"],
                    ),
                    elevation=2,
                ),
                
                ft.Container(height=30),
                
                # App info section
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📚 About", size=20, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                            ft.Container(height=10),
                            ft.Text("ReadWise - Smart Reading Management", size=16, color=theme_colors["text"]),
                            ft.Text("Version 2.0", size=14, color=theme_colors["accent"]),
                            ft.Container(height=10),
                            ft.Text("Manage your personal book library with style ✨", 
                                   size=12, color=theme_colors["accent"]),
                        ], spacing=5),
                        padding=20,
                        bgcolor=theme_colors["surface"],
                    ),
                    elevation=2,
                ),
            ], spacing=20),
            padding=40,
            bgcolor=theme_colors["background"],
        )
    
    def on_theme_change(self, e):
        """Handle theme change from dropdown"""
        selected_theme = e.control.value
        self.change_theme(selected_theme)
    
    def create_stat_card(self, title: str, value: str, icon):
        """Create a statistics card"""
        theme_colors = self.get_theme_colors()
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=32, color=theme_colors["primary"]),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                ft.Text(title, size=14, color=theme_colors["accent"]),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15,
            bgcolor=theme_colors["secondary"],
            border_radius=20,
            width=200,
            height=150,
            alignment=ft.alignment.center,
        )
    
    def create_stat_card_with_emoji(self, title: str, value: str, emoji: str):
        """Create a statistics card with emoji instead of icon"""
        theme_colors = self.get_theme_colors()
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(emoji, size=28),
                    ft.Container(height=5),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
                    ft.Text(title, size=12, color=theme_colors["accent"], weight=ft.FontWeight.W_500),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                bgcolor=theme_colors["surface"],
                width=180,
                height=140,
                alignment=ft.alignment.center,
            ),
            elevation=4,
            color=theme_colors["surface"]
        )
    
    def create_book_card(self, book):
        """Create a book card"""
        theme_colors = self.get_theme_colors()
        
        # Status color mapping using theme colors
        status_colors = {
            "To Be Read": ft.Colors.ORANGE,
            "Currently Reading": theme_colors["primary"],
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
                ft.Text(f"Progress: {book.get_progress_percentage():.1f}%", size=12, color=theme_colors["text"]),
                ft.ProgressBar(value=progress, color=theme_colors["primary"]),
            ], spacing=5)
        
        # Book info section
        book_info = [
            ft.Text(book.title, size=18, weight=ft.FontWeight.BOLD, color=theme_colors["text"]),
            ft.Text(f"by {book.author}", size=14, color=theme_colors["accent"], italic=True),
            ft.Text(" • ".join(book.genre), size=12, color=theme_colors["primary"]),
            ft.Row([
                ft.Text("Status:", size=12, color=theme_colors["text"]),
                ft.Container(
                    content=ft.Text(book.status, size=12, color=ft.Colors.WHITE),
                    bgcolor=status_colors.get(book.status, ft.Colors.GREY),
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    border_radius=8,
                )
            ]),
            ft.Text(f"Rating: {rating_stars}", size=12, color=theme_colors["accent"]),
        ]
        
        if progress_widget:
            book_info.append(progress_widget)
        
        if book.total_pages > 0:
            book_info.append(ft.Text(f"Pages: {book.pages_read}/{book.total_pages}", size=12, color=theme_colors["text"]))
        
        if book.review and len(book.review.strip()) > 0:
            book_info.append(
                ft.Text(
                    f"Review: {book.review[:100]}{'...' if len(book.review) > 100 else ''}",
                    size=12,
                    color=theme_colors["accent"],
                    max_lines=2,
                )
            )
        
        # Add edit button
        edit_button = ft.ElevatedButton(
            text="Edit",
            icon=ft.Icons.EDIT,
            on_click=lambda e: self.show_edit_book_dialog(book),
            height=30,
            bgcolor=theme_colors["primary"],
            color=theme_colors["background"],
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
                bgcolor=theme_colors["surface"],
            ),
            elevation=3,
            color=theme_colors["surface"]
        )
    
    def refresh_book_list(self):
        """Refresh the book list display"""
        # Apply filters
        current_library = self.library_manager.get_current_library()
        if not current_library:
            return
        books_to_show = current_library.books.copy()
        
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
        
        # Sort books based on selected option
        if self.sort_dropdown.value == "Status":
            # Custom order: Currently Reading → To Be Read → Finished
            status_order = {"Currently Reading": 0, "To Be Read": 1, "Finished": 2, "Did Not Finish": 3}
            books_to_show.sort(key=lambda book: (status_order.get(book.status, 4), book.title.lower()))
        elif self.sort_dropdown.value == "Name (A-Z)":
            books_to_show.sort(key=lambda book: book.title.lower())
        elif self.sort_dropdown.value == "Author":
            books_to_show.sort(key=lambda book: book.author.lower())
        elif self.sort_dropdown.value == "Genre":
            books_to_show.sort(key=lambda book: book.genre[0].lower() if book.genre else "zzz")
        elif self.sort_dropdown.value == "Rating":
            books_to_show.sort(key=lambda book: book.rating, reverse=True)  # Highest first
        elif self.sort_dropdown.value == "Date Added":
            # For now, sort by title as we don't have date_added field yet
            books_to_show.sort(key=lambda book: book.title.lower(), reverse=True)
        
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
    
    def sort_books(self, e):
        """Handle sort changes"""
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
            current_library = self.library_manager.get_current_library()
            if current_library:
                current_library.add_book(new_book)
            
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
            current_library = self.library_manager.get_current_library()
            if not current_library:
                return
                
            if old_status != "Did Not Finish" and new_status == "Did Not Finish":
                # Moving from current library to DNF
                current_library.move_to_dnf(self.selected_book)
            elif old_status == "Did Not Finish" and new_status != "Did Not Finish":
                # Moving from DNF back to current library
                current_library.move_from_dnf(self.selected_book)
            else:
                # Status didn't change libraries, just update
                current_library.update_book(self.selected_book)
            
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
    

def main(page: ft.Page):
    app = ReadWiseApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)