import sys
import dotenv

from app.core.comvestinhochatbot import ComvestinhoChatBot

# Load GROQ_API_KEY environment variable in .env file
dotenv.load_dotenv()

# Init and run conversational bot
comvestinho = ComvestinhoChatBot()
chat_history = []

while True:
    query = input("[Prompt] ")
    if query.lower() == "sair":
        sys.exit()
    answer = comvestinho.ask(query, chat_history)
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": answer})
    print(answer)