import json
from typing import List
from document import Document


class DocumentCreator:
    def from_csv(self, file_name: str) -> List[Document]:
        documents: List[Document] = []

        with open(file_name, "rt") as file_in:
            docs_json = json.load(file_in)

            for doc_json in docs_json:
                doc = Document.create(doc_json["section"], doc_json["question"], doc_json["text"], doc_json["id"])
                documents.append(doc)

        return documents
