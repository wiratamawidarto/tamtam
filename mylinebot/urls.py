from django.urls import path

from db_api.models import Yolo
from .models import Manager

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
###################################################################
# from linebot import urls as ul
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

from .alert import alert_message, clear_tasks_queue_web_control
from .views import callback as new_callback

from employee.models import employee #there is gongHao name company
from employee.models import Company



import configparser

config = configparser.ConfigParser()
config.read('/home/christopher0908/ai2021mis/mylinebot/config.ini')

ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@csrf_exempt

#### new callback function in /mylinebot/views.py
def callback(request):
    global password
    sent_json = json.loads(request.body)
    sent_message = sent_json['events'][0]['message']['text']
    reply_token = sent_json['events'][0]['replyToken']
    user_id = sent_json['events'][0]['source']['userId']

    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    result = requests.get(f'https://api.line.me/v2/bot/profile/{user_id}', headers=headers)
    user_name = json.loads(result.text)['displayName']


    password = ""
    #store the data

    dictionary = {}
    mydata_worker = employee.objects.all()

    for i in mydata_worker:
        worker_name = i.name
        worker_id = i.gongHao
        dictionary.update({worker_id:worker_name})
        #idea is that the worker_name will be changed become a password. to improve the security



    if sent_message == '查看':
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text='好的請稍候'))
            instances = Yolo.objects.all().filter(alert='1').order_by('-created_at',)
            count = 1
            text = '最近的警報:\n'
            for instance in instances:
                instance_id = str(instance)
                instance_date = str(instance.timestamp)
                instance_description = str(instance.description)
                text = text + f'\n案件{count}\nid: {instance_id}\n日期: {instance_date}\n說明: {instance_description}\n'
                count = count + 1
            text = text + f'\n總共 {count}個警報 \n'
            message = TextSendMessage(text=text)
            # message = TextSendMessage(text='好的請稍後')
            # line_bot_api.reply_message(reply_token, message)


            # Get dummy data using an API
            # res = requests.get("https://christopher0908.pythonanywhere.com/api/yolo/")
            # # Convert data to dict
            # data = json.loads(res.text)
            # line_bot_api.multicast(['U2e7451ade23b2add1c75be792543d606'], TextSendMessage(text=str(data)))
            # message = TextSendMessage(text=str(data))
            # count = Yolo.objects.all().filter(alert='1').order_by('-created_at',).count()
            # message = str(result) + f'\n總共{count}筆'
        except Exception:
            message = TextSendMessage(text=f'{user_name} something wrong')



    elif sent_message == 'admin activate':
        try:
            instance = Manager.objects.get(line_id = user_id)
            message = TextSendMessage(text=f'『{user_name}』已經是系統管理員')
        except ObjectDoesNotExist:
            Manager.objects.create(name=user_name, line_id=user_id)
            message = TextSendMessage(text=f'已添加『{user_name}』為系統管理員')


    elif sent_message == 'flex':
        try:
            message = FlexSendMessage(alt_text='test', contents=alert_message())
        except Exception:
            message = TextSendMessage(text=str(Exception))


    elif sent_message == '註冊':
        try:
            instance = Manager.objects.get(line_id = user_id)
            message = TextSendMessage(text=f'『{user_name}』your acc has already been activated')
        except ObjectDoesNotExist:
            message = TextSendMessage(text='please enter your ID')


    elif sent_message in dictionary:
        #we must check if the password is correct
        #password = dictionary[sent_message]

        Manager.objects.create(name=user_name, line_id=user_id)
        message = TextSendMessage(text=f' your username『{user_name}』is succefully created')


    elif sent_message == 'admin deactivate':
        try:
            instance = Manager.objects.get(line_id = user_id)
            instance.delete()
            message = TextSendMessage(text=f'管理員『{user_name}』，已被移除')
        except ObjectDoesNotExist:
            message = TextSendMessage(text = f'『{user_name}』不是管理員')

    # elif sent_message == 'admin admin':
    #     if Manager.objects.filter(line_id= user_id).exists():
    #         message = TextSendMessage(text=f'『{user_name}』已經是系統管理員')
    #     else:
    #         mode = 'no'

    #     if sent_message == 'admin admin' and mode == 'no':
    #         message = TextSendMessage(text='please enter your acc')


    else:
        message = TextSendMessage(text=sent_message)



    line_bot_api.reply_message(reply_token, message)



def callback2(request):
    from .alert import clear_tasks_queue
    try:
        clear_tasks_queue()
        # alert_flex_message = alert_FlexMessage(str(instance.id), str(instance.timestamp), str(instance.description))
        result = "OK"
    except Exception:
        result = Exception
    return HttpResponse(result)


urlpatterns = [
    path('test/', callback2),
    path('terminate/', clear_tasks_queue_web_control, name='clear task queue'),
    # path('callback/', callback),
    path('callback/', new_callback),
    ]
