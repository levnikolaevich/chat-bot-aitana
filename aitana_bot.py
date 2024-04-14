from app.chat_llm import Chat
from app.rag_faiss import RagFAISS
import os

from app.rag_ragatouille import RAGatouilleAitana


class AitanaBot:
    def __init__(self, llm_model_id="google/gemma-1.1-2b-it", rag_engine="ragatouille"):
        print("AitanaBot init...")
        self.__rag_faiss = None
        self.__rag_RAGatouille = None
        self.__chat_llm = None

        # 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        self.__modelST_id = 'sentence-transformers/LaBSE'
        self.__llm_model_id = llm_model_id
        self.__rag_engine = rag_engine

    @staticmethod
    def get_available_llm():
        return ["google/gemma-1.1-2b-it", "google/gemma-1.1-7b-it"]

    @staticmethod
    def get_available_RAG_engine():
        return ["ragatouille", "faiss"]

    def __get_RAG(self):
        print(f"Get RAG engine: {self.__rag_engine}")
        if self.__rag_engine == "faiss":
            if self.__rag_faiss is None:
                self.__rag_faiss = RagFAISS(self.__modelST_id)
            return self.__rag_faiss

        elif self.__rag_engine == "ragatouille":
            if self.__rag_RAGatouille is None:
                self.__rag_RAGatouille = RAGatouilleAitana()
            return self.__rag_RAGatouille

    def __get_chat_llm(self):
        if self.__chat_llm is None:
            self.__chat_llm = Chat(self.__llm_model_id)

        return self.__chat_llm

    # ====================
    # = Chat LLM Region
    # ====================

    def get_answer(self, content, max_new_tokens=250):
        chat_llm = self.__get_chat_llm()
        return chat_llm.get_answer(content, max_new_tokens)

    def update_chat_history(self, histories):
        chat_llm = self.__get_chat_llm()
        return chat_llm.update_chat_history(histories)

    def get_chat_history(self):
        chat_llm = self.__get_chat_llm()
        return chat_llm.get_chat_history()

    def clean_cache(self):
        chat_llm = self.__get_chat_llm()
        chat_llm.clean_chat_history()

    # ====================
    # = Rag FAISS Region
    # ====================

    def search_in_faiss_index(self, query, k=5):
        rag = self.__get_RAG()
        return rag.search(query, k)
