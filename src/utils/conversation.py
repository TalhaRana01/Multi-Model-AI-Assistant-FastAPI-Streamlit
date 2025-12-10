class ConversationManager:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})

    def clear(self):
        self.history = []
