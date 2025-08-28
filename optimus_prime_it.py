
import os
import sys
from xai_sdk import Client
from xai_sdk.chat import user, system, assistant  # Assuming 'assistant' is available; if not, use the appropriate method to add assistant messages

# ANSI color codes for colorful output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

client = Client(
    api_key=os.getenv("XAI_API_KEY"),
    timeout=3600,  # Override default timeout with longer timeout for reasoning models
)

chat = client.chat.create(model="grok-code-fast-1")

# Initial system prompt
chat.append(system("You are Grok, a highly intelligent, helpful AI assistant specialized in fast, efficient coding. When optimizing code, always check for bugs, improve efficiency, and expand with detailed comments, error handling, and modular structure to reach at least 1000 lines if possible while keeping it functional."))

clear_screen()
print(f"{Colors.HEADER}{Colors.BOLD}Welcome to Continuous Chat with grok-code-fast-1!{Colors.ENDC}")
print(f"{Colors.OKCYAN}Type 'exit' to quit. For help, type 'help'.{Colors.ENDC}\n")

while True:
    user_input = input(f"{Colors.OKGREEN}You: {Colors.ENDC}")
    actual_message = user_input  # Default to user input
    
    if user_input.lower() == 'exit':
        clear_screen()
        print(f"{Colors.WARNING}{Colors.BOLD}Exiting chat. Goodbye!{Colors.ENDC}")
        sys.exit(0)
    elif user_input.lower() == 'help':
        clear_screen()
        print(f"{Colors.OKBLUE}{Colors.BOLD}Help Menu:{Colors.ENDC}")
        print("- Type your message to chat with Grok.")
        print("- Type 'read filename.txt' to load and send the content of a file as your message.")
        print("- Type 'optimus prime it: filename.txt' to read the file, then optimize its code 10 times iteratively (with bug checks and expansion to at least 1000 lines).")
        print("- Use 'exit' to quit.")
        print("- This chat is powered by grok-code-fast-1 for fast coding tasks.\n")
        continue
    elif user_input.lower().startswith('read '):
        filename = user_input[5:].strip()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                actual_message = f.read().strip()
        except FileNotFoundError:
            clear_screen()
            print(f"{Colors.FAIL}File '{filename}' not found.{Colors.ENDC}\n")
            continue
        except Exception as e:
            clear_screen()
            print(f"{Colors.FAIL}Error reading file: {str(e)}{Colors.ENDC}\n")
            continue
    elif user_input.lower().startswith('optimus prime it: '):
        filename = user_input[18:].strip()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                current_code = f.read().strip()
        except FileNotFoundError:
            clear_screen()
            print(f"{Colors.FAIL}File '{filename}' not found.{Colors.ENDC}\n")
            continue
        except Exception as e:
            clear_screen()
            print(f"{Colors.FAIL}Error reading file: {str(e)}{Colors.ENDC}\n")
            continue
        
        clear_screen()
        print(f"{Colors.OKCYAN}Starting Optimus Prime optimization on '{filename}' (10 iterations)...{Colors.ENDC}\n")
        
        for iteration in range(1, 11):
            prompt = f"Optimize this code fully: check for bugs, improve efficiency, add detailed comments, error handling, and modularize/expand as needed to reach at least 1000 lines while keeping it functional. Provide only the complete optimized code in your response:\n\n{current_code}"
            
            chat.append(user(prompt))
            
            try:
                response = chat.sample()
                current_code = response.content.strip()  # Assume response is the optimized code
            except Exception as e:
                clear_screen()
                print(f"{Colors.FAIL}Error during optimization iteration {iteration}: {str(e)}{Colors.ENDC}\n")
                break
            
            chat.append(assistant(current_code))
            
            clear_screen()
            print(f"{Colors.OKCYAN}Optimus Prime Iteration {iteration}/10 complete.{Colors.ENDC}\n")
        
        clear_screen()
        print(f"{Colors.OKGREEN}Final Optimized Code after 10 iterations:{Colors.ENDC}\n{current_code}\n")
        continue
    
    chat.append(user(actual_message))
    
    try:
        response = chat.sample()
        grok_response = response.content
    except Exception as e:
        grok_response = f"Error: {str(e)}"
    
    clear_screen()  # Auto-clear screen before showing response for neatness
    print(f"{Colors.OKGREEN}You: {Colors.ENDC}{actual_message}\n")
    print(f"{Colors.OKBLUE}Grok: {Colors.ENDC}{grok_response}\n")
    
    # Append the assistant's response to maintain conversation history
    chat.append(assistant(grok_response))  # If 'assistant' is not directly imported, adjust based on SDK docs (e.g., use chat.append({"role": "assistant", "content": grok_response}))
