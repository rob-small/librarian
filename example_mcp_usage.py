"""
example_mcp_usage.py
--------------------
Example script demonstrating direct usage of the LibraryMCPServer.
This can be used for testing or integration with other systems.
"""

from src.library import LibrarySystem
from src.mcp_server import LibraryMCPServer
import json
import requests
import os
from dotenv import load_dotenv
import re


def _try_execute_tools_from_text(content, mcp_server, messages, payload, llm_api_url, headers):
    """
    Attempt to detect and execute tool calls from LLM response text.
    This handles LLMs that return tool calls as JSON in the content field
    instead of using the native tool_calls format.
    
    Returns True if tools were executed, False otherwise.
    """
    try:
        # Look for JSON array patterns in the response that might contain tool calls
        json_pattern = r'\[.*?\]'
        json_matches = re.findall(json_pattern, content, re.DOTALL)
        
        # Tool aliases for LLM response names
        tool_aliases = {
            "get_all_books": "list_books",
            "get_all_patrons": "list_patrons",
            "get_books": "list_books",
            "get_patrons": "list_patrons",
        }
        
        # Get list of valid tool names from MCP server (including aliases)
        valid_tools = set([t["name"] for t in mcp_server.get_tools()])
        valid_tools.update(tool_aliases.keys())
        
        for json_str in json_matches:
            try:
                parsed = json.loads(json_str)
                if isinstance(parsed, list) and len(parsed) > 0:
                    # Check if this looks like tool calls
                    if all(isinstance(item, dict) and "name" in item for item in parsed):
                        print("\n  LLM is invoking tools (detected from text)...")
                        
                        # Convert text format to tool_calls format
                        for tool_call_data in parsed:
                            tool_name = tool_call_data.get("name")
                            tool_args = tool_call_data.get("arguments", {})
                            
                            if tool_name and tool_name in valid_tools:
                                print(f"    - Calling {tool_name} with args: {tool_args}")
                                result = mcp_server.execute_tool(tool_name, tool_args)
                                print(f"      Result: {result}")
                                
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": f"call_{tool_name}",
                                    "name": tool_name,
                                    "content": json.dumps(result) if not isinstance(result, str) else result
                                })
                        
                        # Get final response from LLM with tool results
                        payload["messages"] = messages
                        try:
                            response = requests.post(llm_api_url, json=payload, headers=headers, timeout=30)
                            response.raise_for_status()
                            data = response.json()
                            if "choices" in data and len(data["choices"]) > 0:
                                final_message = data["choices"][0]["message"]
                                final_response = final_message.get('content', 'No response')
                                print(f"\n  LLM Final Response:\n    {final_response}\n")
                        except Exception:
                            pass
                        
                        return True
            except (json.JSONDecodeError, TypeError):
                continue
        
        return False
    except Exception as e:
        print(f"  Warning: Could not parse tool calls from text: {e}")
        return False


def call_llm_with_mcp_tools(mcp_server, user_query, llm_api_url=None, llm_api_key=None, llm_model_name=None):
    """
    Make an LLM call with MCP tools available for function calling.
    
    Args:
        mcp_server: LibraryMCPServer instance
        user_query: User's question or request
        llm_api_url: LLM API endpoint
        llm_api_key: Optional API key
        llm_model_name: Model name to use
    
    Returns:
        The LLM's response as a string
    """
    if not llm_api_url:
        print("Error: LLM_API_URL not configured. Skipping LLM call.")
        return None
    
    headers = {"Content-Type": "application/json"}
    if llm_api_key:
        headers["Authorization"] = f"Bearer {llm_api_key}"
    
    # Determine model name
    if llm_model_name:
        model_name = llm_model_name
    elif "openai.com" in llm_api_url:
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "local-model"
    
    # Define library tools for the LLM
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_all_books",
                "description": "Get all books in the library",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_all_patrons",
                "description": "Get all patrons in the library",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_book",
                "description": "Add a new book to the library",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "author": {"type": "string"},
                        "isbn": {"type": "string"}
                    },
                    "required": ["title", "author", "isbn"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "borrow_book",
                "description": "Borrow a book for a patron",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer"},
                        "patron_id": {"type": "integer"},
                        "loan_days": {"type": "integer", "default": 14}
                    },
                    "required": ["book_id", "patron_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_overdue_loans",
                "description": "Get all overdue loans",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        }
    ]
    
    # Build the request
    messages = [{"role": "user", "content": user_query}]
    payload = {
        "model": model_name,
        "messages": messages,
        "tools": tools,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    print(f"  LLM Query: {user_query}")
    print(f"  Model: {model_name}")
    print(f"  Endpoint: {llm_api_url}")
    
    try:
        response = requests.post(llm_api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            message = data["choices"][0]["message"]
            
            # Check if the LLM wants to use tools
            if "tool_calls" in message and message["tool_calls"]:
                print("\n  LLM is invoking tools...")
                messages.append(message)
                
                tool_results = []
                for tool_call in message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])
                    tool_id = tool_call.get("id", "")
                    
                    print(f"    - Calling {tool_name} with args: {tool_args}")
                    result = mcp_server.execute_tool(tool_name, tool_args)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": tool_name,
                        "content": json.dumps(result) if not isinstance(result, str) else result
                    })
                    tool_results.append((tool_name, result))
                
                # Get final response from LLM with tool results
                payload["messages"] = messages
                response = requests.post(llm_api_url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()
                message = data["choices"][0]["message"]
                
                final_response = message.get('content', 'No response')
                print(f"\n  LLM Final Response:\n    {final_response}\n")
                return final_response
            else:
                # Direct response without tool calls
                content = message.get("content", "No response from LLM")
                
                # Try to detect tool calls in the response text for models that don't support native tool_calls
                if _try_execute_tools_from_text(content, mcp_server, messages, payload, llm_api_url, headers):
                    # Tools were detected and executed, return the final response
                    return content
                
                print(f"\n  LLM Response:\n    {content}\n")
                return content
        else:
            print("  Error: Unexpected response format from LLM\n")
            return None
            
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP Error: {e.response.status_code} - {e.response.text}\n")
        return None
    except Exception as e:
        print(f"  Error: {e}\n")
        return None


def main():
    # Initialize library system
    library = LibrarySystem()
    
    # Add some sample data
    library.add_book("1984", "George Orwell", "978-0451524935")
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
    library.add_patron("John Doe", "john@example.com", "123-456-7890")
    
    # Initialize MCP server
    mcp_server = LibraryMCPServer(library)
    
    print("=== Library MCP Server Example ===\n")
    
    # Display available tools
    print("Available Tools:")
    for tool in mcp_server.get_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\n=== Executing Tool Examples ===\n")
    
    # Example 1: List books
    print("1. Listing all books:")
    result = mcp_server.execute_tool("list_books", {})
    print(f"   Result: {result}\n")
    
    # Example 2: Add a new patron
    print("2. Adding new patron:")
    result = mcp_server.execute_tool("add_patron", {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "098-765-4321"
    })
    print(f"   Result: {result}\n")
    
    # Example 3: Borrow a book
    print("3. Borrowing book (Book ID 1 for Patron ID 2):")
    result = mcp_server.execute_tool("borrow_book", {
        "book_id": 1,
        "patron_id": 2,
        "days": 14
    })
    print(f"   Result: {result}\n")
    
    # Example 4: Get patron info
    print("4. Getting patron info (Patron ID 2):")
    result = mcp_server.execute_tool("get_patron_info", {
        "patron_id": 2
    })
    print(f"   Result: {result}\n")
    
    # Example 5: Get book info
    print("5. Getting book info (Book ID 1):")
    result = mcp_server.execute_tool("get_book_info", {
        "book_id": 1
    })
    print(f"   Result: {result}\n")
    
    # Example 6: List patrons
    print("6. Listing all patrons:")
    result = mcp_server.execute_tool("list_patrons", {})
    print(f"   Result: {result}\n")
    
    # === LLM Integration Tests ===
    print("\n=== Testing LLM with MCP Tools ===\n")
    
    load_dotenv()
    llm_url = os.getenv("LLM_API_URL")
    llm_key = os.getenv("LLM_API_KEY", None)
    llm_model = os.getenv("LLM_MODEL_NAME", None)
    
    if llm_url:
        print("Test 1: Ask LLM about available books")
        response1 = call_llm_with_mcp_tools(
            mcp_server,
            "What books are available in the library?",
            llm_url,
            llm_key,
            llm_model
        )
        
        print("Test 2: Ask LLM to list patrons")
        response2 = call_llm_with_mcp_tools(
            mcp_server,
            "List all the patrons in our library system",
            llm_url,
            llm_key,
            llm_model
        )
        
        print("Test 3: Complex query - Check borrow status")
        response3 = call_llm_with_mcp_tools(
            mcp_server,
            "Can you tell me which books have been borrowed and by whom?",
            llm_url,
            llm_key,
            llm_model
        )
    else:
        print("LLM_API_URL not configured. Skipping LLM tests.")
        print("To test LLM integration, set the following environment variables:")
        print("  - LLM_API_URL (required)")
        print("  - LLM_API_KEY (optional, for some services)")
        print("  - LLM_MODEL_NAME (optional, auto-detected if not set)")
        print("\nExamples:")
        print("  LM Studio:   http://127.0.0.1:1234/v1/chat/completions")
        print("  OpenAI:      https://api.openai.com/v1/chat/completions")
        print("  NVIDIA:      https://integrate.api.nvidia.com/v1/chat/completions")


if __name__ == "__main__":
    main()
