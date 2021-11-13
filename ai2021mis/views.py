from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect

def LoginPage(request, page=''):

    if request.user.is_authenticated:
        return redirect('homepage')

    else:
        # if request.session.test_cookie_worked():
        #     request.session.delete_test_cookie()
        #     messages.info(request, "cookie supported")
        # else:
        #     messages.info(request, "cookie not supported")
        # request.session.set_test_cookie()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            next_url = request.POST.get("next_url")
            user = authenticate(request,username=username,password=password)


            if user is not None:
                login(request, user)

                if next_url != '' and next_url != "/logout/":
                    response = redirect(next_url)
                else:
                    response = redirect("homepage")

                if request.POST.get('remember_me'):
                    # expires = 'Thu, 28-May-2020 08:53:06 GMT'  # 24小时 格林威治时间
                    # expires = datetime.datetime(2020, 5, 28, 23, 44, 55))
                    expires = 60 * 60 * 24
                    max_age = 60 * 60 * 24
                    response.set_cookie('c_username', username, expires=expires, max_age=max_age)
                    response.set_cookie('c_password', password, expires=expires, max_age=max_age)

                return response

            else:
                messages.warning(request, 'Username or password is incorrect')

        if request.COOKIES.get('c_username'):

            context = {
                'c_username': request.COOKIES['c_username'],
                'c_password': request.COOKIES['c_password'],
                }
        else:
            context = {}

        next_url = request.GET.get("next", '')
        context['next_url'] = next_url
        return render(request, 'login/login.html', context)



def LogOutPage(request):
    logout(request)
    return redirect('homepage')