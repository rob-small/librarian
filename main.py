"""
main.py
-------
Entry point for the Library Management System Gradio application.
Initializes and launches the web interface.
"""

from src.interface import create_interface

def main():
    """
    Create and launch the Gradio web interface for the library system.
    """
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()