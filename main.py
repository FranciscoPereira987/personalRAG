import os
from os.path import isdir, isfile
from typing import Annotated
import fastapi
from fastapi.param_functions import Body
from pydantic import BaseModel
from src.model.chat import Chat
from src.model.lang import LocalProvider
from src.model.store import ChromaLocalStore

app = fastapi.FastAPI()
provider = LocalProvider()
db = ChromaLocalStore(location="/home/franciscopereira/chromadb")# TODO: Change this to a parameter

class TextInput(BaseModel):

    input: str

class CollectionQuery(BaseModel):
    collection: str
    input: str

class CollectionInput(BaseModel):
    collection: str
    file_names: list[str]

class ChatInitialization(BaseModel):
    directory: str
    chat_name: str

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
    data = "There is no data, so just answer the question."
    if query.store is not None:
        result = db.search(query.store, query.input)
        data = 'Entry: '.join(result)

    query.input = f"Try to answer the following: {query.input} based on this data: {data}"
    return provider.search_for(query)

@app.post("/completion/start")
def start_queried_chat(dir: Annotated[ChatInitialization, Body()]):
    files = walk_directory(dir.directory)
    db.create_store(dir.chat_name, files) 
    
@app.post("/similar")
def search_similar(query: Annotated[CollectionQuery, Body()]):
    return db.search(query.collection, query.input) 

@app.post("/collection")
def create_collection(query: Annotated[CollectionInput, Body()]):
    db.create_store(query.collection, query.file_names)

@app.post("/embed")
def embed_text(query: Annotated[TextInput, Body(alias="input")]):
    return provider.embed(query.input)

@app.get("/health")
def health() -> dict[str, str]:
    return {
            "status": "OK"
            }
