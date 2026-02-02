"""
main.py
-------
Entry point for the Library Management System Gradio application.
Initializes and launches the web interface.
"""

import os
from src.interface import create_interface
from dotenv import load_dotenv

def main():
    """
    Create and launch the Gradio web interface for the library system.
    
    Environment Variables:
        LLM_API_URL: URL for the LLM API endpoint (REQUIRED)
                     Examples: https://integrate.api.nvidia.com/v1/chat/completions
                              http://127.0.0.1:1234/v1/chat/completions (LM Studio)
                              https://api.openai.com/v1/chat/completions
        LLM_API_KEY: Optional API key for authenticating with the LLM service
                     Required for OpenAI, Anthropic, and NVIDIA APIs
                     Not required for local LLMs like LM Studio
        LLM_MODEL_NAME: Model name to use with the LLM service (Optional)
                        If not set, auto-detected based on API URL
                        Examples: meta/llama-3.1-70b-instruct, gpt-3.5-turbo, local-model
    """
    load_dotenv()
    
    llm_url = os.getenv("LLM_API_URL")
    llm_key = os.getenv("LLM_API_KEY", None)
    llm_model = os.getenv("LLM_MODEL_NAME", None)
    
    if not llm_url:
        raise ValueError("LLM_API_URL environment variable must be set. Check your .env file.")
    
    if not llm_key:
        print("Warning: LLM_API_KEY not set. This may be required for some LLM services.")
    
    if not llm_model:
        print("Info: LLM_MODEL_NAME not set. Using auto-detection based on API URL.")
    else:
        print(f"Using LLM model: {llm_model}")
    
    print(f"Connecting to LLM API: {llm_url}")
    if llm_model:
        print(f"Using model: {llm_model}")
    
    demo = create_interface(llm_api_url=llm_url, llm_api_key=llm_key, llm_model_name=llm_model)
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()