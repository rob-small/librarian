# Chat with LLM - Feature Guide

## Overview

The "Chat with LLM" tab in the Gradio interface allows you to have a natural conversation with an LLM that has direct access to all library management functions.

## How to Use

### Basic Steps

1. Navigate to the "Chat with LLM" tab
2. Type your request in the message box
3. Click "Send"
4. The LLM will:
   - Understand your request
   - Call appropriate library tools if needed
   - Process the results
   - Provide a natural language response

### Examples of What You Can Ask

#### Book Queries
- "What books are available?"
- "Do you have any books by Stephen King?"
- "Tell me about book number 3"
- "How many books are in the library?"

#### Adding Books
- "Add a new book: 'The Hobbit' by J.R.R. Tolkien, ISBN 978-0547928227"
- "Can you add this book to our collection: [Title], [Author], [ISBN]?"

#### Patron Management
- "Register a new patron: John Smith, john.smith@email.com, 555-1234"
- "Show me all library members"
- "Get information about patron 1"

#### Borrowing Books
- "Can Jane Doe borrow book 2?"
- "Let patron 3 borrow book 1 for 21 days"
- "I want to borrow the Great Gatsby"

#### Returning Books
- "Return book 1"
- "I'm done with book 2, time to return it"

#### Status Checks
- "Are there any overdue books?"
- "Show me what patron 1 has borrowed"
- "List all patrons and their loans"

#### Complex Tasks
- "Register Alice Brown (alice@email.com, 555-5678) and let her borrow book 1 for 30 days"
- "Show all available books and which patrons have active loans"

## LLM Requirements

Your LLM must support:

### 1. Function Calling / Tool Use
The LLM needs to be able to:
- Recognize when it needs to use a tool
- Specify which tool to call
- Provide the correct arguments

### 2. OpenAI API Format
The LLM service should support the OpenAI `/v1/chat/completions` endpoint format with tools/functions.

### 3. Adequate Context Window
Recommended: At least 2K token context window for comfortable multi-step operations.

## Supported LLM Services

### Local (Recommended for Development)
- **LM Studio** (default)
  - Free to use locally
  - Good for testing
  - Default URL: `http://host.docker.internal:1234/v1/chat/completions`

### Hosted Services
- **OpenAI GPT-4 / GPT-3.5**
  - High quality responses
  - Requires API key
  - URL: `https://api.openai.com/v1/chat/completions`

- **Anthropic Claude**
  - Via OpenAI-compatible proxy
  - Requires API key

## Configuration

### For Local LM Studio

1. Start LM Studio with a model loaded
2. Ensure it's accessible at `http://host.docker.internal:1234` (Docker) or `http://localhost:1234` (local)
3. Run the app - it will connect automatically

### For OpenAI

```bash
export LLM_API_URL="https://api.openai.com/v1/chat/completions"
export LLM_API_KEY="sk-your-api-key"
python main.py
```

### For Docker with Custom LLM

```bash
docker run \
  -e LLM_API_URL="your-llm-url" \
  -e LLM_API_KEY="your-api-key" \
  -p 7860:7860 \
  librarian
```

## Troubleshooting

### "Error: Connection refused"
- Check that your LLM service is running
- Verify the LLM_API_URL is correct
- For Docker, use `host.docker.internal` instead of `localhost`

### "Error: Invalid API key"
- Verify your LLM_API_KEY is correct
- Ensure the key hasn't expired

### LLM doesn't call tools
- Some models may need prompt engineering
- Ensure your LLM supports function calling
- Try rephrasing your request more clearly

### Tool execution error
- Check the tool parameters are in the right format
- Verify book/patron IDs exist before using them
- Look at the error message for specific issues

## Advanced Usage

### Batch Operations

You can ask the LLM to perform multiple operations:

"1. Add these 3 books to the library: [books list]
 2. Register these 2 new patrons: [patrons list]
 3. Let patron 1 borrow book 1 for 14 days
 4. Let patron 2 borrow book 2 for 21 days"

The LLM will intelligently break this down and execute each step.

### Natural Language Clarification

The LLM can ask for clarification:

User: "Borrow a book"
LLM: "I'd be happy to help with borrowing a book! Could you please provide:
- The book ID or title
- The patron ID or name
- How many days (default is 14)"

### Error Recovery

If an operation fails, the LLM will explain why and suggest alternatives:

User: "Borrow book 100"
LLM: "Book 100 doesn't exist. Here are the available books: [list]"

## Tips for Best Results

1. **Be specific** - Include IDs when possible
2. **Use natural language** - The LLM understands conversational requests
3. **Ask follow-up questions** - The chat history is maintained
4. **Batch related operations** - Group similar requests together
5. **Check status often** - Use list and info commands to verify state

## Privacy & Security

- All data stays in your system (if using local LLM)
- API keys are passed securely via headers
- No chat history is stored on external servers
- Tool outputs are shown only to the user in this session

## Performance Notes

- First request may take a few seconds (LLM startup)
- Complex operations with multiple tool calls take longer
- Local LLMs (LM Studio) are typically faster than cloud services
- Timeout is set to 30 seconds per request
