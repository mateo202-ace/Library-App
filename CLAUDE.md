# ReadWise - Smart Reading Management

This is a Python application for managing a personal book library using Flet for the GUI.

## Running the Application
```bash
python readwise.py
```

## Features
- ✅ Book management (add, edit, delete)
- ✅ Multiple status tracking (To Be Read, Currently Reading, Finished, DNF)
- ✅ Reading progress tracking with pages and time
- ✅ Star ratings and reviews
- ✅ Search and filtering capabilities
- ✅ Statistics dashboard with visual progress indicators
- ✅ DNF (Did Not Finish) books section
- ✅ Import/Export functionality (CSV, JSON, Reading Reports)
- ✅ ISBN lookup integration with Open Library and Google Books APIs
- ✅ Modern GUI with left navigation rail
- ✅ Clean, organized folder structure

## File Structure
```
ReadWise/
├── readwise.py              # Main application (run this)
├── src/
│   ├── models/
│   │   ├── book.py         # Book data model and logic
│   │   └── library.py      # Library management and statistics
│   ├── utils/
│   │   ├── book_api.py     # ISBN lookup and book search APIs
│   │   └── export_utils.py # CSV, JSON, and report export functions
│   └── data/
│       ├── books.csv       # Main book data (CSV format)
│       └── books_extended.json # Extended book data with all features
├── assets/
│   ├── exports/            # Generated export files
│   └── images/             # Book covers and app images
└── CLAUDE.md              # This documentation
```

## What Each File Controls
- **Navigation issues** → Check `readwise.py` (nav_change method)
- **Book display problems** → Check `readwise.py` (create_book_card method)  
- **Search/filter not working** → Check `readwise.py` (refresh_book_list method)
- **Data not saving** → Check `src/models/library.py`
- **API issues** → Check `src/utils/book_api.py`
- **Export problems** → Check `src/utils/export_utils.py`

## Data Storage
The app uses a dual storage system:
- **CSV files** for backward compatibility
- **JSON files** for extended features (progress, ratings, reviews)

## Dependencies
```bash
pip install flet requests
```

## Recent Changes
- Cleaned up folder structure by removing unused files
- Renamed from "Andreas Library Manager" to "ReadWise"
- Fixed all major functionality issues
- Maintained working color scheme and navigation
- Consolidated into single reliable application file