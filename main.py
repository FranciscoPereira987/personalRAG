from typing import Annotated
import fastapi
from fastapi.param_functions import Body
from pydantic import BaseModel

from src.model.chat import Chat
from src.model.lang import LocalProvider
import chromadb

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

@app.post("/completion")
def search_for(query: Annotated[Chat, Body()]):
    return provider.search_for(query)

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
