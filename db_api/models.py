from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.core.files.images import ImageFile
######################################################
from mylinebot.alert import sendAlert as line_sendAlert
from mylinebot.alert import sendAlert_Picture as line_sendAlert_picture
######################################################
try:
    import Image
except ImportError:
   from PIL import Image

import cv2
import io
import os
import numpy as np
import base64
# Create your models here.

#so that there is no object with the same slug
def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(id=unique_slug).exists():
        unique_slug = slug + get_random_string(length=3)
    return unique_slug




class yolo_trial(models.Model):
    alert_choice = (
        (0, '無危險行為'),
        (1, '存在危險行為'),
        (2, '未知'),
        )


    # A slug is a string without special characters, in lowercase letters and with dashes instead of spaces
    id = models.SlugField(unique=True, max_length=50, blank=True, primary_key=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    alert = models.IntegerField(default = 0,choices=alert_choice)
    description = models.CharField(max_length=200, default='(none)')
    image = models.ImageField(upload_to='Uploaded Files/',default='',blank=True)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)


########## store the json file from the AI #################
class Yolo(models.Model):
    alert_choice = (
        (0, '無危險行為'),
        (1, '未正確配戴安全帽'),
        (2, '雙掛鉤未使用'),
        (3, '偵測到無安全網'),
        (4, '未知')
        )


    # A slug is a string without special characters, in lowercase letters and with dashes instead of spaces
    id = models.SlugField(unique=True, max_length=50, blank=True, primary_key=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    alert = models.IntegerField(default = 0,choices=alert_choice)
    description = models.CharField(max_length=200, default='(none)')
    timestamp = models.CharField(max_length=50, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    image_shape = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(editable=True, default = timezone.now)


    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = unique_slugify(self, slugify(self.title.rsplit('.', 1)[0]))
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Yolo"
#########################################################




class Yolo_Files(models.Model):
    id = models.SlugField(unique=True, max_length=50, blank=True, primary_key=True)
    yolo_id = models.ForeignKey(Yolo, on_delete=models.CASCADE,max_length=50,default="")
    #file = models.FileField(blank=True, upload_to='Uploaded Files/')
    image = models.ImageField(upload_to='Uploaded Files/',default='',blank=True)
    send_alert = models.BooleanField(default =False)
    memo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(editable=True, default = timezone.now)


    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = unique_slugify(self, slugify(self.yolo_id))
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Yolo_Files"


class Alert_Data(models.Model):

    id = models.IntegerField(primary_key = True)
    body = models.CharField(max_length=50, null=True, blank=True)

    # def __str__(self):
    #     return self.body


class Picture_Files(models.Model):
    # identifier = models.ForeignKey(Yolo, on_delete=models.CASCADE,max_length=50,default="")
    identifier = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='Uploaded Files/',default='',blank=True)
    memo = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.identifier



##### function tp give email and line notif to the manager######
def email_sendAlert(alert):
    subject = "Alert From Security System"
    #with open("/home/christopher0908/ai2021mis/db_api/message.txt", "r") as f:
    #    body = f.read()

    try:
        total_email= Alert_Data.objects.count()
        data = Alert_Data.objects.get(id = total_email )
        #data = Alert_Data.objects.first()
        body = str(data)

    except:
        with open("/home/christopher0908/ai2021mis/db_api/message.txt", "r") as f:
            body = f.read()


    alert = alert
    message = body + '@' + alert
    send_mail(subject, message, settings.RECIPIENT_ADDRESS, [settings.RECIPIENT_ADDRESS])


@receiver(post_save, sender=Yolo)
def create_alert(sender, instance, created, **kwargs):
    def decode_img():
        directory = settings.MEDIA_ROOT
        directory = os.path.join(directory, 'Uploaded Files')
        img_numpy_StrToBytes = instance.image
        """ Receive message from api  """
        img_numpy_BytesToNumpy = base64.b64decode(img_numpy_StrToBytes)

        """ Convert message to Numpy"""
        img_numpy_BytesToNumpy = np.frombuffer(img_numpy_BytesToNumpy, dtype=np.uint8)

        cv2_img = cv2.imdecode(img_numpy_BytesToNumpy, flags=1)
        cv2_path = os.path.join(directory, instance.title)
        cv2.imwrite(cv2_path, cv2_img)

        # img_numpy_fromBytesToNumpy = instance.image
        # img_numpy_toStr = base64.b64decode(img_numpy_fromBytesToNumpy)
        # pil_img = Image.fromarray(img_numpy_toStr)
        # pil_path = ('/home/christopher0908/ai2021mis/media/test_received.jpeg')
        # pil_img.save(pil_path)
        image_url = os.path.join('Uploaded Files', instance.title)
        # image_bytes = io.BytesIO(cv2_img)
        # image = ImageFile(image_bytes, name=(instance.title))
        Picture_Files.objects.create(picture=image_url, identifier=instance.title)

    if created and instance.alert:
        Yolo_Files.objects.create(id = instance.id, yolo_id = instance, )
        # email_sendAlert('YOLO')
        line_sendAlert(str(instance.id), str(instance.timestamp), str(instance.description))
        decode_img()

    elif created:
        directory = settings.MEDIA_ROOT
        directory = os.path.join(directory, 'Uploaded Files')
        img_numpy_StrToBytes = instance.image
        """ Receive message from api  """
        img_numpy_BytesToNumpy = base64.b64decode(img_numpy_StrToBytes)

        """ Convert message to Numpy"""
        img_numpy_BytesToNumpy = np.frombuffer(img_numpy_BytesToNumpy, dtype=np.uint8)

        cv2_img = cv2.imdecode(img_numpy_BytesToNumpy, flags=1)
        cv2_path = os.path.join(directory, instance.title)
        cv2.imwrite(cv2_path, cv2_img)

        # img_numpy_fromBytesToNumpy = instance.image
        # img_numpy_toStr = base64.b64decode(img_numpy_fromBytesToNumpy)
        # pil_img = Image.fromarray(img_numpy_toStr)
        # pil_path = ('/home/christopher0908/ai2021mis/media/test_received.jpeg')
        # pil_img.save(pil_path)
        image_url = os.path.join('Uploaded Files', instance.title)
        # image_bytes = io.BytesIO(cv2_img)
        # image = ImageFile(image_bytes, name=(instance.title))
        Picture_Files.objects.create(picture=image_url, identifier=instance.title)
    else:
        pass




@receiver(post_save, sender=Picture_Files)
def create_file(sender, instance, created, **kwargs):
    try:
        if created:
            target_yolo = Yolo.objects.get(title = instance.identifier)
            target = Yolo_Files.objects.get(yolo_id = target_yolo)
            target.image = instance.picture
            target.save()
    except Exception as e:
        instance.memo = e
        instance.save()

        # cannot directly match the pic, becozz picture file is cannot be the same
        # pic_data = instance.picture
        # file = Yolo_Files.objects.get(image = pic_data)
        # file.image = instance.picture #update
        # file.save()


@receiver(post_save, sender=Yolo_Files)
def send_picture(sender, instance, created, **kwargs):
    website_host = settings.WEB_HOST

    try:
        if created == False and instance.send_alert == False and instance.image.url != '':
            picture_url = website_host + str(instance.image.url)
            line_sendAlert_picture(str(instance.id), picture_url)
            instance.send_alert = True
            instance.save()

    except Exception as e:
        instance.memo = e
        instance.save()
