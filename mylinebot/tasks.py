from celery import shared_task
import time
import mylinebot

@shared_task(name='Send Alert Message')
def create_task(message):
    for notification_id, message_info in message.items():
        line_id = message_info['lineid']
        alert_id = message_info['alert_id']
        timestamp = message_info['timestamp']
        description = message_info['description']
        repeat_interval = message_info['repeat_interval']

    while True:
        mylinebot.alert.send_alert(line_id, alert_id, timestamp, description, notification_id)
        time.sleep(repeat_interval)
        print(f"pushing messages to <{line_id}>...<{alert_id}>")


@shared_task(name='Send Alert Image')
def create_image_task(message):
    for notification_id, message_info in message.items():
        line_id = message_info['line_id']
        alert_id = message_info['alert_id']
        image_url = message_info['image_url']

        mylinebot.alert.send_alert_picture(line_id, alert_id, image_url)
