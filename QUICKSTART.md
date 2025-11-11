# Quick Start: MCP-Enabled Chat with Library System

## TL;DR - Get Started in 5 Minutes

### 1. Prerequisites
- Docker running
- LM Studio installed and running with a model loaded (or OpenAI API key)

### 2. Build and Run
```bash
cd /home/dell/mycode/librarian
bash run_container.sh
```

### 3. Access the App
- Open browser: `http://localhost:7860`
- Navigate to "Chat with LLM" tab

### 4. Chat Examples
```
"Show all books"
"Add book: The Hobbit by J.R.R. Tolkien, ISBN 978-0547928227"
"Register patron: Alice Smith, alice@email.com, 555-1234"
"Borrow book 1 for patron 1"
"What books are overdue?"
```

## Using OpenAI Instead of Local LLM

```bash
export LLM_API_URL="https://api.openai.com/v1/chat/completions"
export LLM_API_KEY="sk-your-actual-key"
bash run_container.sh
```

## Verify It's Working

```bash
# Test MCP server directly
python example_mcp_usage.py
```

Should output:
```
Available Tools:
  - add_book
  - add_patron
  - borrow_book
  - return_book
  - list_books
  - list_patrons
  - get_overdue_loans
  - get_book_info
  - get_patron_info

Executing Tool Examples:
1. Listing all books:
   Result: No books in the library
[... more examples ...]
```

## What Just Happened?

You now have:
1. ✓ A Gradio web interface for the library system
2. ✓ MCP server exposing 9 library operations as tools
3. ✓ LLM integration with function calling
4. ✓ Natural language interface to manage the library
5. ✓ Containerized application ready for deployment

## Advanced: Custom LLM Service

Any service with OpenAI API compatibility:

```bash
export LLM_API_URL="https://your-service.com/v1/chat/completions"
export LLM_API_KEY="your-api-key"
bash run_container.sh
```

## Documentation

- **MCP_INTEGRATION.md** - Technical deep dive
- **CHAT_GUIDE.md** - User guide for Chat feature
- **MCP_SETUP.md** - Complete setup guide
- **README.md** - Overall project documentation

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Check LLM is running at configured URL |
| "No tools available" | Verify LLM supports function calling |
| Docker can't reach LM Studio | Use `host.docker.internal` (already configured) |
| "Error: Invalid API key" | Check OpenAI key is correct and has credits |

## Example Conversation

```
You: "Add 3 books: 1984, Brave New World, and Fahrenheit 451"
LLM: [Calls add_book tool 3 times]
Response: "I've added all 3 books to the library!"

You: "Register 2 new patrons"
LLM: "I'd be happy to help! Could you provide their names, emails, and phone numbers?"

You: "John Doe john@example.com 555-1111, Jane Smith jane@example.com 555-2222"
LLM: [Calls add_patron tool 2 times]
Response: "Both patrons registered successfully!"

You: "Lend 1984 to John"
LLM: [Looks up book and patron, calls borrow_book]
Response: "John Doe has borrowed '1984'. Due date is 2024-11-24"
```

## Next Steps

1. Read **MCP_INTEGRATION.md** for architecture details
2. Read **CHAT_GUIDE.md** for usage examples
3. Explore the **Chat with LLM** tab
4. Try the **example_mcp_usage.py** script
5. Customize tools in **src/mcp_server.py** as needed

## Need Help?

Check the documentation files or review the error messages from the LLM - they're usually descriptive and can guide you to the solution!
