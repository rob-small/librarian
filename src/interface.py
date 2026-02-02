"""
interface.py
-------------
This module defines the Gradio-based user interface for the Library Management System.
It provides interactive tabs for adding books and patrons, borrowing and returning books,
and viewing the library status, all backed by the LibrarySystem class.
"""

import gradio as gr
from datetime import datetime
from typing import Tuple
from .library import LibrarySystem


class LibraryInterface:
    """
    Provides high-level methods for interacting with the LibrarySystem.
    Used by the Gradio interface to manage books, patrons, loans, and status queries.
    """
    def __init__(self):
        """
        Initialize the LibraryInterface and add sample data for demonstration.
        """
        self.library = LibrarySystem()
        self._add_sample_data()


    def _add_sample_data(self):
        """
        Add sample books and patrons to the library for demonstration purposes.
        """
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
        self.library.add_book("To Kill a Mockingbird", "Harper Lee", "978-0446310789")
        self.library.add_book("1984", "George Orwell", "978-0451524935")
        self.library.add_patron("John Doe", "john@example.com", "123-456-7890")
        self.library.add_patron("Jane Smith", "jane@example.com", "098-765-4321")


    def add_book(self, title: str, author: str, isbn: str) -> str:
        """
        Add a new book to the library.
        Returns a success message or prompts for missing fields.
        """
        if not all([title, author, isbn]):
            return "Please fill in all fields"
        book = self.library.add_book(title, author, isbn)
        return f"Book added successfully! Book ID: {book.id}"


    def add_patron(self, name: str, email: str, phone: str) -> str:
        """
        Add a new patron to the library.
        Returns a success message or prompts for missing fields.
        """
        if not all([name, email, phone]):
            return "Please fill in all fields"
        patron = self.library.add_patron(name, email, phone)
        return f"Patron added successfully! Patron ID: {patron.id}"


    def borrow_book(self, book_id: str, patron_id: str, loan_days: int) -> str:
        """
        Borrow a book for a patron for a specified number of days.
        Returns a success message with due date or an error message.
        """
        try:
            book_id = int(book_id)
            patron_id = int(patron_id)
        except ValueError:
            return "Please enter valid numeric IDs"
        loan = self.library.borrow_book(book_id, patron_id, loan_days)
        if loan:
            return f"Book borrowed successfully! Due date: {loan.due_date.strftime('%Y-%m-%d')}"
        return "Failed to borrow book. Check if book/patron exists and book is available"


    def return_book(self, book_id: str) -> str:
        """
        Return a borrowed book to the library.
        Returns a success message or an error message.
        """
        try:
            book_id = int(book_id)
        except ValueError:
            return "Please enter a valid numeric book ID"
        success = self.library.return_book(book_id)
        if success:
            return "Book returned successfully!"
        return "Failed to return book. Check if book exists and is borrowed"


    def list_books(self) -> str:
        """
        List all books in the library with their status.
        Returns a formatted string of book details.
        """
        if not self.library.books:
            return "No books in the library"
        book_list = []
        for book in self.library.books:
            status = "Available" if book.available else f"Borrowed by Patron #{book.borrowed_by}"
            book_list.append(
                f"ID: {book.id} | {book.title} by {book.author} | ISBN: {book.isbn} | {status}"
            )
        return "\n".join(book_list)


    def list_patrons(self) -> str:
        """
        List all registered patrons in the library.
        Returns a formatted string of patron details.
        """
        if not self.library.patrons:
            return "No patrons registered"
        patron_list = []
        for patron in self.library.patrons:
            patron_list.append(
                f"ID: {patron.id} | {patron.name} | Email: {patron.email} | Phone: {patron.phone}"
            )
        return "\n".join(patron_list)


    def list_overdue(self) -> str:
        """
        List all overdue loans in the library.
        Returns a formatted string of overdue book and patron details.
        """
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


def create_interface(llm_api_url=None, llm_api_key=None, llm_model_name=None):
    """
    Build and return the Gradio Blocks interface for the Library Management System.
    Provides tabs for all major library operations.
    
    Args:
        llm_api_url: URL endpoint for the LLM API (required).
                     Set via LLM_API_URL environment variable.
        llm_api_key: API key for authentication with the LLM service (optional).
                     Used for services like OpenAI, Anthropic, or other hosted LLM providers.
        llm_model_name: Model name to use with the LLM service (optional).
                        If not provided, auto-detects based on API URL.
    """
    interface = LibraryInterface()
    import requests
    from .mcp_server import LibraryMCPServer
    
    # Initialize MCP server for library tools
    mcp_server = LibraryMCPServer(interface.library)

    def chat_with_llm(messages, api_url=llm_api_url, api_key=llm_api_key):
        """
        Send a chat request to an LLM using OpenAI API format.
        Supports both local LLMs (LM Studio) and hosted services (OpenAI, NVIDIA, etc.).
        
        Args:
            messages: List of dicts with 'role' and 'content'.
            api_url: Endpoint for the LLM API (must be OpenAI-compatible format).
            api_key: Optional API key for authentication.
        
        Returns:
            The assistant's reply as a string.
        """
        import json
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Determine the model name: use provided parameter, or default based on API endpoint
        if llm_model_name:
            model_name = llm_model_name
        elif "openai.com" in api_url:
            model_name = "gpt-3.5-turbo"
        else:
            model_name = "local-model"
        
        # Define available tools for the LLM
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
                    "name": "add_patron",
                    "description": "Add a new patron to the library",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"}
                        },
                        "required": ["name", "email", "phone"]
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
                    "name": "return_book",
                    "description": "Return a borrowed book",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "book_id": {"type": "integer"}
                        },
                        "required": ["book_id"]
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
        
        # Build payload
        payload = {
            "model": model_name,
            "messages": messages,
            "tools": tools,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 1024
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Extract the assistant's response
            if "choices" in data and len(data["choices"]) > 0:
                message = data["choices"][0]["message"]
                
                # Check if there are tool calls to execute
                if "tool_calls" in message and message["tool_calls"]:
                    # Add assistant's message to conversation
                    messages.append(message)
                    
                    # Execute each tool call
                    for tool_call in message["tool_calls"]:
                        tool_name = tool_call["function"]["name"]
                        tool_args = json.loads(tool_call["function"]["arguments"])
                        tool_id = tool_call.get("id", "")
                        
                        # Execute the tool
                        result = mcp_server.execute_tool(tool_name, tool_args)
                        
                        # Add tool result to messages in OpenAI format
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_id,
                            "name": tool_name,
                            "content": json.dumps(result) if not isinstance(result, str) else result
                        })
                    
                    # Get final response from LLM with tool results
                    payload_with_results = {
                        "model": model_name,
                        "messages": messages,
                        "tools": tools,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 1024
                    }
                    response = requests.post(api_url, json=payload_with_results, headers=headers, timeout=30)
                    response.raise_for_status()
                    data = response.json()
                    message = data["choices"][0]["message"]
                
                return message.get("content", "No response from LLM")
            else:
                return "Error: Unexpected response format from LLM"
            
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {e}"

    with gr.Blocks(title="Library Management System") as demo:
        gr.Markdown("# Library Management System")

        with gr.Tab("Add Book"):
            with gr.Row():
                title = gr.Textbox(label="Title")
                author = gr.Textbox(label="Author")
                isbn = gr.Textbox(label="ISBN")
            add_book_btn = gr.Button("Add Book")
            add_book_output = gr.Textbox(label="Result")
            add_book_btn.click(
                fn=interface.add_book,
                inputs=[title, author, isbn],
                outputs=add_book_output
            )

        with gr.Tab("Add Patron"):
            with gr.Row():
                name = gr.Textbox(label="Name")
                email = gr.Textbox(label="Email")
                phone = gr.Textbox(label="Phone")
            add_patron_btn = gr.Button("Add Patron")
            add_patron_output = gr.Textbox(label="Result")
            add_patron_btn.click(
                fn=interface.add_patron,
                inputs=[name, email, phone],
                outputs=add_patron_output
            )

        with gr.Tab("Borrow Book"):
            with gr.Row():
                book_id = gr.Textbox(label="Book ID")
                patron_id = gr.Textbox(label="Patron ID")
                loan_days = gr.Slider(minimum=1, maximum=30, value=14, label="Loan Days")
            borrow_btn = gr.Button("Borrow Book")
            borrow_output = gr.Textbox(label="Result")
            borrow_btn.click(
                fn=interface.borrow_book,
                inputs=[book_id, patron_id, loan_days],
                outputs=borrow_output
            )

        with gr.Tab("Return Book"):
            return_book_id = gr.Textbox(label="Book ID")
            return_btn = gr.Button("Return Book")
            return_output = gr.Textbox(label="Result")
            return_btn.click(
                fn=interface.return_book,
                inputs=return_book_id,
                outputs=return_output
            )

        with gr.Tab("View Library Status"):
            with gr.Row():
                list_books_btn = gr.Button("List Books")
                list_patrons_btn = gr.Button("List Patrons")
                list_overdue_btn = gr.Button("List Overdue")
            status_output = gr.Textbox(label="Library Status", lines=10)

            list_books_btn.click(fn=interface.list_books, outputs=status_output)
            list_patrons_btn.click(fn=interface.list_patrons, outputs=status_output)
            list_overdue_btn.click(fn=interface.list_overdue, outputs=status_output)

        # New Chat with LLM Tab
        with gr.Tab("Chat with LLM"):
            chatbot = gr.Chatbot(label="LLM Chat")
            user_msg = gr.Textbox(label="Your message", lines=2)
            send_btn = gr.Button("Send")

            def gradio_chat(history, user_input):
                if not user_input.strip():
                    return history, ""
                
                messages = []
                # Convert chat history to message format
                if history:
                    for msg in history:
                        if isinstance(msg, dict):
                            # Already in message format
                            messages.append(msg)
                        else:
                            # Legacy tuple format (user_text, assistant_text)
                            messages.append({"role": "user", "content": msg[0]})
                
                # Add new user message
                messages.append({"role": "user", "content": user_input})
                
                # Get response from LLM
                reply = chat_with_llm(messages)
                
                # Add to history in new message format
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": reply})
                
                return history, ""

            send_btn.click(
                fn=gradio_chat,
                inputs=[chatbot, user_msg],
                outputs=[chatbot, user_msg]
            )
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch()