from app.chat_llm import Chat
from app.rag import RagFAISS
import os


class AitanaBot:
    def __init__(self, llm_model_id="google/gemma-1.1-2b-it"):
        self.__rag_faiss = None
        self.__chat_llm = None
        self.__llm_model_id = llm_model_id

    def __get_faiss_db(self, modelST_id='avsolatorio/GIST-small-Embedding-v0'):
        if self.__rag_faiss is None:
            self.__rag_faiss = RagFAISS(modelST_id)

        return self.__rag_faiss

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
        rag_faiss = self.__get_faiss_db()
        return rag_faiss.search(query, k)
