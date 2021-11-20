from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .models import Manager, AlertNotification
from employee.models import employee
from db_api.models import Yolo

import json
import requests
ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest


        for event in events:
            user_id = event.source.user_id
            headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
            result = requests.get(f'https://api.line.me/v2/bot/profile/{user_id}', headers=headers)
            user_name = json.loads(result.text)['displayName']

            if not Manager.objects.filter(line_id = user_id).exists():
                unit = Manager.objects.create(name=user_name, line_id=user_id)
                unit.save()
                mode = 'no'
            else:
                unit = Manager.objects.get(line_id = user_id)
                mode = unit.state

            if isinstance(event, MessageEvent):
                sent_message = event.message.text
                reply_token = event.reply_token
                # elif sent_message == '@請輸入帳號' and mode=='login':
                #     message = TextSendMessage(text='你已輸入帳號，請輸入密碼:')

                if sent_message == 'admin activate':
                    try:
                        instance = Manager.objects.get(line_id = user_id)
                        message = TextSendMessage(text=f'『{user_name}』已經是系統管理員')
                    except ObjectDoesNotExist:
                        Manager.objects.create(name=user_name, line_id=user_id)
                        message = TextSendMessage(text=f'已添加『{user_name}』為系統管理員')

                    unit.state = 'logged in'
                    unit.save()
                    mode = unit.state

                if mode == 'no':
                    if sent_message == '@管理員登入':
                        message = TextSendMessage(text='請輸入你的帳號和密碼:\n『格式：@你的賬戶@你的密碼』')

                    elif sent_message[:1] == '@' and len(sent_message) > 8:
                        username = 'none'
                        password = 'none'
                        try:
                            flist = sent_message[1:].split("@")
                            username = str(flist[0])
                            password = str(flist[1])
                        except Exception:
                            message = TextSendMessage(text='格式錯誤、請重新輸入\n『格式：@你的賬戶@你的密碼』')

                        if username != 'none' and password != 'none':
                            if not employee.objects.filter(gongHao = username).exists():
                                message = TextSendMessage(text='無此帳號！')

                            else:
                                user = employee.objects.get(gongHao = username)
                                if password != user.password:
                                    message = TextSendMessage(text='密碼錯誤')

                                elif password == user.password and user.lineid == 'no':
                                    user.lineid = user_id
                                    user.save()
                                    message = TextSendMessage(text=f'登入成功，已添加『{user_name}』為系統管理員')

                                    # unit = Manager.objects.get(line_id = user_id)
                                    unit.state = 'logged in'
                                    unit.save()

                                elif password == user.password and user.lineid == user_id:
                                    message = TextSendMessage(text='登入成功')
                                    unit.state = 'logged in'
                                    unit.save()

                                elif password == user.password and user.lineid != user_id:
                                    message = TextSendMessage(text=f'帳戶『{username}；次此帳戶已有人註冊成為管理員，請聯繫系統管理員')
                        # else:
                        #     message = TextSendMessage(text='請重新輸入')

                    else:
                        message = TextSendMessage(text='請先登入系統～')

                #############################################################
                # funtions after user logged in
                elif mode != 'no' and sent_message =='@管理員登入':
                    message = TextSendMessage(text=f'『{user_name}』已經是系統管理員')

                elif sent_message == '@查看':
                    message = TextSendMessage(text='好的請稍候～')
                    try:
                        line_bot_api.push_message(user_id, TextSendMessage(text='好的請稍候'))
                        instances = Yolo.objects.all().filter(alert='1').order_by('-created_at',)
                        count = 0
                        text = '最近的警報:\n'
                        for instance in instances:
                            count = count + 1
                            instance_id = str(instance)
                            instance_date = str(instance.timestamp)
                            instance_description = str(instance.description)
                            text = text + f'\n案件{count}\nid: {instance_id}\n日期: {instance_date}\n說明: {instance_description}\n'
                        text = text + f'\n總共 {count}個警報 \n'
                        message = TextSendMessage(text=text)

                    except Exception:
                        message = TextSendMessage(text=f'{user_name} something wrong')

                elif sent_message == '@管理員登出':
                    try:
                        instance = Manager.objects.get(line_id = user_id)
                        instance.delete()
                        # delete_user = employee.objects.get(lineid = user_id)
                        # delete_user.lineid = 'no'
                        # delete_user.save()
                        message = TextSendMessage(text=f'管理員『{user_name}』，已被移除')

                    except ObjectDoesNotExist:
                        message = TextSendMessage(text = f'『{user_name}』不是管理員')

                elif "解除警報" in sent_message:
                    foo = 'Here is an example string that contains bar.'
                    action, alert_id, notification_id = '(none)', '(none)', '(none)'
                    try:
                        flist = sent_message.split("@")
                        action = str(flist[0])
                        alert_id = str(flist[1])
                        notification_id = str(flist[2])

                    except Exception:
                        message = TextSendMessage(text='解除警報格式錯誤，請聯繫管理員')

                    try:
                        if notification_id != '(none)' and alert_id != '(none)':
                            alert = AlertNotification.objects.get(pk=notification_id)
                            alert.received = True
                            alert.save()
                            message = TextSendMessage(text=f'已解除警報『{alert_id}』')
                    except Exception:
                        message = TextSendMessage(text='解除警報失敗，請聯繫管理員')

                else:
                    message = TextSendMessage(text=sent_message)

                line_bot_api.reply_message(reply_token, message)

        return HttpResponse()

    else:
        HttpResponseBadRequest()
