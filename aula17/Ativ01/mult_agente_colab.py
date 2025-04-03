class WriterAgent:
    def generate_draft(self, topic):
        prompt = f"Escreva um parágrafo sobre: {topic}"
        return self._ask_ollama(prompt)

class EditorAgent:
    def improve_text(self, text):
        prompt = f"Melhore este texto mantendo o significado:\n{text}"
        return self._ask_ollama(prompt)

# Fluxo colaborativo
writer = WriterAgent()
editor = EditorAgent()
draft = writer.generate_draft("IoT em agricultura")
final_version = editor.improve_text(draft)
print(final_version)