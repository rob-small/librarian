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

The application includes a "Chat with LLM" tab that connects to any LLM service using the OpenAI API format. This supports both local LLMs (e.g., LM Studio) and hosted services (e.g., OpenAI, Anthropic).

### Configuration

The LLM API endpoint and authentication key can be configured using environment variables:

**Environment Variables:**
- `LLM_API_URL`: URL endpoint for the LLM API
  - Default: `http://host.docker.internal:1234/v1/chat/completions` (for Docker)
  - Example: `http://127.0.0.1:1234/v1/chat/completions` (for local development)
  - Example: `https://api.openai.com/v1/chat/completions` (for OpenAI)

- `LLM_API_KEY`: Optional API key for authentication
  - Not required for local LLMs (e.g., LM Studio)
  - Required for hosted services (e.g., OpenAI, Anthropic)
  - The key is passed as a Bearer token in the Authorization header

### Usage Examples

#### Local Development (LM Studio)
```bash
export LLM_API_URL="http://127.0.0.1:1234/v1/chat/completions"
python main.py
```

#### Docker (LM Studio)
```bash
# Default configuration (assumes LM Studio on host)
docker-compose up --build

# Or with explicit URL
docker run -e LLM_API_URL="http://host.docker.internal:1234/v1/chat/completions" -p 7860:7860 librarian
```

#### OpenAI API
```bash
export LLM_API_URL="https://api.openai.com/v1/chat/completions"
export LLM_API_KEY="sk-your-api-key-here"
python main.py
```

#### Docker with OpenAI
```bash
docker run \
  -e LLM_API_URL="https://api.openai.com/v1/chat/completions" \
  -e LLM_API_KEY="sk-your-api-key-here" \
  -p 7860:7860 \
  librarian
```

#### Other Hosted LLM Services (e.g., Anthropic, Replicate)
```bash
export LLM_API_URL="https://api.your-llm-service.com/v1/chat/completions"
export LLM_API_KEY="your-api-key"
python main.py
```

### Docker Compose with Environment Variables

You can also specify these variables in a `.env` file and reference them in `docker-compose.yml`:

**`.env` file:**
```
LLM_API_URL=http://host.docker.internal:1234/v1/chat/completions
LLM_API_KEY=
```

**`docker-compose.yml`:**
```yaml
version: '3'
services:
  librarian:
    build: .
    ports:
      - "7860:7860"
    env_file:
      - .env
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