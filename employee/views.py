from django.shortcuts import render
from .forms import ProfileForm
from .models import employee
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def profile(request):
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    return render(request, "profile/profile.html", locals())


@login_required
def update_profile(request):
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

    return render(request, 'profile/update_profile.html', locals())


