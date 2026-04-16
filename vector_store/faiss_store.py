from sentence_transformers import SentenceTransformer  
# library used to convert text into embeddings (numerical vectors)

import faiss  
# library used for fast similarity search (vector database)

import numpy as np  
# numerical computation library (used internally for vector operations)

import os  
# used to check whether files exist locally

import pickle  
# used to save and load stored data (texts) locally


MODEL = SentenceTransformer("paraphrase-MiniLM-L3-v2")  
# loads pre-trained embedding model
# converts text into 384-dimension vector representations


INDEX_FILE = "faiss_index.bin"  
# file name used to store FAISS vector index locally

TEXT_FILE = "faiss_texts.pkl"  
# file name used to store original text documents locally


class VectorStore:
    # class used to store embeddings and perform similarity search


    def __init__(self):
        # constructor runs automatically when class object is created

        # load existing index if available
        if os.path.exists(INDEX_FILE) and os.path.exists(TEXT_FILE):
            # checks whether saved FAISS index and stored texts exist

            self.index = faiss.read_index(INDEX_FILE)
            # loads previously saved FAISS vector index from file

            with open(TEXT_FILE, "rb") as f:
                # opens stored text file in read-binary mode

                self.texts = pickle.load(f)
                # loads stored documents into memory

        else:

            self.index = faiss.IndexFlatL2(384)
            # creates new FAISS index using L2 distance (Euclidean distance)
            # 384 is embedding dimension of MiniLM model

            self.texts = []
            # initializes empty list to store documents


    def add_documents(self, docs):
        # function used to convert documents into embeddings and store them

        # avoid duplicate embeddings
        new_docs = [
            # list comprehension to filter only new documents

            doc for doc in docs
            # iterate through documents

            if doc not in self.texts
            # include document only if not already stored
        ]

        if len(new_docs) == 0:
            # if no new documents found

            return
            # stop execution to avoid duplicate embedding computation


        embeddings = MODEL.encode(
            # converts text documents into numerical vectors

            new_docs,
            # list of documents to embed

            convert_to_numpy=True,
            # converts embeddings into numpy array format

            show_progress_bar=False
            # disables progress bar for faster execution
        )


        self.index.add(embeddings)
        # adds embeddings into FAISS vector index


        self.texts.extend(new_docs)
        # stores original text documents


        # save index for reuse
        faiss.write_index(self.index, INDEX_FILE)
        # saves FAISS index to file so it can be reused later


        with open(TEXT_FILE, "wb") as f:
            # opens text storage file in write-binary mode

            pickle.dump(self.texts, f)
            # saves stored documents to file


    def search(self, query):
        # function used to find most relevant documents based on user query

        if len(self.texts) == 0:
            # checks if vector store is empty

            return []
            # returns empty list if no documents available


        query_vector = MODEL.encode(
            # converts query text into embedding vector

            [query],
            # query is wrapped in list because model expects list input

            convert_to_numpy=True
            # converts embedding to numpy array
        )


        distances, indices = self.index.search(query_vector, 2)
        # searches FAISS index to find top 2 most similar documents
        # returns distances (similarity score)
        # returns indices (positions of matched documents)


        return [
            # returns list of relevant documents

            self.texts[i]
            # retrieves original document text using index position

            for i in indices[0]
            # iterates through returned indices

            if i < len(self.texts)
            # ensures index is within range
        ]