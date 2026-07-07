from pathlib import Path
from datetime import datetime
from uuid import uuid4
import json

CONVERSATIONS_FILE = Path("data/conversations.json")


class ConversationManager:
    def __init__(self):
        CONVERSATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not CONVERSATIONS_FILE.exists():
            CONVERSATIONS_FILE.write_text("[]", encoding="utf-8")

    def load(self):
        with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, conversations):
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(conversations, f, indent=4, ensure_ascii=False)

    def create_conversation(self, title="Nieuwe chat"):
        conversations = self.load()

        conversation = {
            "id": str(uuid4())[:8],
            "title": title,
            "messages": [],
            "documents": [],
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }

        conversations.insert(0, conversation)
        self.save(conversations)

        return conversation

    def get_conversation(self, conversation_id):
        conversations = self.load()

        for conversation in conversations:
            if conversation["id"] == conversation_id:
                return conversation

        return None

    def update_conversation(self, updated_conversation):
        conversations = self.load()

        for index, conversation in enumerate(conversations):
            if conversation["id"] == updated_conversation["id"]:
                updated_conversation["updated_at"] = datetime.now().isoformat(timespec="seconds")
                conversations[index] = updated_conversation
                break

        self.save(conversations)

    def delete_conversation(self, conversation_id):
        conversations = self.load()
        conversations = [
            conversation
            for conversation in conversations
            if conversation["id"] != conversation_id
        ]
        self.save(conversations)

    def rename_conversation(self, conversation_id, new_title):
        conversation = self.get_conversation(conversation_id)

        if not conversation:
            return

        conversation["title"] = new_title
        self.update_conversation(conversation)

    def add_message(self, conversation_id, role, content, sources=None):
        conversation = self.get_conversation(conversation_id)

        if not conversation:
            return

        conversation["messages"].append(
            {
                "role": role,
                "content": content,
                "sources": sources or [],
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        )

        self.update_conversation(conversation)

    def add_document(self, conversation_id, document):
        conversation = self.get_conversation(conversation_id)

        if not conversation:
            return

        conversation["documents"].append(document)
        self.update_conversation(conversation)

    def all(self):
        return self.load()