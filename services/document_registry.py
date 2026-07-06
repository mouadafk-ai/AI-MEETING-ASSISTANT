from pathlib import Path
import json


REGISTRY_FILE = Path("data/document_registry.json")


class DocumentRegistry:
    """
    Beheert informatie over geïndexeerde documenten.
    """

    def __init__(self):
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not REGISTRY_FILE.exists():
            REGISTRY_FILE.write_text("[]")

    def load(self):
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)

    def save(self, documents):
        with open(REGISTRY_FILE, "w") as f:
            json.dump(documents, f, indent=4)

    def add(self, document):
        documents = self.load()

        documents.append(document)

        self.save(documents)

    def all(self):
        return self.load()