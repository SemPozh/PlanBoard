from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def index(request):
    # index page
    return render(request, 'planning/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # create and login new user
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные или напишите в службу поддержки.')
    else:
        form = UserRegisterForm()

    return render(request, 'planning/register.html', context={'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # find user and login
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка входа, проверьте введённые данные.')
    else:
        form = UserLoginForm()

    return render(request, 'planning/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'planning/index.html')


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # getting email
            email = form.cleaned_data['email']
            try:
                # find user by email and hash his id
                user = User.objects.get(email=email)
                user_hash = hashlib.md5(str(user.id).encode('utf-8')).hexdigest()

                # sending email with link like /change_password/hash_id
                message_text = 'Здравствуйте, вы оставили заявку на смену пароля на сайте plan-board.ru.\n' \
                               'Перейдите по ссылку ниже, чтобы сменить пароль.\n' \
                               'http://127.0.0.1:8000/change-password/' + user_hash
                send_mail('HELLO', message_text, 'SemPozh@mail.ru', ['SemPozh@mail.ru'], fail_silently=True)

                return redirect('info')
            except:
                messages.error(request, 'Пользователя с такой почтой не существует!')

    else:
        form = ResetPasswordForm()

    return render(request, 'planning/reset_password.html', context={'form': form})


def info(request):
    # info about message page
    return render(request, 'planning/info.html')


def change_password(request, id_hash):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user_obj = False
            # find user by id_hash
            for user in User.objects.all():
                if hashlib.md5(str(user.id).encode('utf-8')).hexdigest() == id_hash:
                    user_obj = user
                    break

            # if user with such id_hash exists
            if user_obj is not False:
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 == password2:
                    # change pwd
                    new_password = form.cleaned_data['password1']
                    user_obj.password = make_password(new_password)
                    user_obj.save()
                    messages.success(request, 'Пароль успешно изменён!')
                    return redirect('index')
                else:
                    messages.error(request, 'Ошибка. Пароль не изменён. Введённые вам пароли не совпадают!')
            else:
                messages.error(request, 'Ошибка смены пароля. Неверная ссылка.')
        else:
            messages.error(request, 'Ошибка. Форма не валидна! Проверьте данные.')
    else:
        form = ChangePasswordForm()

    return render(request, 'planning/change_password.html', context={'form': form})
