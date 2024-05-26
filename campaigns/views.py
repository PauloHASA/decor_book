from django.shortcuts import render
from django.http import HttpResponse
from .email_utils import send_custom_email

def send_test_email(request):
    subject = 'Test de envio de email'
    message = 'Este e um email de teste'
    recipient_list = ['paulohasa@gmail.com']
    
    send_custom_email(subject,
                      message,
                      recipient_list
                      )
    
    return HttpResponse("E-mail enviado com sucesso!")