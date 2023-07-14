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
from langchain.prompts import PromptTemplate

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

documents = []
# url = "https://www.ideou.com/blogs/inspiration/what-is-design-thinking"

# loading documents
# print(f"[+] loading data from URL:{url}")
# loader = WebBaseLoader(url)
# doc = loader.load()
# documents.extend(doc)
# print("[+] URL loaded")

# splitting into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
# documents = text_splitter.split_documents(documents)

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
prompt_template = """reply me as an AI bot:
                     {text}
                  """
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# completion llm
llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'),
                model_name='gpt-3.5-turbo',
                temperature=0.0)
chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    # prompt=prompt,
                                    retriever=vectorstore.as_retriever())



def get_response(query, chat_history=[]):
    # result = chain({"query": query, "chat_history": chat_history})
    # result = chain.get_relevant_documents(query)                            # new line
    result = docsearch.similarity_search(query)                               # new line
    chat_history.append((query, result))

    return result, chat_history


if __name__ == "__main__":
  print("START THE CHAT:\n")
  while True:
    query = input("[You]: ")
    response, chat_history = get_response(query, [])
    # print(response["answer"])
    print(response[0].page_content)
