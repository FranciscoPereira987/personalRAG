from langchain.llms.bedrock import BedrockLLM
from typing import Protocol

class LLMProvider(Protocol):
    
    def search_for(self, query: str) -> str:
        """
            Searches for the corresponding Bedrock LLMs that 
            are similar to what the user is looking for.
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

    def __init__(self):
        # TODO: Set the values to answer based on something that is self-hosted
        pass

    def search_for(self, query: str) -> str:
        # TODO: create the query and return the response from the model
        raise Exception("TODO")
    
    
