# MCP Integration Guide

## Overview

This Library Management System now includes a built-in Model Context Protocol (MCP) server that allows LLMs to interact with library operations through function calling.

## Architecture

### Components

1. **LibraryMCPServer** (`src/mcp_server.py`)
   - Defines 9 library tools available to the LLM
   - Translates tool calls into library operations
   - Handles errors and returns formatted results

2. **Chat Interface Integration** (`src/interface.py`)
   - The `chat_with_llm()` function now includes MCP tools
   - Sends available tools to the LLM with each request
   - Handles tool execution when the LLM requests it
   - Supports iterative tool usage for complex tasks

3. **LibraryInterface & LibrarySystem** (existing)
   - Core business logic unchanged
   - MCP server wraps these operations for LLM access

## How It Works

1. **User sends a message** in the "Chat with LLM" tab
2. **Message is sent to the LLM** along with available library tools
3. **LLM decides** if it needs to use any tools to answer the question
4. **If tools are needed:**
   - LLM specifies which tool(s) to call with arguments
   - MCP server executes the tools locally
   - Results are sent back to the LLM
   - LLM formulates a natural language response
5. **Response is displayed** to the user

## Available Tools

### Book Management
- `add_book(title, author, isbn)` - Add a book to the library
- `get_book_info(book_id)` - Get detailed info about a specific book
- `list_books()` - List all books with availability status

### Patron Management
- `add_patron(name, email, phone)` - Register a patron
- `get_patron_info(patron_id)` - Get patron details and loan info
- `list_patrons()` - List all patrons

### Loan Management
- `borrow_book(book_id, patron_id, days)` - Borrow a book (14 days default)
- `return_book(book_id)` - Return a borrowed book
- `get_overdue_loans()` - Get all overdue books

## Configuration

### LLM Requirements

The LLM service must support:
- OpenAI-compatible API format (`/v1/chat/completions`)
- Function calling / tool use capability
- Bearer token authentication (if needed)

**Compatible Services:**
- LM Studio (local)
- OpenAI API
- Anthropic Claude API
- Any OpenAI-compatible endpoint with tool support

### Environment Variables

```bash
# LLM API endpoint
export LLM_API_URL="http://host.docker.internal:1234/v1/chat/completions"

# API key (optional, required for hosted services)
export LLM_API_KEY="your-api-key"
```

## Examples

### Example 1: Simple Query
**User:** "How many books are in the library?"
1. LLM calls `list_books()`
2. Gets list of all books
3. Returns: "There are 3 books in the library: 'The Great Gatsby', 'To Kill a Mockingbird', and '1984'"

### Example 2: Complex Operation
**User:** "Add a new book by Stephen King called 'The Shining' with ISBN 978-0385333312, then show me all books"
1. LLM calls `add_book("The Shining", "Stephen King", "978-0385333312")`
2. LLM calls `list_books()`
3. Returns: "I've added 'The Shining' to the library. Here are all books: [list of books]"

### Example 3: Multi-Step Task
**User:** "Register Jane Doe, email jane@example.com, phone 555-0123, then borrow book 1 for her"
1. LLM calls `add_patron("Jane Doe", "jane@example.com", "555-0123")` → Patron ID: 5
2. LLM calls `borrow_book(1, 5, 14)`
3. Returns: "Jane Doe has been registered and book 1 is now borrowed for 14 days"

## Error Handling

- All tool calls are wrapped in try-catch
- Errors are returned as meaningful messages to the LLM
- LLM can handle errors and suggest alternatives or retry

## Security Considerations

1. **API Key Protection**
   - API keys should be stored in environment variables, not hardcoded
   - Use `.env` files locally (excluded from git)
   - In production, use proper secrets management

2. **Input Validation**
   - MCP server validates tool inputs
   - Invalid IDs or parameters return appropriate errors

3. **Rate Limiting**
   - Consider implementing rate limiting for production use
   - Set appropriate timeouts (currently 30 seconds)

## Future Enhancements

- Persistent storage (database integration)
- User authentication for library access
- Advanced filtering and search in tools
- Notifications for overdue items
- Book reservations and holds
- Integration with external book APIs (ISBN lookup)
