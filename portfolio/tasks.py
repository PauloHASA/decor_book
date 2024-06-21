from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import ImagePortfolio, NewProject
from PIL import Image
import os

@shared_task
def process_image_upload(image_id):
    try:
        image = ImagePortfolio.objects.create(id=image_id)
        image.save()
    except ImagePortfolio.DoesNotExist:
        pass

