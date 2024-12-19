from typing import Protocol, Tuple

import chromadb

from src.model.embed import Embedder, LocalEmbedder


class Store(Protocol):

    def create_store(self, store_name: str, file_names: list[str]):
        """
            Creates a new store by embedding the files passed in file_names.
            If the store is already created, it is deleted and created once more
        """
        pass
    
    def create_from_documents(self, store_name: str, files: dict[str, str]):
        """
            Same as create_store, but recieves the contents of the files directly
        """
        pass

    def search(self, collection: str, query: str) -> list[str]:
        """
            Searches in the database based on the query and returns a list of documents
            that are closely related to the embedding
        """
        return []
    

class ChromaLocalStore:

    def __init__(self, location: str):
        self.db = chromadb.PersistentClient(location)
        self.embedder: Embedder = LocalEmbedder() 

    def __process_file(self, file_name: str) -> list[str]:
        """
            Reads the contents of a file (taking a couple lines at a time)
        """
        contents = []
        with open(file_name) as file:
            readed = file.read(500)
            i = -1
            while i > -len(readed) and readed[i].isalnum():
                i -= 1
            contents.append(readed[:i])
        return contents

    def __read_files(self, file_names: list[str]) -> dict[str, list[str]]:
        """
            Reads the files contents and stores them in a dictionary associating
            the names of the files with their names
        """
        files: dict[str, list[str]] = {}
        for file_name in file_names:
           files[file_name] = self.__process_file(file_name)
        return files 

    def __produce_blobs(self, blobs: dict[str, list[str]]) -> list[str]:
        contents = []
        for key in blobs.keys():
            for chunk in blobs[key]:
                contents.append(f"from file: {key}; content: {chunk}")
        return contents
    
    def __embed_chunks(self, chunks: list[str]) -> Tuple[list[str], list[list[float]]]:
        embeddings = []
        for chunk in chunks:
            embeddings.append(self.embedder.embed(chunk)) 
        return chunks, embeddings 

    def create_store(self, store_name: str, file_names: list[str]):
        
        try:
            self.db.create_collection(name=store_name)
        except:
            self.db.delete_collection(name=store_name)
            self.db.create_collection(name=store_name)

        collection = self.db.get_collection(name=store_name)
        data, embeddings = self.__embed_chunks(
                self.__produce_blobs(
                    self.__read_files(
                        file_names
                        )
                    )
                )
        collection.add(ids=list(map(lambda x: str(x), range(1, len(data)+1))), embeddings=embeddings, documents=data) #type: ignore
         
    def search(self, collection: str, text: str) -> list[str]:

        _, embedding = self.__embed_chunks([text])
        
        col = self.db.get_collection(collection)
        matchings = col.query(embedding.pop(), n_results=10)
        return matchings.get("documents").pop() #type: ignore
