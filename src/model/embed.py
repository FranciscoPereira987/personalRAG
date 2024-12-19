from typing import Protocol
import requests as r

class Embedder(Protocol):

    def embed(self, text: str) -> list[float]:
        """
            Recieves the given text and embeds it, 
            returning the corresponding embeddings
        """
        return []
class LocalEmbedder:

    def __init__(self,
                 conn: str = "http://127.0.0.1",
                 port: str = "1234",
                 model: str = "text-embedding-nomic-embed-text-v1.5"):
        self.model = model
        self.conn_string = f"{conn}:{port}/v1/embeddings"

    def embed(self, text: str) -> list[float]:
        request = {
                "model": self.model,
                "input": text
                }
        response = r.post(self.conn_string, json=request)
        data = response.json().get("data").pop().get("embedding")
        return data
