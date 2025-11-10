from src.interface import create_interface

def main():
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()