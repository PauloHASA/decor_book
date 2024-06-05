from django.shortcuts import render
from django.http import HttpResponse
from .email_utils import send_custom_email

import pandas as pd
from campaigns.models import Dataframe
import uuid

def send_test_email(request):
    dataframe = Dataframe.objects.filter(request_id = 1)
    
    total_emails = len(dataframe)
    email_sent = 0
    email_faled = 0
    
    for df in dataframe:
        unique_id = uuid.uuid4()  
        subject = f"Seu Assunto Aqui - ID: {unique_id}"
        message = f"Seu conteúdo de mensagem aqui - ID: {unique_id}"
        subject = 'Test de envio de email'
        message = 'Este e um email de teste'
        recipient_list = [df.email]
        
        try:
            send_custom_email(subject,
                            message,
                            recipient_list,
                            )
            print(f"E-mail enviado para {df.email} - OK")
            email_sent += 1
        except Exception as e:
            print(f"Erro ao enviar e-mail para {df.email}: {e}")
            email_faled += 1
            
        print(f"------------------------------------------------")
        print(f"Total de e-mails processados: {total_emails}")
        print(f"E-mails enviados com sucesso: {email_sent}")
        print(f"E-mails que falharam: {email_faled}")
        print(f"------------------------------------------------")

    
    return HttpResponse("E-mail enviado com sucesso!")

        
def email_build(request):
    
    return render (request, "email_build.html")

def email_test(request):
    return render( request, 'test.html')