from typing import Protocol

from src.model.store import Store

BASIC_PROMPT = "You are an assistant that answer questions based on the information that is given to you by the system"



class PromptBuilder(Protocol):
    
    def generate_prompt(self, input: str, store: str, db: Store) -> list[dict[str, str]]:
        """
            Based on the input given by the user, the store that should be used
            and the database returns the prompt to pass down to the model.
        """
        return []

    def base_prompt(self) -> dict[str, str]:
        """
            Returns a base prompt, given by a developer role to kick-off the conversation.
        """
        return {}
    
    def generate_basic(self, query: str) -> list[dict[str, str]]:
        """
            Returns a basic prompt with just a user role input
        """
        return []

class BasicPrompt:

    def __init__(self, base_prompt: str = BASIC_PROMPT):
        self.base = base_prompt
    
    def __build_info(self, info: list[str]) -> str:
        text = ""
        for chunk in info:
            text += f"Entry text: {chunk}\n"

        return text

    def base_prompt(self) -> dict[str, str]:
        return {
                "role": "system",
                "content": self.base
                }

    def generate_prompt(self, input: str, store: str, db: Store) -> list[dict[str, str]]:
        info = db.search(store, input)
        info_text = self.__build_info(info)
        return [
                {"role": "system", "content": f"Use the following information to answer the user question: {info_text}"},
                {"role": "user", "content": input}
                ]

    def generate_basic(self, query: str) -> list[dict[str, str]]:
        return [
                {"role": "user", "content": query}
                ]
