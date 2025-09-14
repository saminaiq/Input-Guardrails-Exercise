# main.py
import openai
from config import OPENAI_API_KEY
from guardrails import validate_input

# OpenAI API key set کریں
openai.api_key = OPENAI_API_KEY

def generate_poem(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative poetry assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.8,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("🎭 Welcome to the Poetry Guardrails Project 🎭")
    while True:
        user_input = input("\nEnter a topic for your poem (or type 'exit'): ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        allowed, reasons, sanitized = validate_input(user_input)

        if not allowed:
            print("❌ Input rejected:", reasons)
            print("Sanitized preview:", sanitized)
            continue

        poem = generate_poem(sanitized)
        print("\n✨ Your AI-Generated Poem ✨\n")
        print(poem)

if __name__ == "__main__":
    main()
