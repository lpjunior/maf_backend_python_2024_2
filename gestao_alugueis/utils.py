from django.conf import settings
from django.core.mail import send_mail

def enviar_email(destinatario, assunto, mensagem, mensagem_html):
    send_mail(
        subject=assunto,
        message=mensagem,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[destinatario],
        fail_silently=False,
        html_message=mensagem_html
    )