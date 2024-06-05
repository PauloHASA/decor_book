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
    
    

    
    
