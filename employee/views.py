from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import ProfileForm
from .models import employee, generate_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
##############################################
# Create your views here.


@login_required
def profile(request):
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    return render(request, "profile/profile.html", locals())


@login_required
def update_profile(request):
    line_channel_id = settings.LINE_CHANNEL_ID
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '資料更新成功')
        else:
            messages.warning(request, '請檢查每個欄位是否都有正確填寫')
    else:
        profile_form = ProfileForm(instance=user_profile)

    if user_profile.lineid == employee._meta.get_field(field_name='lineid').get_default():
        new_password = user_profile.password

    return render(request, 'profile/update_profile.html', locals())



@login_required
def update_line_id(request):
    new_password = generate_password()
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    user_profile.password = new_password
    user_profile.lineid = employee._meta.get_field(field_name='lineid').get_default()
    user_profile.line_username = employee._meta.get_field(field_name='line_username').get_default()
    user_profile.save()
    messages.success(request, 'Line ID更新成功')

    return redirect('my_profile_update')


@login_required(login_url="login")
def user_login_line(request):
    line_channel_id = settings.LINE_CHANNEL_ID
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    return redirect(f'https://line.me/R/oaMessage/{line_channel_id}/@{user_profile.gongHao}@{user_profile.password}')
