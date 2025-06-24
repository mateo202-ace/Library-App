import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from .library import Library

class LibraryManager:
    """Manages multiple user libraries with max 5 library limit"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.libraries_config_file = os.path.join(base_path, "libraries_config.json")
        self.dnf_csv_file = os.path.join(base_path, "dnf_books.csv")
        self.dnf_json_file = os.path.join(base_path, "dnf_books_extended.json")
        
        # Load or create libraries configuration
        self.libraries_config = self.load_libraries_config()
        
        # Initialize libraries
        self.libraries = {}
        self.current_library_id = None
        self.dnf_books = []
        
        self.load_all_libraries()
        
    def load_libraries_config(self) -> Dict:
        """Load libraries configuration from JSON file"""
        default_config = {
            "libraries": [
                {
                    "id": "main",
                    "name": "Main Library",
                    "created_date": datetime.now().isoformat(),
                    "color": "#2196F3",
                    "icon": "library_books"
                }
            ],
            "current_library": "main",
            "max_libraries": 5
        }
        
        if os.path.exists(self.libraries_config_file):
            try:
                with open(self.libraries_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading libraries config: {e}")
                return default_config
        else:
            # Create default config
            self.save_libraries_config(default_config)
            return default_config
    
    def save_libraries_config(self, config: Dict = None):
        """Save libraries configuration to JSON file"""
        if config is None:
            config = self.libraries_config
            
        try:
            with open(self.libraries_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving libraries config: {e}")
    
    def load_all_libraries(self):
        """Load all libraries from configuration"""
        for lib_config in self.libraries_config["libraries"]:
            lib_id = lib_config["id"]
            lib_name = lib_config["name"]
            
            # Create file paths for this library
            csv_file = os.path.join(self.base_path, f"books_{lib_id}.csv")
            
            # Create Library instance
            library = Library(lib_name, csv_file, self.dnf_csv_file)
            self.libraries[lib_id] = library
        
        # Set current library
        self.current_library_id = self.libraries_config.get("current_library", "main")
        
        # Load DNF books (shared across all libraries)
        if self.libraries:
            first_library = list(self.libraries.values())[0]
            self.dnf_books = first_library.dnf_books
    
    def get_current_library(self) -> Optional[Library]:
        """Get the currently active library"""
        if self.current_library_id and self.current_library_id in self.libraries:
            return self.libraries[self.current_library_id]
        return None
    
    def switch_library(self, library_id: str) -> bool:
        """Switch to a different library"""
        if library_id in self.libraries:
            self.current_library_id = library_id
            self.libraries_config["current_library"] = library_id
            self.save_libraries_config()
            return True
        return False
    
    def create_library(self, name: str, color: str = "#2196F3", icon: str = "library_books") -> Optional[str]:
        """Create a new library (max 5 libraries)"""
        if len(self.libraries) >= self.libraries_config.get("max_libraries", 5):
            return None  # Max libraries reached
        
        # Generate unique ID
        lib_id = name.lower().replace(" ", "_").replace("-", "_")
        counter = 1
        original_id = lib_id
        while lib_id in self.libraries:
            lib_id = f"{original_id}_{counter}"
            counter += 1
        
        # Create library config
        lib_config = {
            "id": lib_id,
            "name": name,
            "created_date": datetime.now().isoformat(),
            "color": color,
            "icon": icon
        }
        
        # Add to configuration
        self.libraries_config["libraries"].append(lib_config)
        self.save_libraries_config()
        
        # Create Library instance
        csv_file = os.path.join(self.base_path, f"books_{lib_id}.csv")
        library = Library(name, csv_file, self.dnf_csv_file)
        self.libraries[lib_id] = library
        
        return lib_id
    
    def rename_library(self, library_id: str, new_name: str) -> bool:
        """Rename an existing library"""
        if library_id not in self.libraries:
            return False
        
        # Update library name
        self.libraries[library_id].name = new_name
        
        # Update configuration
        for lib_config in self.libraries_config["libraries"]:
            if lib_config["id"] == library_id:
                lib_config["name"] = new_name
                break
        
        self.save_libraries_config()
        return True
    
    def delete_library(self, library_id: str) -> bool:
        """Delete a library (cannot delete if it's the only one)"""
        if len(self.libraries) <= 1 or library_id not in self.libraries:
            return False
        
        # Remove library files
        library = self.libraries[library_id]
        try:
            if os.path.exists(library.csv_file):
                os.remove(library.csv_file)
            if os.path.exists(library.json_file):
                os.remove(library.json_file)
        except Exception as e:
            print(f"⚠️ Error deleting library files: {e}")
        
        # Remove from memory
        del self.libraries[library_id]
        
        # Remove from configuration
        self.libraries_config["libraries"] = [
            lib for lib in self.libraries_config["libraries"] 
            if lib["id"] != library_id
        ]
        
        # Switch to another library if this was current
        if self.current_library_id == library_id:
            self.current_library_id = list(self.libraries.keys())[0]
            self.libraries_config["current_library"] = self.current_library_id
        
        self.save_libraries_config()
        return True
    
    def get_library_list(self) -> List[Dict]:
        """Get list of all libraries with metadata"""
        return [
            {
                "id": lib_config["id"],
                "name": lib_config["name"],
                "color": lib_config.get("color", "#2196F3"),
                "icon": lib_config.get("icon", "library_books"),
                "book_count": len(self.libraries[lib_config["id"]].books) if lib_config["id"] in self.libraries else 0,
                "is_current": lib_config["id"] == self.current_library_id
            }
            for lib_config in self.libraries_config["libraries"]
        ]
    
    def move_books_between_libraries(self, book_titles: List[str], from_library_id: str, to_library_id: str) -> int:
        """Move books from one library to another. Returns number of books moved."""
        if from_library_id not in self.libraries or to_library_id not in self.libraries:
            return 0
        
        from_lib = self.libraries[from_library_id]
        to_lib = self.libraries[to_library_id]
        
        moved_count = 0
        books_to_move = []
        
        # Find books to move
        for book in from_lib.books:
            if book.title in book_titles:
                books_to_move.append(book)
        
        # Move books
        for book in books_to_move:
            from_lib.books.remove(book)
            to_lib.books.append(book)
            moved_count += 1
        
        # Save both libraries
        if moved_count > 0:
            from_lib.save_books()
            to_lib.save_books()
        
        return moved_count
    
    def get_all_books_count(self) -> int:
        """Get total number of books across all libraries"""
        total = sum(len(library.books) for library in self.libraries.values())
        total += len(self.dnf_books)
        return total
    
    def get_dnf_books(self):
        """Get DNF books (shared across all libraries)"""
        return self.dnf_books