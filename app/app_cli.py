import sys
import dotenv

from comvestinhochatbot import ComvestinhoChatBot

# Load OPENAI_API_KEY environment variable in .env file
dotenv.load_dotenv()

# Init and run conversational bot
comvestinho = ComvestinhoChatBot()

while True:
    query = input("[Prompt] ")
    if query.lower() == "sair":
        sys.exit()
    answer = comvestinho.ask(query)
    print(answer)