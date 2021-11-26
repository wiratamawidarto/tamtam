from django.conf import settings
from .models import Manager, AlertNotification, AlertImageNotification
from employee.models import employee
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
############################################
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextMessage, TextSendMessage, FlexSendMessage, ImageSendMessage
###########################################
from ai2021mis.celery import app
from celery.result import AsyncResult
from .tasks import create_task, create_image_task
import signal

ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)



# def sendAlert_Picture(alert_id, alert_picture_url):
#     all_objects = employee.objects.all()
#     managers = [object for object in all_objects if object.lineid != 'no']
#     calls = Manager.objects.filter(state='logged in')
#     call = []
#     for i in calls:
#         call.append(str(i.line_id))
#     image_message = ImageSendMessage(
#         original_content_url=str(alert_picture_url),
#         preview_image_url=str(alert_picture_url)
#     )
#     # image_message = {
#     #         "original_content_url" : ,
#     #         "preview_image_url" : 'alert_picture_url'
#     #         }
#     text_message = '這是ID:『' + alert_id + '』的危險信息縮圖'
#     line_bot_api.multicast(call, image_message)
#     line_bot_api.multicast(call, TextSendMessage(text=text_message))


###################################################################
def send_alert_to_managers(Yolo_object):
    all_objects = employee.objects.all()
    managers = [object for object in all_objects if object.lineid != 'no']
    for manager in managers:
        notification = AlertNotification.objects.create(alert_id=Yolo_object, line_user=manager)
        notification.save()


def send_alert_img_to_managers(Yolofile_object):
    all_objects = employee.objects.all()
    managers = [object for object in all_objects if object.lineid != 'no']
    for manager  in managers:
        notification = AlertImageNotification.objects.create(alert_id=Yolofile_object, line_user=manager)
        notification.save()


def send_alert_picture(line_id, alert_id, alert_image_url, notification_id):
    image_message = ImageSendMessage(
        original_content_url=str(alert_image_url),
        preview_image_url=str(alert_image_url)
    )
    text_message = '這是ID:『' + alert_id + '』的危險信息縮圖'
    try:
        line_bot_api.push_message(line_id, image_message)
        line_bot_api.push_message(line_id, TextSendMessage(text=text_message))
        notification = AlertImageNotification.objects.get(pk=notification_id)
        notification.received = True
        notification.timestamp = timezone.now()
        notification.save()
    except Exception as e:
        print(e)


def send_alert(lineid, alert_id, timestamp, description, notification_id):
    message = alert_message(alert_id, timestamp, description, notification_id)
    FlexMessage = FlexSendMessage(alt_text='@工地安全警報', contents=message)
    line_bot_api.push_message(lineid, FlexMessage)


def append_imgtask_queue(notification_object):
    website_host = settings.WEB_HOST

    notification_id = str(notification_object.pk)
    line_id = str(notification_object.line_user.lineid)
    alert_id = str(notification_object.alert_id.id)
    image_url = website_host + str(notification_object.alert_id.image.url)

    message = dict()
    message[notification_id] = {'line_id': line_id,
                                'alert_id': alert_id,
                                'image_url': image_url,
                                }
    result = create_image_task.delay(message)
    return result.task_id


def append_task_queue(notification_object):
    notification_id = str(notification_object.pk)
    line_id = str(notification_object.line_user.lineid)
    alert_id = str(notification_object.alert_id.id)
    timestamp = str(notification_object.alert_id.timestamp)
    description = str(notification_object.alert_id.description)
    repeat_interval = int(30)
    message = dict()
    message[notification_id] = {'lineid': line_id,
                                  'alert_id': alert_id,
                                  'timestamp': timestamp,
                                  'description': description,
                                'repeat_interval': repeat_interval,
                                }
    result = create_task.delay(message)
    return result.task_id


def remove_task_from_queue(task_id):
    result = AsyncResult(task_id)
    if result.state == 'STARTED' or "RETRY" or "PENDING":
        result.revoke(terminate=True, signal=signal.SIGQUIT)
    else:
        result.revoke(terminate=False, signal=signal.SIGQUIT)

@login_required(login_url='login')
def clear_tasks_queue_web_control(request):
    clear_tasks_queue()
    return HttpResponse("All tasks terminated")


def clear_tasks_queue():
    from mylinebot.models import AlertNotification
    all_objects = AlertNotification.objects.all()
    objects_task_id = [object.task_id for object in all_objects]
    for task in objects_task_id:
        remove_task_from_queue(task)
    app.control.purge()


# Create your views here.

def buttons_message():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
            title="是否要進行抽獎活動？",
            text="輸入生日後即獲得抽獎機會",
            actions=[
                DatetimePickerTemplateAction(
                    label="請選擇生日",
                    data="input_birthday",
                    mode='date',
                    initial='1990-01-01',
                    max='2019-03-10',
                    min='1930-01-01'
                ),
                MessageTemplateAction(
                    label="看抽獎品項",
                    text="有哪些抽獎品項呢？"
                ),
                URITemplateAction(
                    label="免費註冊享回饋",
                    uri="https://tw.shop.com/nbts/create-myaccount.xhtml?returnurl=https%3A%2F%2Ftw.shop.com%2F"
                )
            ]
        )
    )
    return message


def message3():
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "image",
                    "url": "https://engineering.linecorp.com/wp-content/uploads/2018/11/linedev_logo-90x90.jpg"
                },
                {
                    "type": "text",
                    "text": "ＶＳ",
                    "gravity": "center",
                    "align": "center",
                    "size": "xxl",
                    "weight": "bold"
                },
                {
                    "type": "image",
                    "url": "https://engineering.linecorp.com/wp-content/uploads/2018/11/linedev_logo-90x90.jpg"
                }
            ]
        },
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "89：101",
                    "align": "center",
                    "gravity": "center",
                    "size": "xxl",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "進場人數： 1000/1200",
                    "gravity": "center",
                    "align": "center",
                    "size": "md",
                    "margin": "md"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "熊大廣場",
                    "weight": "bold",
                    "size": "xl",
                    "gravity": "center",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "2020/01/01 17:00",
                    "align": "center",
                    "size": "md",
                    "margin": "md"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "官方網站",
                        "uri": "https://www.youtube.com/c/LINEDevelopersTaiwan/videos"
                    },
                    "style": "link"
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "分享",
                        "uri": "https://www.facebook.com/LINEDevelopersTW"
                    }
                }
            ],
            "flex": 0
        }
    }


def alert_message(alert_id='(none)', timestamp='(none)', descrption='(none)', notification_id='(none)'):
    website_host = settings.WEB_HOST
    if alert_id != '(none)':
        yolo_info_url = website_host + "/website/detail/" + alert_id + "/"
    else:
        yolo_info_url = website_host + "/website/"

    alert_received_txt = "解除警報" + "@" + alert_id + "@" + notification_id

    message = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "image",
                    "url": "https://cdn.pixabay.com/photo/2012/04/12/22/25/warning-sign-30915__340.png"
                }
            ]
        },
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "危險警告",
                    "align": "center",
                    "gravity": "center",
                    "size": "xxl",
                    "weight": "bold"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "ID",
                            "color": "#aaaaaa",
                            "flex": 2,
                            "size": "md",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": alert_id,
                            "color": "#666666",
                            "size": "md",
                            "flex": 5
                        }
                    ],
                    "spacing": "sm"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "時間",
                            "color": "#aaaaaa",
                            "flex": 2,
                            "size": "md",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": timestamp,
                            "color": "#666666",
                            "size": "md",
                            "flex": 5
                        }
                    ],
                    "spacing": "sm"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "警報內容",
                            "color": "#aaaaaa",
                            "flex": 2,
                            "size": "md",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": descrption,
                            "color": "#666666",
                            "size": "md",
                            "flex": 5,
                            "wrap": True
                        }
                    ],
                    "spacing": "sm"
                }
            ],
            "margin": "lg",
            "spacing": "md"
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "查看",
                        "uri": yolo_info_url
                    },
                    "style": "secondary"
                },
                {
                    "type": "button",

                    "action": {
                        "type": "message",
                        "label": "解除警報",
                        "text": alert_received_txt
                    },
                    "style": "secondary"
                }
            ],
            "flex": 0
        }
    }
    return message
