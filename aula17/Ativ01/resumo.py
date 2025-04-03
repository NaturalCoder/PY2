class ResearchAgent:
    def __init__(self, model="mistral"):
        self.model = model
    
    def research(self, topic):
        prompt = f"""Resuma de forma estruturada (tópicos) o seguinte assunto: {topic}.
        Inclua aplicações práticas e desafios."""
        return self._ask_ollama(prompt)
    
    def _ask_ollama(self, prompt):
        # Implementar chamada à API do Ollama (similar ao Exercício 1)
        ...

# Uso
agent = ResearchAgent()
print(agent.research("energia nuclear"))