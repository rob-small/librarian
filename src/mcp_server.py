"""
mcp_server.py
-------------
Model Context Protocol (MCP) server for the Library Management System.
Allows LLMs to interact with the library system through standard MCP tools.
"""

import json
from typing import Any, Dict, List
from .library import LibrarySystem


class LibraryMCPServer:
    """
    Simple MCP-compatible server that exposes library operations as tools for LLM use.
    Allows an LLM to add books, manage patrons, handle loans, and query status.
    """
    
    def __init__(self, library_system: LibrarySystem):
        """
        Initialize the MCP server with a LibrarySystem instance.
        
        Args:
            library_system: The LibrarySystem instance to manage.
        """
        self.library = library_system
        self.tools = self._define_tools()
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """
        Define all available library tools in MCP format.
        Returns a list of tool definitions.
        """
        return [
            {
                "name": "add_book",
                "description": "Add a new book to the library",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Book title"},
                        "author": {"type": "string", "description": "Author name"},
                        "isbn": {"type": "string", "description": "ISBN number"}
                    },
                    "required": ["title", "author", "isbn"]
                }
            },
            {
                "name": "add_patron",
                "description": "Add a new patron to the library",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Patron name"},
                        "email": {"type": "string", "description": "Email address"},
                        "phone": {"type": "string", "description": "Phone number"}
                    },
                    "required": ["name", "email", "phone"]
                }
            },
            {
                "name": "borrow_book",
                "description": "Borrow a book for a patron",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer", "description": "ID of the book to borrow"},
                        "patron_id": {"type": "integer", "description": "ID of the patron borrowing"},
                        "days": {"type": "integer", "description": "Number of days for the loan", "default": 14}
                    },
                    "required": ["book_id", "patron_id"]
                }
            },
            {
                "name": "return_book",
                "description": "Return a borrowed book to the library",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer", "description": "ID of the book to return"}
                    },
                    "required": ["book_id"]
                }
            },
            {
                "name": "list_books",
                "description": "List all books in the library with their status",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "list_patrons",
                "description": "List all patrons registered in the library",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_overdue_loans",
                "description": "Get all overdue loans in the library",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_book_info",
                "description": "Get detailed information about a specific book",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer", "description": "ID of the book"}
                    },
                    "required": ["book_id"]
                }
            },
            {
                "name": "get_patron_info",
                "description": "Get detailed information about a specific patron",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "patron_id": {"type": "integer", "description": "ID of the patron"}
                    },
                    "required": ["patron_id"]
                }
            }
        ]
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get all available tools in MCP format."""
        return self.tools
    
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a library tool based on the tool name and input parameters.
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Dictionary of input parameters
        
        Returns:
            Result of the tool execution as a string
        """
        try:
            # Handle tool name aliases
            tool_aliases = {
                "get_all_books": "list_books",
                "get_all_patrons": "list_patrons",
                "get_books": "list_books",
                "get_patrons": "list_patrons",
            }
            
            # Map aliases to actual tool names
            actual_tool_name = tool_aliases.get(tool_name, tool_name)
            
            if actual_tool_name == "add_book":
                book = self.library.add_book(
                    tool_input["title"],
                    tool_input["author"],
                    tool_input["isbn"]
                )
                return f"Book added successfully! ID: {book.id}, Title: {book.title}"
            
            elif actual_tool_name == "add_patron":
                patron = self.library.add_patron(
                    tool_input["name"],
                    tool_input["email"],
                    tool_input["phone"]
                )
                return f"Patron added successfully! ID: {patron.id}, Name: {patron.name}"
            
            elif actual_tool_name == "borrow_book":
                days = tool_input.get("days", 14)
                loan = self.library.borrow_book(
                    tool_input["book_id"],
                    tool_input["patron_id"],
                    days
                )
                if loan:
                    return f"Book borrowed successfully! Due date: {loan.due_date.strftime('%Y-%m-%d')}"
                return "Failed to borrow book. Check if book/patron exists and book is available."
            
            elif actual_tool_name == "return_book":
                success = self.library.return_book(tool_input["book_id"])
                if success:
                    return "Book returned successfully!"
                return "Failed to return book. Check if book exists and is borrowed."
            
            elif actual_tool_name == "list_books":
                if not self.library.books:
                    return "No books in the library"
                book_list = []
                for book in self.library.books:
                    status = "Available" if book.available else f"Borrowed by Patron #{book.borrowed_by}"
                    book_list.append(
                        f"ID: {book.id} | {book.title} by {book.author} | ISBN: {book.isbn} | {status}"
                    )
                return "\n".join(book_list)
            
            elif actual_tool_name == "list_patrons":
                if not self.library.patrons:
                    return "No patrons registered"
                patron_list = []
                for patron in self.library.patrons:
                    patron_list.append(
                        f"ID: {patron.id} | {patron.name} | Email: {patron.email} | Phone: {patron.phone}"
                    )
                return "\n".join(patron_list)
            
            elif actual_tool_name == "get_overdue_loans":
                overdue = self.library.get_overdue_loans()
                if not overdue:
                    return "No overdue books"
                overdue_list = []
                for loan in overdue:
                    book = next(b for b in self.library.books if b.id == loan.book_id)
                    patron = next(p for p in self.library.patrons if p.id == loan.patron_id)
                    overdue_list.append(
                        f"Book: {book.title} (ID: {book.id}) | "
                        f"Patron: {patron.name} (ID: {patron.id}) | "
                        f"Due date: {loan.due_date.strftime('%Y-%m-%d')}"
                    )
                return "\n".join(overdue_list)
            
            elif actual_tool_name == "get_book_info":
                book = next((b for b in self.library.books if b.id == tool_input["book_id"]), None)
                if not book:
                    return f"Book with ID {tool_input['book_id']} not found"
                status = "Available" if book.available else f"Borrowed by Patron #{book.borrowed_by}"
                return f"ID: {book.id} | Title: {book.title} | Author: {book.author} | ISBN: {book.isbn} | Status: {status}"
            
            elif actual_tool_name == "get_patron_info":
                patron = next((p for p in self.library.patrons if p.id == tool_input["patron_id"]), None)
                if not patron:
                    return f"Patron with ID {tool_input['patron_id']} not found"
                loans = self.library.get_patron_loans(tool_input["patron_id"])
                active_loans = len([l for l in loans if l.return_date is None])
                return f"ID: {patron.id} | Name: {patron.name} | Email: {patron.email} | Phone: {patron.phone} | Active Loans: {active_loans}"
            
            else:
                return f"Unknown tool: {actual_tool_name}"
        
        except Exception as e:
            return f"Error executing {actual_tool_name}: {str(e)}"

