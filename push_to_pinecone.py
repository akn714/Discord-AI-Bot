import pinecone

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Pinecone

import os
from dotenv import load_dotenv

load_dotenv()

pinecone.init(os.getenv("MY_PINECONE_API_KEY"),
              environment=os.getenv("MY_PINECONE_ENV"))

index_name = 'test-index'
index = pinecone.Index(index_name)
# pinecone.create_index('test-index', dimension=128)

# loading the data
loader = PyPDFLoader("./know-india-booklet.pdf")
data = loader.load()
# Create an instance of OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

# splitting the data
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512,
                                               chunk_overlap=10)

# getting the docs
documents = text_splitter.split_documents(data)

docsearch = Pinecone.from_texts([t.page_content for t in documents],
                                embeddings,
                                index_name=index_name)

query = "write all the names of states in india"
docs = docsearch.similarity_search(query)

# index.upsert(vectors=zip(ids, vecs))
