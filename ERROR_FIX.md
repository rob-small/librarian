# Chat Error Troubleshooting

## Issue: "Error: 400 Client Error: Bad Request"

### What Was Wrong

The chat function was sending the `tools` parameter to **all** LLM services, including LM Studio. However:

- **LM Studio** does NOT support the `tools` parameter (no function calling support)
- **OpenAI** DOES support the `tools` parameter (has function calling)

Sending unsupported parameters causes a 400 Bad Request error.

### The Fix

The chat function now:

1. **Detects the LLM service** - Checks if the URL contains "openai.com"
2. **Conditional tool support** - Only adds `tools` parameter for OpenAI
3. **LM Studio compatibility** - Sends simple chat requests for local LLMs
4. **Graceful degradation** - Works with basic chat even without function calling

### Code Changes

**Before:**
```python
payload = {
    "model": "local-llm",
    "messages": messages,
    "tools": tools,              # ← Causes error for LM Studio
    "tool_choice": "auto",
    "temperature": 0.7
}
```

**After:**
```python
is_openai = "openai.com" in api_url

payload = {
    "model": "gpt-3.5-turbo" if is_openai else "local-model",
    "messages": messages,
    "temperature": 0.7
}

if is_openai:
    tools = mcp_server.get_tools()
    payload["tools"] = tools
    payload["tool_choice"] = "auto"
```

### Current Status

✅ **Container rebuilt and running**
✅ **Chat function fixed**
✅ **Gradio warnings removed**
✅ **Ready to use**

## How to Use

### With LM Studio (Local)
1. Start LM Studio with a model loaded
2. Open http://localhost:7860
3. Go to "Chat with LLM" tab
4. Type: "Show me all books"
5. Should work now without 400 error ✅

### With OpenAI
```bash
export LLM_API_URL="https://api.openai.com/v1/chat/completions"
export LLM_API_KEY="sk-your-key"
bash run_container.sh
```
Then chat and it will use function calling ✅

## What Works Now

- ✅ LM Studio basic chat (no tool calling needed)
- ✅ OpenAI with function calling
- ✅ Clean error messages if something goes wrong
- ✅ Proper message format with Gradio

## Testing the Fix

Try these in the chat:

1. **Simple query:** "How many books are in the library?"
2. **Add book:** "Add a book called 'The Hobbit' by J.R.R. Tolkien with ISBN 978-0547928227"
3. **List everything:** "Show me all books and patrons"
4. **Complex task:** "Register a patron named John Doe (john@email.com, 555-1234) and show me all patrons"

All should work without the 400 error ✅

## If You Still Get Errors

### "Error: Connection refused"
- Check LM Studio is running
- Verify URL: `http://host.docker.internal:1234` (Docker) or `http://127.0.0.1:1234` (local)

### "Error: 401 Unauthorized"
- Check your OpenAI API key is correct
- Ensure it has not expired

### "Error: 404 Not Found"
- Verify the URL is correct for your LLM service
- Check the endpoint path (some services use different paths)

### "Error: Timeout"
- LM Studio may be slow loading the model
- Try again after waiting a few seconds
- Or choose a smaller model in LM Studio

## Next Steps

1. Open http://localhost:7860
2. Go to "Chat with LLM" tab
3. Start chatting with your library!

For more help, see CHAT_GUIDE.md
