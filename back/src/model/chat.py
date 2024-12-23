from typing import Optional, Protocol

from pydantic import BaseModel


class Chat(BaseModel):
    #Works as an identifier to the datastore that the user wants to use for this particular chat
    store: str = "" 
    #ID for chat history
    chat_id: Optional[str] = None
    #User input
    input: str

class ChatRepository(Protocol):

    def get_chat(self, chat_id: str) -> list[dict[str, str]]:
        """
            Returns a list of the questions and responses made during the chat
        """
        return []

    def get_chats(self) -> list[str]:
        """
            Returns the IDs of all chats currently stored.
            # TODO: could add a feature later to return only the chats associated with a given user
        """
        return []

    def store_in_chat(self, chat_id: str, role: str, input: str):
        """
            Stores the user_input and response in the chat referenced by chat_id
        """
    
    def store_batch(self, chat_id: str, entries: list[dict[str, str]]):
        """
            Stores the whole list, where every entry should have a 'role' and a 'content'
            key
        """
    def create_chat(self, chat_id: str, base: list[dict[str, str]]):
        """
            Initializes a new chat, or recreates if it already exists
        """

class LocalRepository:

    def __init__(self):
        self.chats: dict[str, list[dict[str, str]]] = {}

    def get_chat(self, chat_id: str) -> list[dict[str, str]]:
        chat = self.chats.get(chat_id, [])
        return list(
                filter(
                    lambda x: x['role'] != "system",
                    chat
                    )
                )

    def store_in_chat(self, chat_id: str, role: str, input: str):
        chat = self.get_chat(chat_id)
        #If chat is empty, initialize it
        if not chat:
            self.chats[chat_id] = []
        self.chats[chat_id].append({"role": role, "content": input})
    
    def create_chat(self, chat_id: str, base: list[dict[str, str]]):
        self.chats[chat_id] = base

    def get_chats(self) -> list[str]:
        return list(self.chats.keys())

    def store_batch(self, chat_id: str, entries: list[dict[str, str]]):
        for entry in entries:
            self.store_in_chat(chat_id, entry.get("role", "unknown"), entry.get("content", ""))
