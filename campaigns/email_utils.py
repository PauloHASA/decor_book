from django.core.mail import send_mail
from django.conf import settings
import pandas as pd

from campaigns.models import Dataframe


def send_custom_email(subject, message, recipient_list):
    send_mail(subject,
              message,
              settings.EMAIL_HOST_USER,
              recipient_list,
              fail_silently=True,
              )
    
    
def email_list(df):
    first_linha = df.iloc[0]
    print(first_linha)
    
    
def main():
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
        dataframe_instance.EMAIL = row['EMAIL']

        # Salvar no banco de dados
        dataframe_instance.save()
if __name__ == "__main__":
    main()