import dotenv

from core.comvestinhochatbot import ComvestinhoChatBot

# Load OPENAI_API_KEY environment variable in .env file
dotenv.load_dotenv()

# Init and run conversational bot
comvestinho = ComvestinhoChatBot()

idx = 1
fq = open("./data/questions.txt", "r")
fw = open("./data/answers.txt", "a")

for question in fq:
    answer = comvestinho.ask(question, [])
    out = f"--------\nQuestion {idx}:\n--------\n{question}--------\nAnswer {idx}:\n--------\n{answer}\n--------\n"
    print(out)
    fw.write(out)
    idx += 1

fw.close()
fq.close()