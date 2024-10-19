from repositories.task_repository import TaskRepository

class TaskService:
    def adicionar_tarefa(self, conteudo, user_id, prioridade="Média"):
        if not conteudo or not conteudo:
            raise ValueError("A tarefa não pode ser vazia")

        TaskRepository.add_task(conteudo, user_id, prioridade)

    def listar_tarefas(self, user_id):
        return TaskRepository.get_all_tasks(user_id)

    def completar_tarefa(self, tarefa_id):
        TaskRepository.complete_task(tarefa_id)

    def remover_tarefa(self, tarefa_id):
        TaskRepository.delete_task(tarefa_id)

    @staticmethod
    def listar_tarefas_com_usuarios():
        return TaskRepository.get_tasks_with_users()