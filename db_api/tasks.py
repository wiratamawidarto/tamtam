from celery import shared_task
from django.conf import settings
import base64
import os
import cv2
import numpy as np
from .models import Picture_Files

@shared_task(name='Decode Image')
def create_decode_task(message):
    for notification_id, message_info in message.items():
        title = message_info['title']
        image = message_info['image']

    directory = settings.MEDIA_ROOT
    directory = os.path.join(directory, 'Uploaded Files')
    img_numpy_StrToBytes = image
    """ Receive message from api  """
    img_numpy_BytesToNumpy = base64.b64decode(img_numpy_StrToBytes)

    """ Convert message to Numpy"""
    img_numpy_BytesToNumpy = np.frombuffer(img_numpy_BytesToNumpy, dtype=np.uint8)

    cv2_img = cv2.imdecode(img_numpy_BytesToNumpy, flags=1)
    cv2_path = os.path.join(directory, title)
    cv2.imwrite(cv2_path, cv2_img)
    image_url = os.path.join('Uploaded Files', title)
    create_picture_file(image_url, title)


def create_picture_file(image_url, title):
    Picture_Files.objects.create(picture=image_url, identifier=title)
