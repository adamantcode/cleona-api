import os
import qdrant_client
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings


class VectorStore:
    def __init__(self):
        self.client = qdrant_client.QdrantClient(
            os.getenv("QDRANT_HOST"),
            api_key=os.getenv("QDRANT_API_KEY"),
            timeout=60
        )

        # Vector size: 1536
        self.embeddings = OpenAIEmbeddings()

        self.vector_store = Qdrant(
            client=self.client,
            collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
            embeddings=self.embeddings,
        )

        self.max_len = 500

    def _split_array(self, input_array):
        result = []
        current_array = []

        for item in input_array:
            if len(current_array) >= self.max_len:
                result.append(current_array)
                current_array = []
            current_array.append(item)

        if current_array:
            result.append(current_array)

        return result

    def get_vectorstore(self):
        return self.vector_store

    def add(self, text_chunks, metadata):
        # Chunks are batched to avoid timeouts
        batched_chunks = self._split_array(text_chunks)

        for chunks in batched_chunks:
            # metadatas needs to be the same length as chunks
            self.vector_store.add_texts(texts=chunks, metadatas=[
                                        metadata] * len(chunks))
