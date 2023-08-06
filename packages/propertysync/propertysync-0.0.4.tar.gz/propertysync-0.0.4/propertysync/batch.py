import json
from .document import Document

"""
This is a helper class for working with PropertySync batches.
"""

class Batch:
    
    def __init__(self, json_string=None):
        self.documents = []
        self._json = json_string

        if "id" in self._json:
            self.id = self._json["id"]
        else:
            self.id = None        

        for doc in self._json["documents"]:
            self.documents.append(Document(doc))
    
    def __len__(self):
        return len(self.documents)
    
    def documents_with_tags(self, tags):
        return [doc for doc in self.documents if set(tags).issubset(set(doc.tags))]
    
    def documents_without_tags(self, tags):
        return [doc for doc in self.documents if not set(tags).issubset(set(doc.tags))]
    
    # get documents with a specific instrumentType value
    def documents_with_instrument_type(self, instrument_type):
        return [doc for doc in self.documents if doc.instrumentType == instrument_type]