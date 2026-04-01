import os 
from dotenv import load_dotenv, dotenv_values 
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
import time 

load_dotenv()

MAX_NUM_OF_QUESTIONS = 40
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHROMA_COLLECTION = "question_collection"
CHROMA_PATH          = "../chroma"


# Set environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

print('--ENVIRONMENT VARIABLES LOADED--')

#configure the LLM model
llm = ChatOpenAI(
    api_key = OPENAI_API_KEY,
    base_url =OPENAI_BASE_URL,
    model= LLM_MODEL,
    temperature = 0
)

#configuring the embedding model
embedding_model = OpenAIEmbeddings(
    api_key = OPENAI_API_KEY,
    base_url = OPENAI_BASE_URL,
    model = EMBEDDING_MODEL
)

chromadb_client = chromadb.PersistentClient(
    path = CHROMA_PATH 
)
print('--CHROMA CLIENT CREATED--')

# Set up vectorstore
vector_store = Chroma(
    collection_name = CHROMA_COLLECTION,
    collection_metadata = {'hnsw:space': 'cosine'},
    embedding_function = embedding_model,
    client = chromadb_client,
    persist_directory = CHROMA_PATH 
)

print('--VECTOR STORE SET UP SUCESSFULLY --')

# Initialize the TavilySearch tool here
tavily_search = TavilySearch(max_results = 1,
                             search_depth = 'advanced',
                             include_raw_content = True,
                             include_images = False,
                             include_answer=True)

print('--TAVILYSEARCH INICIALIZED --')

#create a function to check how fast each code runs 
def tictoc(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()-t1
        print(f'took {t2} seconds')
    return wrapper 