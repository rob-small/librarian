# Library Management System

A simple library management system implemented in Python that helps track books, patrons, and loans.

## Features

- Add and manage books
- Register and manage patrons
- Handle book loans and returns
- Track overdue books
- Chat with LLM with integrated library access via MCP tools
- LLM can directly manage library operations through natural conversation
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

### Option 1: Run in Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or use the provided script
bash run_container.sh
```

Access the app at http://localhost:7860

### Option 2: Run Locally

```bash
python main.py
```

This will launch a web interface where you can:
- Add new books to the library
- Register new patrons
- Borrow and return books
- View the status of all books, patrons, and overdue loans
- Chat with a local LLM (if running)

The interface will be available at http://localhost:7860 by default.

### Option 3: Run in Docker with Custom Settings

```bash
docker run -p 7860:7860 \
  -e LLM_API_URL=http://host.docker.internal:1234/v1/chat/completions \
  -e LLM_MODEL_NAME=llama2 \
  librarian:latest
```

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

- `LANGSMITH_TRACING`: Enable LangSmith tracing (`true`/`false`)
  - Default: `false`
  - Set to `true` to log chat runs and token usage

- `LANGSMITH_API_KEY`: LangSmith API key (required when tracing is enabled)
  - Used by the LangSmith SDK for authenticated tracing

- `LANGSMITH_PROJECT`: LangSmith project name
  - Default: `librarian`

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
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=librarian
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

## MCP (Model Context Protocol) Integration

The application features an embedded MCP server that exposes library operations as tools to the LLM. This allows the LLM to directly interact with the library system through natural language conversation.

### Available Tools

The LLM has access to the following library tools:

- **add_book**: Add a new book to the library
- **add_patron**: Register a new patron
- **borrow_book**: Borrow a book for a patron
- **return_book**: Return a borrowed book
- **list_books**: View all books and their availability status
- **list_patrons**: View all registered patrons
- **get_overdue_loans**: Check for overdue books
- **get_book_info**: Get detailed information about a specific book
- **get_patron_info**: Get detailed information about a specific patron

### Example Chat Interactions

Once the application is running, you can chat with the LLM in the "Chat with LLM" tab and have natural conversations like:

- "Add a book called 'Python Programming' by Guido van Rossum with ISBN 123-456-789"
- "Show me all books in the library"
- "Register a new patron named Alice Smith with email alice@example.com and phone 555-1234"
- "Borrow book 1 for patron 1"
- "What books are overdue?"
- "Get info about patron 2"

The LLM will understand your requests and execute the appropriate library operations, then provide you with the results.

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
