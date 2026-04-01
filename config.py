import openai
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

# chroma_client = chromadb.Client()    # sirf ye lagana sa data temporany store hota h or server restart hona pa gayab ho jata h data

client = openai.OpenAI(
    api_key  = os.environ.get("OPEN_API_KEY"),          # api_key fetch kr raha hai .env sa humari API key
    base_url = "https://api.groq.com/openai/v1",        # ye Groq k server ko call kr raha hai
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")                       # or ye is liya use kiya h taka data delete na ho
collection    = chroma_client.get_or_create_collection(name="my_collection")        # yahan pa get_or_Create check kr raa agar collection hai to mat banao agar nai hai to bana do. This prevents duplicate collections on re-runs