from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Chroma

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

# Constants for  prompt messages templates
SYSTEM_MESSAGE_TEMPLATE = "Considere a conversa, o contexto e a pergunta dada para dar uma resposta. Caso você não saiba uma resposta, fale 'Me desculpe, mas não tenho uma resposta para esta pergunta' em vez de tentar inventar algo.\n----\nConversa:\n{chat_history}\n----\nContexto:\n{context}\n----\n"
HUMAN_MESSAGE_TEMPLATE = "Pergunta:\n{question}"

# ComvestinhoChatBot Class
class ComvestinhoChatBot():
    # Inits ComvestinhoChatBot
    def __init__(self, chat_history=[]):
        # Sets model names
        self.chat_model_name = 'gpt-3.5-turbo'
        self.embeddings_model_name = 'text-embedding-ada-002'

        # Sets default values
        self.chunk_size = 750
        self.chunk_overlap = 10
        self.temperature = 0

        # Creates embeddings and chat models
        self.chat_model = ChatOpenAI(
            model_name=self.chat_model_name, 
            temperature=self.temperature,
        )
        self.embeddings_model = OpenAIEmbeddings(
            model=self.embeddings_model_name, 
            chunk_size=self.chunk_size,
        )

        # Sets chat history which is a list of tuples of strings as (human_question, ai_answer)
        self.chat_history = chat_history

        # Creates document vectostore and retriever
        doc_url = "https://www.pg.unicamp.br/norma/31594/0"
        docs = self.__load_webpage(doc_url)
        docs_splits = self.__split_documents(docs)
        self.vectordb = self.__create_doc_vectorstore(docs_splits)
        self.retriever = self.vectordb.as_retriever()
        
        # Defines prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE_TEMPLATE),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE_TEMPLATE),
        ])

    # Augments prompt adding chat history and context to question
    def __create_augmented_prompt(self, question):
        docs = self.retriever.get_relevant_documents(query=question)
        
        docs_formatted = '\n'.join([doc.page_content for doc in docs])
        chat_history_formatted = '\n'.join(self.chat_history)
        
        prompt = self.prompt_template.format_messages(
            input_language="Portuguese", 
            output_language="Portuguese", 
            question=question,
            context=docs_formatted,
            chat_history=chat_history_formatted
        )
        return prompt

    # Loads html page and convert it to text
    def __load_webpage(self, page_url):
        loader = AsyncHtmlLoader([page_url])
        html2text = Html2TextTransformer()
        docs = loader.load()
        docs_transformed = html2text.transform_documents(docs)
        return docs_transformed

    # Splits documents to smaller chunks
    def __split_documents(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        docs_splits = text_splitter.split_documents(docs)
        return docs_splits

    # Creates document vector store
    def __create_doc_vectorstore(self, docs):
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings_model,
            persist_directory='./vectorstore'
        )
        vectordb.persist()
        return vectordb

    # Asks the ComvestinhoChatBot a question, saves in chat history and returns the answer
    def ask(self, question):
        prompt = self.__create_augmented_prompt(question)
        answer = self.chat_model(prompt)
        self.chat_history.append(f"Usuário: {question}")
        self.chat_history.append(f"Sistema: {answer}")
        return answer.content