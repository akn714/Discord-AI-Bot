#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Adarsh Kumar (https://github.com/adarshkumar714)

from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain import PromptTemplate
# from langchain.chains import RetrievalQA
# from langchain.chains import ConversationalRetrievalChain
# from langchain.chains import LLMChain
# from langchain.chains.question_answering import load_qa_chain
# from langchain.memory import ConversationBufferMemory

GENIEPROMPT = "You are an Ecommerce expert/mentor. Your users are beginners in this field. You provide accurate and descriptive answers to user questions in under 2000 characters, after researching through the vector DB. Provide additional descriptions of any complex terms being used in the response \n\nUser: {question}\n\nAi: "

# prompt template
prompt_template = PromptTemplate(input_variables=['question'],
                                 template=GENIEPROMPT)

# environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# repl.it asks for these useless line
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")
os.environ['PINECONE_ENV'] = os.getenv("PINECONE_ENV")
os.environ['PINECONE_INDEX_NAME'] = os.getenv("PINECONE_INDEX_NAME")

#
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
                          prompt=prompt_template,
                          verbose=False,
                          memory=ConversationBufferMemory())

# chain = LLMChain(llm=llm, prompt=prompt_template)


def get_response(query, chat_history):

    # fetching docs from pinecone db
    print('[+] fetching docs from pinecone_db...')
    docs = docsearch.similarity_search(query)
    print(f'[+] {len(docs)} docs fetched.')

    # using different method of getting result
    # result = chain({"query": query, "chat_history": chat_history})
    # result = chain.get_relevant_documents(query)
    # result = chain({"question": query, "chat_history": chat_history})

    # converting list to dictionary
    # docs_dict = {docs[i]: docs[i + 1] for i in range(0, len(docs), 2)}

    result = chain.run({"input": query})

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
