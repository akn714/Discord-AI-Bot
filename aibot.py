#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Adarsh Kumar (https://github.com/adarshkumar714)

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from langchain.chains import ChatVectorDBChain

from langchain.chains import LLMChain

from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationChain
from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory

GENIEPROMPT = "You are an Ecommerce expert/mentor. Your users are beginners in this field. You provide accurate and descriptive answers to user questions in under 2000 characters, after researching through the vector DB. Provide additional descriptions of any complex terms being used in the response \n\nUser: {question}\n\nAi: "

# environment variables
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv(
  "OPENAI_API_KEY")  # repl.it asks for this useless line
os.environ['PINECONE_API_KEY'] = os.getenv(
  "PINECONE_API_KEY")  # repl.it asks for this useless line
os.environ['PINECONE_ENV'] = os.getenv(
  "PINECONE_ENV")  # repl.it asks for this useless line
os.environ['PINECONE_INDEX_NAME'] = os.getenv(
  "PINECONE_INDEX_NAME")  # repl.it asks for this useless line

# # NOTE: commented this code, as we want to use existing pinecone index
# loading documents
# documents = []
# url = "https://www.ideou.com/blogs/inspiration/what-is-design-thinking"
# print(f"[+] loading data from URL:{url}")
# loader = WebBaseLoader(url)
# doc = loader.load()
# documents.extend(doc)
# print("[+] URL loaded")

# splitting into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
# documents = text_splitter.split_documents(documents)
"""
for storing chat histories for individual chats:

key -> unique chat id
value -> chat history for that chat
"""
history = dict()


# chat history
def chat_history(key):
  global history
  try:
    return history[key]
  except:
    history[key] = ConversationBufferMemory()
    return history[key]


# embeddings
embeddings = OpenAIEmbeddings()

# initializing pinecone db
print('[+] Initializing pinecone db...')
pinecone.init(
  api_key=os.getenv('PINECONE_API_KEY'),
  environment=os.getenv('PINECONE_ENV'),
)

index_name = os.getenv('PINECONE_INDEX_NAME')
index = pinecone.Index(index_name)
index.describe_index_stats()

print("[+] Index Stats: ")
print(index.describe_index_stats())
# docsearch = Pinecone.from_documents(documents,
#                                     embedding=embeddings,
#                                     index_name=index_name)

print('[+] Creating vector store')

text_field = "text"

# switch back to normal index for langchain
index = pinecone.Index(index_name)

# embed will be created by client
vectorstore = Pinecone(index, embeddings.embed_query, text_field)

# docsearch
docsearch = Pinecone.from_existing_index(index_name, embeddings)

# prompt template
# prompt_template = """reply me as an AI bot:
# {text}
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# completion llm
llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'),
                 model_name='gpt-3.5-turbo',
                 temperature=0.3)

# chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     # prompt=prompt,
#     retriever=vectorstore.as_retriever())
# chain = load_qa_chain(llm, chain_type="map_reduce", verbose=True)
# chain = ConversationalRetrievalChain.from_llm(
#   llm=llm, chain_type="map_reduce", retriever=vectorstore.as_retriever())

chain = ConversationChain(llm=llm,
                          verbose=False,
                          memory=ConversationBufferMemory())

# chain = LLMChain(llm=llm, prompt=prompt_template)


def get_response(query, chat_history):
  # result = chain({"query": query, "chat_history": chat_history})
  # result = chain.get_relevant_documents(query)                     # new line
  docs = docsearch.similarity_search(query)  # new line
  # result = chain({"question": query, "chat_history": chat_history})

  result = chain.run({
    "input": query,
  })

  chat_history.save_context({"input": query}, {"output": result})
  return result, chat_history


if __name__ == "__main__":
  print("START THE CHAT:\n")
  chat_hist = ConversationBufferMemory()
  while True:
    query = input("[You]: ")
    response, chat_hist = get_response(query, chat_hist)
    # print(response["answer"])
    # print(response['output_text'])
    print(response)
