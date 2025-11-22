"""
main.py
-------
Entry point for the Library Management System Gradio application.
Initializes and launches the web interface.
"""

import os
from src.interface import create_interface

def main():
    """
    Create and launch the Gradio web interface for the library system.
    
    Environment Variables:
        LLM_API_URL: URL for the LLM API endpoint 
                     (default: http://host.docker.internal:1234/v1/chat/completions)
        LLM_API_KEY: Optional API key for authenticating with the LLM service
                     (not required for local LLMs like LM Studio, required for OpenAI/Anthropic)
        LLM_MODEL_NAME: Model name to use with the LLM service
                        (default: local-model for local services, gpt-3.5-turbo for OpenAI)
    """
    llm_url = os.getenv("LLM_API_URL", "http://host.docker.internal:1234/v1/chat/completions")
    llm_key = os.getenv("LLM_API_KEY", None)
    llm_model = os.getenv("LLM_MODEL_NAME", None)
    demo = create_interface(llm_api_url=llm_url, llm_api_key=llm_key, llm_model_name=llm_model)
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()