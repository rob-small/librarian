"""
example_mcp_usage.py
--------------------
Example script demonstrating direct usage of the LibraryMCPServer.
This can be used for testing or integration with other systems.
"""

from src.library import LibrarySystem
from src.mcp_server import LibraryMCPServer
import json


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


if __name__ == "__main__":
    main()
