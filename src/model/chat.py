from typing import Optional, Protocol

from pydantic import BaseModel


class Chat(BaseModel):
    chat_id: Optional[str] = None
    input: str

class ChatRepository(Protocol):

    def get_chat(self, chat_id: str) -> list[dict[str, str]]:
        """
            Returns a list of the questions and responses made during the chat
        """
        return []

    def store_in_chat(self, chat_id: str, role: str, input: str):
        """
            Stores the user_input and response in the chat referenced by chat_id
        """

class LocalRepository:

    def __init__(self):
        self.chats: dict[str, list[dict[str, str]]] = {}

    def get_chat(self, chat_id: str) -> list[dict[str, str]]:
        #Returns the chat till this moment
        return self.chats.get(chat_id, [])

    def store_in_chat(self, chat_id: str, role: str, input: str):
        chat = self.get_chat(chat_id)
        #If chat is empty, initialize it
        if not chat:
            self.chats[chat_id] = []
        self.chats[chat_id].append({"role": role, "content": input})
 
