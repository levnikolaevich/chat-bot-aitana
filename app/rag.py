from sentence_transformers import SentenceTransformer
import faiss
import os

from app.content_extractor import ContentExtractor


class RagFAISS:
    def __init__(self, model_st_id='avsolatorio/GIST-small-Embedding-v0', index_file='rag-faiss/faiss_index.bin'):
        # Initialize the SentenceTransformer model on creation of a RagFAISS instance
        self.index_file = index_file
        self.modelST = SentenceTransformer(model_st_id)
        self.indexFlatIP = None  # Placeholder for the FAISS index
        self.text = []  # Placeholder for the paragraphs extracted from the PDF
        self.normalize = False  # Flag to indicate whether to normalize embeddings
        self.__prepare_data()

    def __prepare_data(self):
        text2vec = ContentExtractor.extract_text_to_paragraphs()
        self.__read_or_create_faiss_index(text2vec)

    def search(self, query, k=5):
        """
        Search the FAISS index for the k most similar paragraphs to the query.

        Args:
            query (str): The query string.
            k (int): The number of results to return.

        Returns:
            tuple: Cosine similarities, indices of nearest neighbors, and the paragraphs corresponding to those indices.
        """
        # Encode the query and prepare it for FAISS search
        query_embedding = self.modelST.encode(query)
        xq = query_embedding.reshape(1, -1)
        if self.normalize:
            faiss.normalize_L2(xq)

        # Perform the search on the index
        D, I = self.indexFlatIP.search(xq, k)  # D - cosine similarities, I - indices of nearest neighbors
        RAG_context = [self.text[idx] for idx in I[0]]
        return D, I, RAG_context

    def __read_or_create_faiss_index(self, paragraphs, normalize=False):
        """
        Load a FAISS index from a file if it exists, or create one using embeddings
        from the provided paragraphs.

        Args:
            paragraphs (list): A list of paragraphs to index.
            normalize (bool): Whether to normalize the embeddings.
        """
        if os.path.exists(self.index_file):
            # Load the FAISS index from the file
            self.indexFlatIP = faiss.read_index(self.index_file)
            self.text = paragraphs
            print("FAISS index loaded from file.")
        else:
            # Create the FAISS index and save it to the file
            self.create_faiss_index(paragraphs, normalize)
            faiss.write_index(self.indexFlatIP, self.index_file)
            print(f"FAISS index created and saved to {self.index_file}.")

    def create_faiss_index(self, paragraphs, normalize=False):
        """
        Create a FAISS index using embeddings from the provided paragraphs.

        Args:
            paragraphs (list): A list of paragraphs to index.
            normalize (bool): Whether to normalize the embeddings.
        """
        self.normalize = normalize
        self.text = paragraphs
        corpus = [f'{item["page_name"]} {item["content"]}' for item in paragraphs]
        embeddings = self.modelST.encode(corpus, show_progress_bar=True)

        # Normalize embeddings if required
        if self.normalize:
            faiss.normalize_L2(embeddings)

        # Initialize and populate the FAISS index
        d = embeddings.shape[1]  # Dimensionality of embeddings
        self.indexFlatIP = faiss.IndexFlatIP(d)
        self.indexFlatIP.add(embeddings)
