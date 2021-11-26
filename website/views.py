from django.shortcuts import render
from django.http import HttpResponse
from db_api.models import Yolo, Yolo_Files, yolo_trial
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import date



# Create your views here.


def web1(request):

    database = Yolo.objects.all()
    database_image = Yolo_Files.objects.all()
    alert_choice = [
        '無危險行為',
        '存在危險行為',
        '未知',
        ]
    english_alert_choice = [
        'No dangerous behavior',
        'Dangerous behavior exists',
        'Unknown',
        ]
    data = []
    for a in database:
        body=[]
        body.append(a.id)
        body.append(a.title)
        body.append(english_alert_choice[a.alert])
        body.append(a.description)
        body.append(a.created_at)

        data.append(body)


    return render(request, 'web1.html',locals())

#this is the main homepage
@login_required(login_url='login')
def template1(request):
    user = request.user
    username = user.username
    database = Yolo.objects.all()
    database_image = Yolo_Files.objects.all()
    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    english_alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    data = []
    for a in database:
        body=[]
        body.append(a.id)
        body.append(a.title)
        body.append(english_alert_choice[a.alert])
        body.append(a.created_at)

        data.append(body)

    return render(request,'template1.html',locals())

####################################################################################################################


@login_required(login_url='login')
def template2(request):
    today = date.today()
    user = request.user
    username = user.username
    database = Yolo.objects.all()
    database_image = Yolo_Files.objects.all()

    total_alert = Yolo.objects.all().count()
    no_danger = Yolo.objects.filter(alert=0).count()
    unknown = Yolo.objects.filter(alert=4).count()
    total_dangerous = total_alert - no_danger
    total_danagerous_without_unknown = total_alert - no_danger - unknown

    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    data = []
    statistics = []
    # no_danger = 0
    # dangerous_behaviour = 0
    # unknown = 0
    todays_alert = 0
    this_week_alert = 0
    for a in database:
        body=[]
        body.append(a.id)
        body.append(a.title)
        body.append(alert_choice[a.alert])
        # if a.alert == 0:
        #     no_danger +=1
        # elif a.alert == 4:
        #     unknown += 1
        # else:
        #     dangerous_behaviour +=1
        body.append(a.created_at)
        statistics.append(a.created_at)

        data.append(body)
    # total_alert = len(data)
    # total_dangerous = total_alert - no_danger
    for i in statistics:
        if today.day == i.day:
            todays_alert += 1
            this_week_alert +=1
        elif today.day-7 <=  i.day:
            this_week_alert +=1
        else:
            pass


    return render(request,'homepage/index.html',locals())

##########################################################################################################################

#this is for selecting specific objects
@login_required(login_url='login')
def ShowAlertMsgById(request, id='none'):
    website_host = settings.WEB_HOST
    user = request.user
    username = user.username
    if id == 'none':
        output = {'result':'No object Found'}
    elif not Yolo.objects.filter(id = id).exists():
        output = {'result':'No object Found'}
    else:
        obj_yolo = Yolo.objects.get(pk = id)
        #yolo_file.yolo_id.title get parent element from child
        if Yolo_Files.objects.filter(pk=obj_yolo.pk).exists():
            obj_yolofiles = Yolo_Files.objects.get(pk=obj_yolo.pk)
            if obj_yolofiles.image != "":
                url = website_host + str(obj_yolofiles.image.url)
            else:
                url = ''
        else:
            obj_yolofiles = ''
            url = ''

        output = {
            'result' : 'Success',
            'obj_yolo' : obj_yolo,
            'obj_yolofiles' : obj_yolofiles,
            'username' : username,
            'img_url' : url,
            }

    return render(request, 'web2.html', output)

