@echo off

echo Iniciando o servidor Django...
start "Django Server" cmd /k "python manage.python runserver"

echo Iniciando o worker do Celery...
start "Celery Worker" cmd /k "celery -A gestao_alugueis worker -l info -P solo"

echo Iniciando o Celery Beat...
start "Celery Worker" cmd /k "celery -A gestao_alugueis beat -l info"

echo Todos Todos processos foram iniciados.
pause