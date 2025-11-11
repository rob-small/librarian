# Library Management System

A simple library management system implemented in Python that helps track books, patrons, and loans.

## Features

- Add and manage books
- Register and manage patrons
- Handle book loans and returns
- Track overdue books
- Basic testing suite

## Project Structure

```
library_system/
├── src/
│   ├── __init__.py
│   ├── models.py
│   └── library.py
├── tests/
│   └── test_library.py
├── main.py
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.8 or higher
- pytest (for running tests)
- gradio (for web interface)
- requests (for LLM API communication)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

```
python main.py
```

This will launch a web interface where you can:
- Add new books to the library
- Register new patrons
- Borrow and return books
- View the status of all books, patrons, and overdue loans
- Chat with a local LLM (if running)

The interface will be available at http://localhost:7860 by default.

## LLM Chat Integration

The application includes a "Chat with LLM" tab that connects to a local LLM running on your machine using the OpenAI API format (e.g., LM Studio).

### Configuration

The LLM API endpoint can be configured using the `LLM_API_URL` environment variable:

```bash
# Default (for Docker container)
export LLM_API_URL="http://host.docker.internal:1234/v1/chat/completions"

# For local development
export LLM_API_URL="http://127.0.0.1:1234/v1/chat/completions"

python main.py
```

### Docker Usage

When running in Docker, use the default URL `http://host.docker.internal:1234/v1/chat/completions` which allows the container to reach the host machine's LLM.

To run the application with a custom LLM URL in Docker:

```bash
docker run -e LLM_API_URL="http://host.docker.internal:1234/v1/chat/completions" -p 7860:7860 librarian
```

## Running Tests

```
pytest
```

## Usage Example

```python
from src.library import LibrarySystem

# Initialize the library system
library = LibrarySystem()

# Add a book
book = library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")

# Add a patron
patron = library.add_patron("John Doe", "john@example.com", "123-456-7890")

# Borrow a book
loan = library.borrow_book(book.id, patron.id)

# Return a book
library.return_book(book.id)
```