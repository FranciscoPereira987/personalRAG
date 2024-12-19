import requests as r
from typing import Any, Optional, Protocol

from src.model.chat import Chat, ChatRepository, LocalRepository

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
                 port: str = "1234",
                 base_prompt: str = "",
                 model: str = "llama-3.2-3b-instruct",
                 embed_model: str = "text-embedding-nomic-embed-text-v1.5",
                 temperature: float = 0.7,
                 max_tokens: int = -1):
        self.conn_string = f"http://127.0.0.1:{port}"
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_prompt = base_prompt
        self.embed_model = embed_model
        self.chats: ChatRepository = LocalRepository()
    
    def __base_story(self) -> list[dict[str, str]]:
        return [
                {"role": "system", "content": self.base_prompt},
                ]

    def __req_dic(self, query: str, chat_id: Optional[str]) -> dict[str, Any]:
        
        chat_story = self.chats.get_chat(chat_id) if chat_id is not None else self.__base_story()  
        chat_story.append({"role": "user", "content": query})
        return {
                    "model": self.model,
                    "messages": chat_story, 
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": False
                }
    
    def __embed_dic(self, query: str) -> dict[str, Any]:
        return {
                    "model": self.embed_model,
                    "input": query,
                    "encoding_format": "float"
                }
    
    def __update_chat(self, json_dic: dict[str, Any], chat: Chat):
        id = chat.chat_id
        if id is None:
            id = json_dic.get("id", "")
            base = self.__base_story()
            self.chats.store_in_chat(id, base[0].get("role", ""), base[0].get("content", ""))
        response: dict[str, str] = json_dic.get("choices", [])[0].get("message")
        self.chats.store_in_chat(id, "user", chat.input)
        self.chats.store_in_chat(id, response.get("role", "assistant"), response.get("content", ""))

    def search_for(self, query: Chat) -> str:
        request = self.__req_dic(query.input, query.chat_id)
        response = r.post(f"{self.conn_string}/v1/chat/completions", json=request)
        response_json = response.json()
        self.__update_chat(response_json, query)
        return response_json

    def embed(self, query: str) -> str:
        response = r.post(f"{self.conn_string}/v1/embeddings", json=self.__embed_dic(query))
        return response.json()
