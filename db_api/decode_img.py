from .tasks import create_decode_task

def append_task_queue(yolo_object):
    title = str(yolo_object.title)
    image = str(yolo_object.image)

    message = dict()
    message[title] = {'title': title,
                      'image': image,
                    }
    result = create_decode_task.delay(message)
    return result.task_id
