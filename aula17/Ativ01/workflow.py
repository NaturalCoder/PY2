class Pipeline:
    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "writer": WriterAgent(),
            "editor": EditorAgent()
        }
    
    def run(self, topic):
        research = self.agents["researcher"].research(topic)
        draft = self.agents["writer"].generate_draft(research)
        return self.agents["editor"].improve_text(draft)

# Execução
pipeline = Pipeline()
print(pipeline.run("carros autônomos"))