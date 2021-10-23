from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Field, Template
from django.http import JsonResponse
import json


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


def add_template(request):
    fields = Field.objects.all()
    return render(request, 'planning/add_template.html', context={'fields': fields})


def ajax_add_template(request):
    if request.is_ajax():
        field_id = request.GET['field_id']
        elem_id = request.GET['elem_id']

        field_obj = Field.objects.get(id=field_id)
        if field_obj.title == 'Большое поле':
            input_html = f'<div class="textarea_wrapper">' \
                         f'<label class="input_label" for="name{elem_id}"></label>' \
                         f'<textarea class="{field_obj.input_name.css_class} field_elem" name="name{elem_id}" field_id={field_id}></textarea>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'</div>'
        elif field_obj.title == 'Поле с выбором':
            input_html = f'<div class="select_wrapper">' \
                         f'<label class="input_label" for="name{elem_id}"></label>' \
                         f'<div class="select_wrap">' \
                         f'<select class="{field_obj.input_name.css_class} field_elem" field_id={field_id}>' \
                         f'<option value="Some option" class="select_option">Some option</option>' \
                         f'<option value="Another option" class="select_option">Another option</option>' \
                         f'</select>' \
                         f'</div>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'</div>'
        elif field_obj.input_name.css_class == 'input_radio_css' or  field_obj.input_name.css_class == 'input_checkbox_css':

            input_html = f'<div>'\
                         f'<label class="input_label_for_button" for="name{elem_id}"></label>'\
                         f'<div class="button_input field_elem" field_id={field_id}>'\
                         f'<div class="button_wrap" elem_id={elem_id}>' \
                         f'<label class="{field_obj.input_name.css_class}_label">' \
                         f'<input type={field_obj.input_name.title} class="{field_obj.input_name.css_class}" name="name{elem_id}" value="Some option" checked>' \
                         f'<span class="{field_obj.input_name.css_class}_fake"></span>' \
                         f'<span class="text">Some option</span>' \
                         f'</label>' \
                         f'<label class="{field_obj.input_name.css_class}_label">' \
                         f'<input type={field_obj.input_name.title} class="{field_obj.input_name.css_class}" name="name{elem_id}" value="Another option">' \
                         f'<span class="{field_obj.input_name.css_class}_fake"></span>' \
                         f'<span class="text">Another option</span>' \
                         f'</label>' \
                         f'</div>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'</div>'\
                         f'</div>'

        else:
            input_html = f'<div class="input_wrapper">' \
                         f'<label class="input_label" for="name{elem_id}"></label>' \
                         f'<input type="{field_obj.input_name.title}" class="{field_obj.input_name.css_class} field_elem" name="name{elem_id}" field_id={field_id}>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'</div>'

        data = {
            'input_html': input_html,
            'field_title': field_obj.title,
        }

        return JsonResponse(data)


def ajax_save_input_settings(request):
    if request.is_ajax():
        return JsonResponse({'data': 1})


def ajax_save_template(request):
    if request.is_ajax():
        data = json.loads(request.POST['data'])
        user = request.user
        template_title = data['template_title']
        template_data = data['template_data']

        Template.objects.create(user_id=user.id, title=template_title, fields=template_data)

        return JsonResponse({'data': 1})


def my_plans(request):
    pass
