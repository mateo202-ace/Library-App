# ReadWise - Smart Reading Management

This is a Python application for managing a personal book library using Flet for the GUI with **multi-library support** and **Harry Potter house-themed UI**.

## Running the Application
```bash
python readwise.py
```

## 🌟 Major Features
- ✅ **Multi-Library System** - Up to 5 custom libraries + global DNF
- ✅ **Harry Potter House Themes** - 🦁 Gryffindor, 🦅 Ravenclaw, 🦡 Hufflepuff, 🐍 Slytherin + Light/Dark
- ✅ **Library Management** - Create, switch, delete libraries with confirmation dialogs
- ✅ **Book Management** - Add, edit, delete with status tracking
- ✅ **Advanced Filtering** - Search, status, rating, sorting with 6 options
- ✅ **Colorful Statistics** - House-themed stat cards, rainbow genre breakdown
- ✅ **Global DNF System** - Centralized "Did Not Finish" for AI recommendations
- ✅ **Professional UI** - Clean cards, proper contrast, theme-aware components
- ✅ **ISBN Lookup** - Integration with Open Library and Google Books APIs
- ✅ **Progress Tracking** - Pages, ratings, reviews, reading time

## 🏰 Current Theme System
### House Themes (Dark backgrounds with house accents):
- **🦁 Gryffindor**: Dark brown/grey with gold/amber accents
- **🦅 Ravenclaw**: Deep navy blue with light blue accents  
- **🦡 Hufflepuff**: Dark brown with yellow accents
- **🐍 Slytherin**: Dark grey with green accents

### Classic Themes:
- **Light**: Clean white with blue accents
- **Dark**: Dark grey with blue accents

## 📁 Updated File Structure
```
ReadWise/
├── readwise.py              # Main application with multi-library & themes
├── src/
│   ├── models/
│   │   ├── book.py         # Book data model and logic
│   │   ├── library.py      # Single library management
│   │   └── library_manager.py # NEW: Multi-library manager (max 5)
│   ├── utils/
│   │   ├── book_api.py     # ISBN lookup and book search APIs
│   │   └── export_utils.py # CSV, JSON, and report export functions
│   └── data/
│       ├── books_main.csv  # Main library books (CSV format)
│       ├── books_main_extended.json # Main library extended data
│       ├── dnf_books.csv   # Global DNF books
│       ├── dnf_books_extended.json # DNF extended data
│       ├── libraries_config.json # NEW: Library metadata & settings
│       └── settings.json   # NEW: User preferences (theme, etc.)
├── assets/
│   ├── exports/            # Generated export files
│   └── images/             # Book covers and app images
└── CLAUDE.md              # This updated documentation
```

## 🛠️ Developer Cheat Sheet - Where to Make Changes

### 🎨 **Theme System**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **House theme colors** | `readwise.py` | `self.themes` dictionary | ~24-80 |
| **Theme switching** | `readwise.py` | `change_theme()` method | ~140-180 |
| **Theme persistence** | `readwise.py` | `save_theme_preference()` | ~95-111 |
| **Component theming** | `readwise.py` | `get_theme_colors()` | ~113-115 |
| **Settings theme selector** | `readwise.py` | `show_settings_view()` | ~982-1047 |

### 📚 **Multi-Library System**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **Library creation** | `readwise.py` | `show_create_library_dialog()` | ~429-495 |
| **Library management** | `readwise.py` | `show_manage_libraries_dialog()` | ~497-571 |
| **Library deletion** | `readwise.py` | `confirm_delete_library()` | ~573-625 |
| **Library switching** | `readwise.py` | `library_change()` | ~403-427 |
| **Library dropdown** | `readwise.py` | `update_library_dropdown_options()` | ~369-401 |
| **LibraryManager core** | `src/models/library_manager.py` | Entire file | All |

### 📱 **User Interface Changes**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **Navigation sidebar** | `readwise.py` | Navigation rail setup | ~199-224 |
| **Book card appearance** | `readwise.py` | `create_book_card()` | ~1092-1175 |
| **Statistics dashboard** | `readwise.py` | `show_statistics_view()` | ~797-980 |
| **Colorful genre breakdown** | `readwise.py` | Statistics genre section | ~855-895 |
| **Search & filter styling** | `readwise.py` | `show_library_view_without_refresh()` | ~646-748 |
| **House-themed stat cards** | `readwise.py` | `create_stat_card_with_emoji()` | ~1071-1090 |

### 📊 **Enhanced Statistics**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **House-specific icons** | `readwise.py` | `house_stat_icons` dictionary | ~805-843 |
| **Colorful progress bars** | `readwise.py` | Genre breakdown section | ~860-895 |
| **Quick stats cards** | `readwise.py` | `quick_stats` section | ~897-935 |
| **Statistics calculations** | `src/models/library.py` | `get_reading_statistics()` | ~279-310 |

### 📚 **Book Management**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **Add new book** | `readwise.py` | `add_book()` method | ~516-540 |
| **Edit existing book** | `readwise.py` | `save_book_edit()` | ~669-740 |
| **Book status changes** | `readwise.py` | Status change logic | ~690-700 |
| **DNF book transfers** | `src/models/library.py` | `move_to_dnf()`, `move_from_dnf()` | ~178-205 |
| **Book search/filtering** | `readwise.py` | `refresh_book_list()` | ~452-490 |
| **Book sorting** | `readwise.py` | Sort logic in `refresh_book_list()` | ~459-474 |

### 💾 **Data Storage & Files**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **CSV file handling** | `src/models/library.py` | `save_books_to_csv()` | ~129-160 |
| **JSON file handling** | `src/models/library.py` | `save_books_to_json()` | ~117-127 |
| **DNF books storage** | `src/models/library.py` | `save_dnf_books()` | ~193-225 |
| **Data loading** | `src/models/library.py` | `load_books()`, `load_dnf_books()` | ~16-115 |
| **File paths** | `readwise.py` | `__init__()` method | ~15-20 |

### 🔍 **Search & Filter Features**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **Search functionality** | `readwise.py` | `search_books()` method | ~480-482 |
| **Status filtering** | `readwise.py` | Filter dropdown logic | ~447-457 |
| **Book sorting** | `readwise.py` | Sort dropdown logic | ~459-474 |
| **Book list display** | `readwise.py` | `refresh_book_list()` | ~430-490 |

### 🌐 **API & External Services**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **ISBN lookup** | `src/utils/book_api.py` | `lookup_isbn()` | Entire file |
| **Book cover fetching** | `src/utils/book_api.py` | Cover URL methods | Entire file |
| **API error handling** | `src/utils/book_api.py` | Exception blocks | Throughout |


### 🎨 **Visual & UI Styling**
| What you want to change | File | Method/Location | Line Range |
|-------------------------|------|-----------------|------------|
| **Status colors** | `readwise.py` | `create_book_card()` | ~376-381 |
| **Card styling** | `readwise.py` | Container/Card properties | Throughout |
| **Button styles** | `readwise.py` | Button definitions | Throughout |
| **Layout spacing** | `readwise.py` | Container margins/padding | Throughout |

### 🔧 **Common Quick Fixes**
| Issue | File | What to look for |
|-------|------|------------------|
| **App won't start** | `readwise.py` | File paths in `__init__()` around line 16-18 |
| **Books not saving** | `src/models/library.py` | `save_books()` method around line 159 |
| **Statistics wrong** | `src/models/library.py` | `get_reading_statistics()` around line 279 |
| **DNF not working** | `src/models/library.py` | `move_to_dnf()` around line 178 |
| **Edit dialog issues** | `readwise.py` | `show_edit_book_dialog()` around line 580 |

### 📝 **Data File Locations**
- **Main books**: `src/data/books.csv` and `src/data/books_extended.json`
- **DNF books**: `src/data/dnf_books.csv` and `src/data/dnf_books_extended.json`
- **Exports**: `assets/exports/`

---

## What Each File Controls

## Data Storage
The app uses a dual storage system:
- **CSV files** for backward compatibility
- **JSON files** for extended features (progress, ratings, reviews)

## Dependencies
```bash
pip install flet requests
```

## 🏗️ Architecture Overview

### Navigation Structure
```
📚 [Library Dropdown ▼] | Statistics | Settings
├─ 📚 Main Library
├─ 📚 Custom Library 1  
├─ 📚 Custom Library 2
├─ 🚫 Did Not Finish (Global)
├─ ➕ New Library (if < 5)
└─ ⚙️ Manage Libraries
```

### Theme System Architecture
- **6 total themes**: Light, Dark, + 4 house themes
- **Persistent storage**: Saved to `settings.json`
- **Live switching**: Instant UI updates without restart
- **Component theming**: All UI elements respect current theme
- **Contrast optimization**: White text on dark, black text on white

### Multi-Library Data Flow
1. **LibraryManager** manages up to 5 libraries + global DNF
2. **Per-library files**: `books_main.csv`, `books_custom_id.csv`
3. **Global DNF**: Shared across all libraries for AI training
4. **Metadata**: `libraries_config.json` stores library info

## 🔧 Latest Major Updates

### Theme System Implementation (Latest)
- ✅ **6 Professional Themes** - Light, Dark, + 4 house themes with proper contrast
- ✅ **House Color Schemes** - Dark atmospheric backgrounds with bright accents
- ✅ **Readability Fixes** - White text on dark, white dropdowns for clarity
- ✅ **Navigation Theming** - Proper contrast for sidebar and labels
- ✅ **Component Theming** - All inputs, cards, and text properly themed

### Multi-Library System  
- ✅ **Library Management** - Create, switch, delete with max 5 limit
- ✅ **Global DNF System** - Centralized "Did Not Finish" books
- ✅ **Library Dropdown** - Clean navigation with icons and actions
- ✅ **Confirmation Dialogs** - Safe deletion with warnings
- ✅ **File Organization** - Separate storage per library

### Enhanced Statistics Dashboard
- ✅ **Colorful Genre Breakdown** - Rainbow progress bars for each genre
- ✅ **House-Themed Icons** - Different emoji sets per house theme
- ✅ **Quick Stats Cards** - Additional mini-statistics
- ✅ **Professional Layout** - Clean cards with borders and spacing

### UI/UX Improvements
- ✅ **Professional Card Design** - Clean Material Design cards
- ✅ **Overlay Dialogs** - Fixed dialog display issues
- ✅ **Comprehensive Sorting** - 6 sorting options (Status, Name, Author, etc.)
- ✅ **Enhanced Search/Filter** - Themed components with proper labels
- ✅ **Book Card Styling** - House-themed colors and content