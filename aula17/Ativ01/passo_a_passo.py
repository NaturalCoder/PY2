class MathAgent:
    def solve(self, problem):
        prompt = f"""Resolva o problema passo a passo:
        {problem}
        """
        solution = self._ask_ollama(prompt)
        return self._extract_answer(solution)
    
    def _extract_answer(self, text):
        # Extrai a resposta final (ex: "Resposta: 42")
        ...

# Teste
math_agent = MathAgent()
print(math_agent.solve("Qual é a soma dos ângulos internos de um pentágono?"))