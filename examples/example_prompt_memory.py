# prompt_memory_example.py

# Configure Logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format = '%(name)s - %(levelname)s - %(message)s (line: %(lineno)d)',
    handlers=[
        logging.StreamHandler(),  # Log to console
        # logging.FileHandler('app.log')  # Log to file
    ]
)

from WrapAI import VeniceChatPrompt  # adjust import as needed
from secret_loader import load_secret


def print_message_chain(messages):
    print("\n🔗 Conversation History:")
    for i, msg in enumerate(messages):
        role = msg["role"].capitalize()
        content = msg["content"].strip()
        print(f"\n{i+1}. {role}:\n{'-' * 10}\n{content}\n")


def main():
    api_key = load_secret("VENICE_API_KEY")

    # model = "mistral-31-24b"
    model = "llama-3.1-405b"

    # Initialize the chat prompt with the Venice model
    chat = VeniceChatPrompt(api_key, model)

    # Set any additional parameters if needed
    chat.set_attributes(
        temperature=0.7,
        venice_parameters={
            "enable_web_search": "off"  # Disable web search for this example
        }
    )

    # First question
    q1 = "What's the capital of France?"
    print(f"🟦 Asking: {q1}")
    chat.prompt(q1)
    print(f"🟩 Response: {chat.get_response()}")

    # Follow-up question
    q2 = "What's one famous museum there?"
    print(f"\n🟦 Asking: {q2}")
    chat.prompt(q2)
    print(f"🟩 Response: {chat.get_response()}")

    # Follow-up question
    q3 = "What's year was the museum built?"
    print(f"\n🟦 Asking: {q3}")
    chat.prompt(q3)
    print(f"🟩 Response: {chat.get_response()}")

    # Show total tokens used
    print(f"\n🧠 Total tokens used: {chat.memory.token_count} / {chat.memory.max_tokens}")

    # Summarize (default and custom)
    summary_default = chat.summarize_memory()
    print(f"\n🧾 Summary (default prompt):\n{summary_default}")

    summary_custom = chat.summarize_memory("Summarize in a concise paragraph.")
    print(f"\n🧾 Summary (custom prompt):\n{summary_custom}")

    # Trim if needed
    print(f"Before trim: {chat.memory.token_count}")
    chat.trim_and_summarize_if_needed()
    print(f"After trim: {chat.memory.token_count}")

    # Show memory again after potential reset
    print("\n🔄 Memory After Summary/Trim:")
    print_message_chain(chat.memory.message_history)


if __name__ == "__main__":
    main()

