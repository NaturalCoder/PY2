class DebateAgent:
    def __init__(self, role):
        self.role = role  # ex: "pró-nuclear", "anti-nuclear"
    
    def argue(self, topic):
        prompt = f"""Atue como especialista {self.role}. 
        Argumente sobre {topic} em 3 parágrafos."""
        return self._ask_ollama(prompt)

# Simulação
tema = "energia nuclear"
agent_pro = DebateAgent("pró-nuclear")
agent_anti = DebateAgent("anti-nuclear")

print("Pró:", agent_pro.argue(tema))
print("\nAnti:", agent_anti.argue(tema))