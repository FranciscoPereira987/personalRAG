from typing import Annotated
import fastapi
from fastapi.param_functions import Body
from pydantic import BaseModel

from src.model.chat import Chat
from src.model.lang import LocalProvider
import chromadb


app = fastapi.FastAPI()
provider = LocalProvider()
db = chromadb.PersistentClient(path="C:/users/franc/chroma/personalRag") # TODO: Change this to a parameter

class TextInput(BaseModel):

    input: str

@app.post("/completion")
def search_for(query: Annotated[Chat, Body()]):
    return provider.search_for(query)

@app.post("/embed")
def embed_text(query: Annotated[TextInput, Body(alias="input")]):
    return provider.embed(query.input)

@app.get("/health")
def health() -> dict[str, str]:
    return {
            "status": "OK"
            }
