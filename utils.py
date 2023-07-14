import pinecone

import os
#
#
#
#
#
#
#
"""
Loading the document
"""
# from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import UnstructuredURLLoader

documents = []
urls = [
    "https://www.google.com/search?q=how+to+create+a+requirements.txt+in+python&oq=how+to+create+a+requirements.txt+in+python&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyCAgCEAAYFhgeMggIAxAAGBYYHjIKCAQQABiGAxiKBTIKCAUQABiGAxiKBTIKCAYQABiGAxiKBTIKCAcQABiGAxiKBdIBCDgzODNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8"
]
loader = UnstructuredURLLoader(urls=urls)
data = loader.load()
documents.extend(data)
print("[+] loading data from url")

# pdf_path = './test-data.txt'
# doc = PyMuPDFLoader(pdf_path).load()
# documents.extend(doc)
print("[+] loaded from url")
#
#
#
#
#
#
#
"""
embedding
"""
from langchain.embeddings.openai import OpenAIEmbeddings

model_name = 'gpt-3.5-turbo'
print(f'[+] using model {model_name}')
print('[+] Embedding the docs...')
embeddings = OpenAIEmbeddings(model=model_name,
                              openai_api_key=os.getenv('OPENAI_API_KEY'))
#
#
#
#
#
#
#
"""
splitting the doc
"""
print('[+] Splitting the docs...')
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=512,
                                               chunk_overlap=10)
documents = text_splitter.split_documents(documents)
#
#
#
#
#
#
#
"""
initializing pinecone db
"""
print('[+] Initializing pinecone db...')
from langchain.vectorstores import Pinecone

pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment=os.getenv('PINECONE_ENV'),  # next to api key in console
)

index_name = os.getenv('PINECONE_INDEX_NAME')

index = pinecone.Index(index_name)

index.describe_index_stats()
print(index.describe_index_stats())
docsearch = Pinecone.from_documents(documents,
                                    embedding=embeddings,
                                    index_name=index_name)
#
#
#
#
#
#
#
"""
Creating vector store
"""
print('[+] Creating vector store')
text_field = "text"

# switch back to normal index for langchain
index = pinecone.Index(index_name)

# embed will be created by client
vectorstore = Pinecone(index, embeddings.embed_query, text_field)
#
#
#
#
#
#
#
"""
######## QnA ########
"""
print('[+] QnA time...')
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# completion llm
llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'),
                 model_name=model_name,
                 temperature=0.0)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    # to be done by client
    retriever=vectorstore.as_retriever()
)

# running QnA
query = "who are you?"
print(f'[-] question : {query}')
print('[+] results : ', end='')
qa.run(query)
