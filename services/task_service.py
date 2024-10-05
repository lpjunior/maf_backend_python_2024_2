from models.task_model import Task

class TaskService:
    
    def __init__(self):
        self.tarefas = []

    def adicionar_tarefa(self, conteudo): # conteudo é uma str que tem a descrição/titulo da tarefa
        if not conteudo:
            raise ValueError("A tarefa não pode ser vazia")
        
        nova_tarefa = Task(conteudo, False) # Task(conteudo, False) é a instanciação da classe Task
        self.tarefas.append(nova_tarefa) # Adição da nova tarefa na lista
            

    def listar_tarefas(self):
        return self.tarefas

    def completar_tarefa(self, tarefa_id):
        self.tarefas[tarefa_id].completa = True

    def remover_tarefa(self, tarefa_id):
        self.tarefas.pop(tarefa_id)