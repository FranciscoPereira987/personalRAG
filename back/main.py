import os
from typing import Annotated
import fastapi
from fastapi.param_functions import Body
from fastapi.params import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from back.src.model.embed import LocalEmbedder
from src.model.chat import Chat
from src.model.lang import LocalProvider
from fastapi.middleware.cors import CORSMiddleware

class Settings(BaseSettings):
    chroma_location: str = "/home/franciscopereira/chromadb"
    service_addr: str = "http://127.0.0.1"
    service_port: str = "1234"
    model: str = "llama-3.2-3b-instruct"
    embed_model: str = "text-embedding-nomic-embed-text-v1.5"
    temperature: float = 0.7
    max_tokens: int = -1

settings = Settings()
app = fastapi.FastAPI()
embedder = LocalEmbedder(settings.service_addr, settings.service_port, settings.embed_model)
provider = LocalProvider(
   embedder=embedder,
   llm_service=settings.service_addr,
   port=settings.service_port,
   model=settings.model,
   embed_model=settings.embed_model,
   temperature=settings.temperature,
   max_tokens=settings.max_tokens,
   store_location=settings.chroma_location 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

class TextInput(BaseModel):
    input: str

class CollectionQuery(BaseModel):
    collection: str
    input: str

class CollectionInput(BaseModel):
    collection: str
    file_names: list[str]

class StorePathInitialization(BaseModel):
    store_name: str
    store_path: str

class FileInput(BaseModel):
    name: str

def walk_directory(directory: str) -> list[str]:
    """
        Walks a directory, returning all the files contained within it
    """
    entries = os.listdir(directory)
    files = []
    for entry in entries:
        path = os.path.join(directory, entry)
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path) and not entry.startswith(".") and not entry.startswith("_"):
            files += walk_directory(path)
    return files

@app.post("/completion")
def search_for(query: Annotated[Chat, Body()]):
    return provider.search_for(query)

@app.get("/chats/{chat_id}")
def get_chat_history(chat_id: Annotated[str, Path()]):
    return provider.get_chat(chat_id)

@app.post("/chats/{chat_id}")
def create_new_chat(chat_id: Annotated[str, Path()]):
    provider.create_new_chat(chat_id) 

@app.get("/chats")
def query_chats() -> list[str]:
    """
        Returns all chat's id stored
    """
    return provider.get_chats() 

@app.post("/stores")
def start_queried_chat(dir: Annotated[StorePathInitialization, Body()]):
    files = walk_directory(dir.store_path)
    provider.create_store(dir.store_name, files) 

@app.post("/stores/directory/{store_id}")
def add_directory_to_store(store_id: Annotated[str, Path()], dir: Annotated[FileInput, Body()]):
    files = walk_directory(dir.name)
    provider.add_to_store(store_id, files)
    return

@app.post("/stores/file/{store_id}")
def add_file_to_store(store_id: Annotated[str, Path()], file: Annotated[FileInput, Body()]):
    return

@app.get("/stores")
def query_stores() -> list[str]:
    """
        Returns all store's names 
    """
    return provider.get_collections() 

@app.post("/store/{store}/directory")
def add_directory(store: Annotated[str, Path()], dir: Annotated[FileInput, Body()]):
    """
        Adds all files in the given directory into the given store
    """
    files = walk_directory(dir.name)
    provider.add_to_store(store, files)

@app.post("/store/{store}/file")
def add_file(store: Annotated[str, Path()], file: Annotated[FileInput, Body()]):
    """
        Add the given file into the given store
    """ 
    provider.add_to_store(store, [file.name]) 

# TODO: Try to find the way to retrieve the most similar files
@app.post("/similar")
def search_similar(query: Annotated[CollectionQuery, Body()]):
    return provider.db.search(query.collection, query.input) 

# TODO: Create two different endpoints; 1- To just start it, 2- To read a directory and start it
@app.post("/collection")
def create_collection(query: Annotated[CollectionInput, Body()]):
    provider.create_store(query.collection, query.file_names)

# TODO: Should just delete it when the time comes
@app.post("/embed")
def embed_text(query: Annotated[TextInput, Body(alias="input")]):
    return provider.embed(query.input)

@app.get("/health")
def health() -> dict[str, str]:
    return {
            "status": "OK"
            }
