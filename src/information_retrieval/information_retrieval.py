from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

def get_openai_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()
os.environ["OPENAI_API_KEY"] = get_openai_api_key("api_key.txt")

class DocumentSearcher:
    def __init__(self, folder_path, glob_pattern="**/*.txt"):        
        self.loader = DirectoryLoader(folder_path, glob=glob_pattern)
        self.embeddings = OpenAIEmbeddings()
        self.db = self.index_documents()

    def index_documents(self):
        documents = self.loader.load()
        db = FAISS.from_documents(documents, self.embeddings)
        return db

    def search_documents(self, query, k=3):
        retriever = self.db.as_retriever(search_kwargs={"k": k})
        return retriever.get_relevant_documents(query)

if __name__ == "__main__":
    # Example usage
    folder_path = 'example/algorithm_video/transnetv2/segments'
    document_searcher = DocumentSearcher(folder_path)
    query = "What is BFS"
    docs = document_searcher.search_documents(query)
    print(docs)