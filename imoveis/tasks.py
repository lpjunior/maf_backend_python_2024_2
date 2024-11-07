from celery import shared_task
import datetime
from datetime import timedelta
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from gestao_alugueis.utils import enviar_email
from imoveis.models import Aluguel
import logging

logger = logging.getLogger(__name__)

@shared_task
def verificar_vencimento_aluguel():
    try:
        hoje = datetime.date.today()
        vencimento_proximo = hoje + timedelta(days=7)
        
        # Filtra aluguéis a vencer em 7 dias que ainda estão com pagamento em aberto
        alugueis_a_vencer = Aluguel.objects.filter(
            Q(pago=False) &
            Q(data_vencimento__lte=vencimento_proximo) &
            Q(data_vencimento__gte=hoje)
        )
        
        # Filtra aluguéis vencidos e ainda não pagos
        alugueis_vencidos = Aluguel.objects.filter(
            Q(pago=False) &
            Q(data_vencimento__lt=hoje)
        )
    
        logger.info(f"Aluguéis a vencer: {alugueis_a_vencer.count()}")
        logger.info(f"Aluguéis vencidos: {alugueis_vencidos.count()}")
        
        # Envia notificações para aluguéis a vencer
        for aluguel in alugueis_a_vencer:
            envia_email_notificacao(aluguel, 'proximo_vencimento')
        
        # Envia notificações para aluguéis vencidos
        for aluguel in alugueis_vencidos:
            envia_email_notificacao(aluguel, 'vencido')
            
    except Exception as e:
        logger.error(f"Erro na task de vencimento de aluguel: {e}")

def envia_email_notificacao(aluguel, tipo):
    if tipo == 'proximo_vencimento':
        assunto = f'Lembrete: Seu aluguel vence em breve'
        template_content = 'email/proximo_vencimento.html'
    else:
        assunto = 'Aviso: Seu aluguel está vencido!'
        template_content = 'email/aluguel_vencido.html'

    mensagem_html = render_to_string(template_content, {
        'aluguel': aluguel,
        'titulo_email': assunto,
        'ano_atual': datetime.datetime.now().year
    })

    plain_message = strip_tags(mensagem_html)

    enviar_email(
        destinatario=aluguel.inquilino.email,
        assunto=assunto,
        mensagem=plain_message,
        mensagem_html=mensagem_html
    )