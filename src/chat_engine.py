from query import query_index

class ChatEngine:
    def __init__(self, index, system_prompt):
        self.index = index
        self.conversation_history = []
        self.system_prompt = system_prompt

    def chat(self, query):
        self.conversation_history.append({"role": "system", "content": self.system_prompt})
        self.conversation_history.append({"role": "user", "content": query})
        response = query_index(self.index, query)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response