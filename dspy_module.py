import dspy
from dspy.retrieve.faiss_rm import FaissRM

from app.content_extractor import ContentExtractor


class DSPyModule:
    def __init__(self, llm_model_id='google/gemma-1.1-2b-it'):
        self.faiss = None
        self.llm = dspy.HFModel(model=llm_model_id)
        self.dspy = dspy.settings.configure(lm=self.llm, rm=self.faiss)
        self.__prepare_data()

    def __prepare_data(self):
        text2vec = ContentExtractor.extract_text_to_paragraphs()
        print("text2vec:", text2vec)
        self.faiss = FaissRM(text2vec)

    def search(self, query, k=5):
        return self.faiss(query, k)


module = DSPyModule()
output = module.search("query", 5)
print(output)