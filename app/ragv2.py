import os
from ragatouille import RAGPretrainedModel

from app.content_extractor import ContentExtractor


class RAGatouilleAitana:
    def __init__(self, model_st_id="colbert-ir/colbertv2.0"):
        self.index_name = 'aitana'
        self.index_path = f".ragatouille/colbert/indexes/{self.index_name}/"
        self.RAG = RAGPretrainedModel.from_pretrained(model_st_id)
        self.__prepare_data(model_st_id)

    def __prepare_data(self, model_st_id):
        if os.path.exists(self.index_path):
            return

        rag = RAGPretrainedModel.from_pretrained(model_st_id)
        text2vec = ContentExtractor.extract_text_to_paragraphs()
        collection = [f'{item["page_name"]} {item["content"]}' for item in text2vec]
        document_ids = [f'{item["index_page"]}' for item in text2vec]
        rag.index(
            collection=collection,
            document_ids=document_ids,
            index_name=self.index_name,
            max_document_length=300,
            split_documents=True,
        )

    def get_RAG(self):
        return RAGPretrainedModel.from_index(self.index_path)
