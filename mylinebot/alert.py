from django.conf import settings
from .models import Manager
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextMessage, TextSendMessage, FlexSendMessage, ImageSendMessage


ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
website_host = settings.WEB_HOST

def sendAlert(alert_id, timestamp, descrption):
    # with open("/home/christopher0908/ai2021mis/db_api/message.txt", "r") as f:
    #     body = f.read()
    # alert = alert
    # message = body + '@' + alert
    calls = Manager.objects.filter(state = 'logged in')
    call = []
    for i in calls:
        call.append(str(i.line_id))
    message = alert_message(alert_id, timestamp, descrption)
    # alert_flex_message = instance
    line_bot_api.multicast(call, FlexSendMessage(alt_text='@工地安全警報', contents=message))
    # line_bot_api.multicast(call, FlexSendMessage(alt_text='query record: alert', contents=alert_flex_message))


def sendAlert_Picture(alert_id, alert_picture_url):
    calls = Manager.objects.filter(state = 'logged in')
    call = []
    for i in calls:
        call.append(str(i.line_id))
    image_message = ImageSendMessage(
            original_content_url= str(alert_picture_url),
            preview_image_url= str(alert_picture_url)
        )
    # image_message = {
    #         "original_content_url" : ,
    #         "preview_image_url" : 'alert_picture_url'
    #         }
    text_message = '這是ID:『' + alert_id + '』的危險信息縮圖'
    line_bot_api.multicast(call, image_message)
    line_bot_api.multicast(call, TextSendMessage(text = text_message))


    #     alert_flex_message = alert_FlexMessage(str(instance.id), str(instance.timestamp), str(instance.description))
    #     calls = Manager.objects.all()
    #     call = []
    #     for i in calls:
    #         call.append(str(i.line_id))
    #     line_bot_api.multicast(call, FlexSendMessage(alt_text='alert', contents=message2))


# @receiver(post_save, sender=Yolo)
# def create_alert(sender, instance, created, **kwargs):
#     # if created and instance.alert:
#     #     alert_flex_message = alert_FlexMessage(str(instance.id), str(instance.timestamp), str(instance.description))
#     #     sendAlert('YOLO', alert_flex_message)
#     if created:
#         alert_flex_message = alert_FlexMessage(str(instance.id), str(instance.timestamp), str(instance.description))
#         sendAlert('YOLO', alert_flex_message)
#     # elif created:
#     #     alert_flex_message = alert_FlexMessage(str(instance.id), str(instance.timestamp), str(instance.description))
#     #     calls = Manager.objects.all()
#     #     call = []
#     #     for i in calls:
#     #         call.append(str(i.line_id))
#     #     line_bot_api.multicast(call, FlexSendMessage(alt_text='alert', contents=message2))




from django.shortcuts import render
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

def alert_message(alert_id='(none)', timestamp='(none)', descrption='(none)'):

    if alert_id != '(none)':
        yolo_info_url = website_host + "/website/detail/" + alert_id +"/"
    else:
        yolo_info_url = website_host + "/website/"

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
        "style": "link"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "解除警報",
          "uri": yolo_info_url,
          "altUri": {
            "desktop": yolo_info_url
          }
        }
      }
    ],
    "flex": 0
  }
}
    return message
