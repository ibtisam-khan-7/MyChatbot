from chatbot import ChatBot
import sys

def start_app():
    # Initialize Lily
    lily = ChatBot(name="Lily")
    
    # Start conversation
    lily.greet()
    
    while lily.is_active:
        try:
            user_input = input("You: ")
            response = lily.process_input(user_input)
            print(f"{lily.name}: {response}")
            
        except KeyboardInterrupt:
            print("\nSystem shutting down.")
            sys.exit()

if __name__ == "__main__":
    start_app()