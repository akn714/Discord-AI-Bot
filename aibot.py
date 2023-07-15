#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Adarsh Kumar (https://github.com/adarshkumar714)

from conversations import history, chat_history

from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain import PromptTemplate

# environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# repl.it asks for these useless lines
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")
os.environ['PINECONE_ENV'] = os.getenv("PINECONE_ENV")
os.environ['PINECONE_INDEX_NAME'] = os.getenv("PINECONE_INDEX_NAME")

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
print('[+] Creating vector store')
# switch back to normal index for langchain
index = pinecone.Index(index_name)
# embed will be created by client
vectorstore = Pinecone(index, embeddings.embed_query, "text")

# docsearch
docsearch = Pinecone.from_existing_index(index_name, embeddings)

# completion llm
llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'),
                 model_name='gpt-3.5-turbo',
                 temperature=0.3)

# custom prompt
GENIEPROMPT = "You are an Ecommerce expert/mentor. Your users are beginners in this field. You provide accurate and descriptive answers to user questions in under 2000 characters, after researching through the vector DB. Provide additional descriptions of any complex terms being used in the response \n\nUser: {question}\n\nAi: "

# prompt template
prompt_template = PromptTemplate(template=GENIEPROMPT,
                                 input_variables=["question"])

# chain
chain = ConversationChain(llm=llm,
                          prompt=prompt_template,
                          verbose=False,
                          memory=ConversationBufferMemory())


def get_response(query, chat_hist):
    # fetching docs from pinecone db
    print('[+] fetching docs from pinecone_db...')
    docs = docsearch.similarity_search(query)
    print(f'[+] {len(docs)} docs fetched.')
    result = chain.run({"input": query})

    chat_hist.save_context({"input": query}, {"output": result})
    return result, chat_hist


if __name__ == "__main__":
    print("START THE CHAT:\n")
    chat_hist = ConversationBufferMemory()
    while True:
        query = input("[You]: ")
        response, chat_hist = get_response(query, chat_hist)
        print(response)
