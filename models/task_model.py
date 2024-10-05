class Task:
    def __init__(self, conteudo, completa):
        self.conteudo = conteudo        # O conteúdo ou descrição da tarefa
        self.completa = completa        # Estado da tarefa (booleano): completa ou não

    def __repr__(self):                  # Representação textual da tarefa
        return f"Tarefa('{self.conteudo}', '{self.completa}')"   
        
    def __str__(self):                  # Representação textual da tarefa
        return f"Conteúdo: {self.conteudo}, Completa: {self.completa}"
    
    def completar(self):
        self.completa = True            # Método para marcar a tarefa como completa