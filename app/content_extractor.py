import os
import json


class ContentExtractor:
    @staticmethod
    def extract_text_to_paragraphs(json_path="rag-faiss/page_contents.json"):
        # Iterate through all files in the specified folder
        content = []

        # Check if the JSON file exists
        if os.path.exists(json_path):
            # Open and read the JSON file
            with open(json_path, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                # Assuming json_data is a list of objects with a 'content' field
                for item in json_data:
                    if 'content' in item:
                        # Append the content field to paragraphs
                        content.append(item)

        return content
