import requests as r
from typing import Any, Optional, Protocol

from src.model.chat import Chat, ChatRepository, LocalRepository
from src.model.embed import Embedder, LocalEmbedder
from src.model.prompt import BasicPrompt, PromptBuilder
from src.model.store import ChromaLocalStore, Store

class LLMProvider(Protocol):
    
    def search_for(self, query: str) -> str:
        """
            Searches for the corresponding Bedrock LLMs that 
            are similar to what the user is looking for.
        """
        return ""
    
    def embed(self, query: str) -> str:
        """
            Embeds the text in the query
        """
        return ""

class BedrockProvider:

    def __init__(self, model: str = "claude-instant", region: str = "brazil-south"):
        # TODO: Set the values and create the model 
        pass

    def search_for(self, query: str) -> str:
        # TODO: create the query and return the response from the model
        raise Exception("TODO")

class LocalProvider:

    def __init__(self,
                 llm_service: str = "http://127.0.0.1",
                 port: str = "1234",
                 model: str = "llama-3.2-3b-instruct",
                 embed_model: str = "text-embedding-nomic-embed-text-v1.5",
                 temperature: float = 0.7,
                 max_tokens: int = -1,
                 store_location: str = "."):
        self.conn_string = f"{llm_service}:{port}"
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.chats: ChatRepository = LocalRepository()
        self.embedder: Embedder = LocalEmbedder(conn=llm_service, port=port, model=embed_model)
        self.prompter: PromptBuilder = BasicPrompt()
        self.db: Store = ChromaLocalStore(store_location) 

    def __base_story(self) -> list[dict[str, str]]:
        return [self.prompter.base_prompt()]

    def __req_dic(self, query: str, store: str, chat_id: Optional[str]) -> dict[str, Any]:
        chat_story = self.chats.get_chat(chat_id) if chat_id is not None else self.__base_story()  
        chat_story += self.prompter.generate_prompt(query, store, self.db) if store != '' else self.prompter.generate_basic(query)
        return {
                    "model": self.model,
                    "messages": chat_story, 
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": False
                }
    
    def __update_chat(self, json_dic: dict[str, Any], req: list[dict[str, str]], chat: Chat):
        id = chat.chat_id
        if id is None:
            id = json_dic.get("id", "")
            base = self.__base_story()
            self.chats.store_in_chat(id, base[0].get("role", ""), base[0].get("content", ""))
        response: dict[str, str] = json_dic.get("choices", [])[0].get("message")
        self.chats.store_batch(id, req)
        self.chats.store_in_chat(id, response.get("role", "assistant"), response.get("content", ""))

    def search_for(self, query: Chat) -> str:
        request = self.__req_dic(query.input, query.store, query.chat_id)
        response = r.post(f"{self.conn_string}/v1/chat/completions", json=request)
        response_json = response.json()
        self.__update_chat(response_json, request.get("messages", [{}, {}])[-2:], query)
        return response_json

    def embed(self, query: str) -> list[float]:
        return self.embedder.embed(query)

    def get_chats(self) -> list[str]:
        return self.chats.get_chats()
    
    def get_chat(self, chat: str) -> list[dict[str, str]]:
        return self.chats.get_chat(chat)

    def get_collections(self) -> list[str]:
        return self.db.get_collections()
    
    def add_to_store(self, store_name: str, files: list[str]):
        self.db.add_to_store(store_name, files)
    
    def create_new_chat(self, chat_id: str):
        self.chats.create_chat(chat_id, self.__base_story())  

    def create_store(self, store_name: str, files: list[str]):
        self.db.create_store(store_name, files)
