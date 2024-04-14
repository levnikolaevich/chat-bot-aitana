import os
from ragatouille import RAGPretrainedModel

from app.content_extractor import ContentExtractor


class RAGatouilleAitana:
    def __init__(self, model_st_id="colbert-ir/colbertv2.0"):
        self.index_name = 'aitana'
        self.index_path = f".ragatouille/colbert/indexes/{self.index_name}/"
        self.RAG = None
        self.__prepare_data(model_st_id)

    def __prepare_data(self, model_st_id):
        if os.path.exists(self.index_path):
            print("Index ragatouille does exist. Skipping preparation index.")
            return

        print("Index ragatouille does not exist. Preparation index.")
        rag = RAGPretrainedModel.from_pretrained(model_st_id)
        paragraphs = ContentExtractor.extract_text_to_paragraphs()
        collection = [f'{item["page_name"]} {item["content"]}' for item in paragraphs]
        document_metadatas = [
            {
                "page_name": item["page_name"],
                "url": item["url"]
            } for item in paragraphs
        ]
        document_ids = [f'{item["index_page"]}' for item in paragraphs]

        rag.index(
            collection=collection,
            document_ids=document_ids,
            document_metadatas=document_metadatas,
            index_name=self.index_name,
            max_document_length=300,
            split_documents=True,
        )
        print("Index ragatouille preparation finished.")

    def search(self, query, k=5):
        if os.path.exists(self.index_path) is False:
            print("Index ragatouille does not exist.")
            return

        if self.RAG is None:
            print(f"'RAGatouille' is None. Loading from index {self.index_path}.")
            self.RAG = RAGPretrainedModel.from_index(self.index_path)

        if self.RAG is not None:
            print(f"'RAGatouille' exists. Searching..")
            results = self.RAG.search(query, k=k)

            output = [
                {
                    "rank": item["rank"],
                    "content": item["content"],
                    "page_name": item["document_metadata"]["page_name"],
                    "url": item["document_metadata"]["url"],
                }
                for item in results
            ]

            return output
