from django.shortcuts import render
from django.http import HttpResponse
from .email_utils import send_custom_email

import pandas as pd
from campaigns.models import Dataframe

def send_test_email(request):
    subject = 'Test de envio de email'
    message = 'Este e um email de teste'
    recipient_list = ['paulohasa@gmail.com']
    
    send_custom_email(subject,
                      message,
                      recipient_list
                      )
    
    return HttpResponse("E-mail enviado com sucesso!")


def email_build(request):
    
    return render (request, "email_build.html")


def main(request):
    file_path = r'media\email_list_test.csv'
    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        dataframe_instance = Dataframe()
        
        dataframe_instance.request_id = 1
        dataframe_instance.admin_id = row['ADMIN_ID']
        dataframe_instance.name = row['PRFSNL_ORG_RGSTRD_NM']
        dataframe_instance.addr_pstl_cd = row['ADDR_PSTL_CD']
        dataframe_instance.latitude = row['LATITUDE']
        dataframe_instance.longitude = row['LONGITUDE']
        dataframe_instance.coord_geoc = row['GEOC']
        dataframe_instance.email = row['EMAIL']

        dataframe_instance.save()
        
    if __name__ == "__main__":
        main()
        
    return HttpResponse("Deu certo !")
