from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Field, Template, Plan
from django.http import JsonResponse
import json
from datetime import datetime
from django.http import HttpResponseNotFound
import numpy as np



def index(request):
    # index page
    return render(request, 'planning/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # create and login new user
            user = form.save()
            # Create default template!!!
            def_template_data = {"data": [{"attrs": {"label": "ФИО", "height": "",
                                                     "options": ["Some option", "Another option"], "maxvalue": "",
                                                     "minvalue": "", "maxlength": "", "canBeBlank": "0",
                                                     "default_value": "Unnamed"}, "elem_id": 1, "field_id": "1"},{
                                              "attrs": {"label": "День рождения", "height": "",
                                                        "options": ["Some option", "Another option"], "maxvalue": "",
                                                        "minvalue": "", "maxlength": "", "canBeBlank": "1",
                                                        "default_value": ""}, "elem_id": 2, "field_id": "7"}]}
            template_title = 'Дни рождения'
            Template.objects.create(user=user, title=template_title, fields=def_template_data)

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
    if request.user.is_authenticated:
        fields = Field.objects.all()
        template_title = 'Untitled'
        return render(request, 'planning/add_template.html', context={'fields': fields, 'template_title': template_title})
    else:
        return redirect('login')


def api_get_template_data(request):
    if request.is_ajax():
        template_id = request.GET.get('template_id')
        template = Template.objects.get(id=template_id)
        template_data = template.fields
        return JsonResponse(template_data)
    else:
        return HttpResponseNotFound('Page Not Found')


def ajax_redact_template(request):
    if request.is_ajax():
        template_data = json.loads(request.POST['data'])['template_data']
        title = json.loads(request.POST['data'])['template_title']
        template_id = request.POST['template_id']
        template = Template.objects.get(id=template_id)
        template.title = title
        template.fields = template_data
        template.save()
        return JsonResponse({'data': []})
    else:
        return HttpResponseNotFound('Page Not Found')


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
                         f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field_id}></i>'\
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
                         f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field_id}></i>'\
                         f'</div>'
        elif field_obj.input_name.css_class == 'input_radio_css' or field_obj.input_name.css_class == 'input_checkbox_css':

            input_html = f'<div>' \
                         f'<label class="input_label_for_button" for="name{elem_id}"></label>' \
                         f'<div class="button_input field_elem" field_id={field_id}>' \
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
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>'\
                         f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field_id}></i>'\
                         f'</div>' \
                         f'</div>'

        else:
            input_html = f'<div class="input_wrapper">' \
                         f'<label class="input_label" for="name{elem_id}"></label>' \
                         f'<input type="{field_obj.input_name.title}" class="{field_obj.input_name.css_class} field_elem" name="name{elem_id}" field_id={field_id}>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field_id}></i>'\
                         f'</div>'

        data = {
            'input_html': input_html,
            'field_title': field_obj.title,
        }

        return JsonResponse(data)
    else:
        return HttpResponseNotFound('Page Not Found')


def ajax_save_input_settings(request):
    if request.is_ajax():
        return JsonResponse({'data': 1})
    else:
        return HttpResponseNotFound('Page Not Found')


def ajax_save_template(request):
    if request.is_ajax():
        data = json.loads(request.POST['data'])
        user = request.user
        template_title = data['template_title']
        template_data = data['template_data']

        Template.objects.create(user_id=user.id, title=template_title, fields=template_data)

        return JsonResponse({'data': 1})
    else:
        return HttpResponseNotFound('Page not found')


def redact_template(request, template_id):
    if request.user.is_authenticated:
        template = Template.objects.get(id=template_id)
        data = template.fields
        fields = Field.objects.all()
        template_title = template.title

        return render(request, 'planning/add_template.html', context={'fields': fields, 'data': data, 'template_id': template_id, 'template_title': template_title})
    else:
        return redirect('login')


def ajax_delete_template(request):
    if request.is_ajax():
        template_id = request.POST.get('template_id')

        template = Template.objects.get(id=template_id)
        template.delete()

        return JsonResponse({'data': 1})
    else:
        return HttpResponseNotFound('Page not found')


# My plans
def my_plans(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_templates = Template.objects.filter(user_id=user_id)
        user_plans = Plan.objects.filter(user_id=user_id)

        return render(request, 'planning/my_plans.html',
                      # context={'templates': user_templates, 'first_template': user_templates[0].id, 'user_plans': user_plans}
                      context={'templates': user_templates, 'user_plans': user_plans})
    else:
        return redirect('login')


def ajax_add_plan(request):
    if request.is_ajax():
        template_id = request.GET.get('template_id')
        template_data = Template.objects.get(id=template_id)
        fields = template_data.fields['data']
        fields_html = []
        for field in fields:
            elem_id = field['elem_id']
            field_object = Field.objects.get(id=field['field_id'])
            if str(field['field_id']) in ['1', '3', '7', '8', '9']:
                if str(field['field_id']) == '7':
                    try:
                        field['attrs']['default_value'] = datetime.strptime(field['attrs']['default_value'],
                                                                            '%d.%m.%Y').strftime('%Y-%m-%d')
                    except:
                        pass

                if str(field['attrs']['canBeBlank']) == '0':
                    is_required = 'required'
                else:
                    is_required = ''

                field_html = f'<div class="input_wrapper" field_id={field["field_id"]}>' \
                             f'<label class="input_label working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<input type="{field_object.input_name.title}" class="{field_object.input_name.css_class} field_elem working" field_id={field["field_id"]} name="name{elem_id}" style="height:{field["attrs"]["height"]}px" max="{field["attrs"]["maxvalue"]}" min="{field["attrs"]["minvalue"]}" maxlength="{field["attrs"]["maxlength"]}" value="{field["attrs"]["default_value"]}" {is_required}>' \
                             f'</div>'
            elif str(field['field_id']) == '2':
                if str(field['attrs']['canBeBlank']) == '0':
                    is_required = 'required'
                else:
                    is_required = ''
                field_html = f'<div class="textarea_wrapper" field_id={field["field_id"]}>' \
                             f'<label class="input_label working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<textarea class="{field_object.input_name.css_class} field_elem working" name="name{elem_id}" field_id={field["field_id"]} style="height:{field["attrs"]["height"]}px" maxlength="{field["attrs"]["maxlength"]}" {is_required}>{field["attrs"]["default_value"]}</textarea>' \
                             f'</div>'
            elif str(field['field_id']) in ['4', '5']:

                if str(field['attrs']['canBeBlank']) == '0':
                    is_required = 'required'
                else:
                    is_required = ''

                all_options = ''
                for option in field['attrs']['options']:
                    if option == field['attrs']['default_value']:
                        is_checked = 'checked'
                    else:
                        is_checked = ''
                    all_options = all_options + f'<label class="{field_object.input_name.css_class}_label">' \
                                                f'<input type={field_object.input_name.title} class="{field_object.input_name.css_class} working" name="name{elem_id}" value="{option}" {is_checked}>' \
                                                f'<span class="{field_object.input_name.css_class}_fake"></span>' \
                                                f'<span class="text">{option}</span>' \
                                                f'</label>'
                field_html = f'<div field_id={field["field_id"]}>' \
                             f'<label class="input_label_for_button working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<div class="button_input field_elem" field_id={field["field_id"]}>' \
                             f'<div class="button_wrap" elem_id={elem_id}>' \
                             f'{all_options}' \
                             f'</div>' \
                             f'</div>' \
                             f'</div>'
            elif str(field['field_id']) == '6':
                all_options = ''
                for option in field['attrs']['options']:
                    if option == field['attrs']['default_value']:
                        is_selected = 'selected'
                    else:
                        is_selected = ''
                    all_options = all_options + f'<option value="{option}" class="select_option" {is_selected}>{option}</option>'
                field_html = f'<div class="select_wrapper" field_id={field["field_id"]} style="height:{field["attrs"]["height"]}px">' \
                             f'<label class="input_label working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<div class="select_wrap working">' \
                             f'<select class="{field_object.input_name.css_class} field_elem" field_id={field["field_id"]}>' \
                             f'{all_options}' \
                             f'</select>' \
                             f'</div>' \
                             f'</div>'
            else:
                field_html = ''

            fields_html.append(field_html)

        return JsonResponse({'data': fields_html})
    else:
        return HttpResponseNotFound('Page Not Found')


def ajax_create_plan(request):
    if request.is_ajax():
        user_id = request.user.id
        data = json.loads(request.POST.get('data'))
        template_id = json.loads(request.POST.get('template_id'))

        plan_obj = Plan.objects.create(user_id=user_id, template_id=template_id, data=data)
        plan = plan_obj.data
        count = Plan.objects.filter(template_id=template_id).count()
        return JsonResponse({'plan': plan, 'count': count, 'plan_id': plan_obj.id})
    else:
        return HttpResponseNotFound('Page Not Found')


def api_get_plans_by_template_id(request):
    if request.is_ajax():
        template_id = request.GET.get('template_id')
        fields = Template.objects.get(id=template_id).fields
        plans = Plan.objects.filter(template_id=template_id)
        data = []
        for plan in plans:
            data.append([plan.id, plan.data])
        return JsonResponse({'data': data, 'fields': fields})
    else:
        return HttpResponseNotFound('Page Not Found')


def api_get_plan_data(request):
    if request.is_ajax():
        plan_id = request.GET.get('plan_id')
        plan_obj = Plan.objects.get(id=plan_id)
        plan_data = plan_obj.data["plan_data"]
        template = plan_obj.template
        fields = template.fields['data']
        fields_html = []
        for field in fields:
            elem_id = field['elem_id']
            field_object = Field.objects.get(id=field['field_id'])
            if str(field['field_id']) in ['1', '3', '7', '8', '9']:
                if str(field['field_id']) == '7':
                    try:
                        field['attrs']['default_value'] = datetime.strptime(field['attrs']['default_value'],
                                                                            '%d.%m.%Y').strftime('%Y-%m-%d')
                    except:
                        pass

                if str(field['attrs']['canBeBlank']) == '0':
                    is_required = 'required'
                else:
                    is_required = ''

                field_html = f'<div class="input_wrapper" field_id={field["field_id"]}>' \
                             f'<label class="input_label working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<input type="{field_object.input_name.title}" class="{field_object.input_name.css_class} field_elem working" field_id={field["field_id"]} name="name{elem_id}" style="height:{field["attrs"]["height"]}px" max="{field["attrs"]["maxvalue"]}" min="{field["attrs"]["minvalue"]}" maxlength="{field["attrs"]["maxlength"]}" value="{plan_data["field" + str(elem_id)]}" {is_required}>' \
                             f'</div>'
            elif str(field['field_id']) == '2':
                if str(field['attrs']['canBeBlank']) == '0':
                    is_required = 'required'
                else:
                    is_required = ''
                field_html = f'<div class="textarea_wrapper" field_id={field["field_id"]}>' \
                             f'<label class="input_label working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<textarea class="{field_object.input_name.css_class} field_elem working" name="name{elem_id}" field_id={field["field_id"]} style="height:{field["attrs"]["height"]}px" maxlength="{field["attrs"]["maxlength"]}" {is_required}>{plan_data["field" + str(elem_id)]}</textarea>' \
                             f'</div>'
            elif str(field['field_id']) in ['4', '5']:

                if str(field['attrs']['canBeBlank']) == '0':
                    is_required = 'required'
                else:
                    is_required = ''

                all_options = ''
                for option in field['attrs']['options']:
                    if option == plan_data['field' + elem_id] or option in plan_data['field' + elem_id]:
                        is_checked = 'checked'
                    else:
                        is_checked = ''
                    all_options = all_options + f'<label class="{field_object.input_name.css_class}_label">' \
                                                f'<input type={field_object.input_name.title} class="{field_object.input_name.css_class} working" name="name{elem_id}" value="{option}" {is_checked}>' \
                                                f'<span class="{field_object.input_name.css_class}_fake"></span>' \
                                                f'<span class="text">{option}</span>' \
                                                f'</label>'
                field_html = f'<div field_id={field["field_id"]}>' \
                             f'<label class="input_label_for_button working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<div class="button_input field_elem" field_id={field["field_id"]}>' \
                             f'<div class="button_wrap" elem_id={elem_id}>' \
                             f'{all_options}' \
                             f'</div>' \
                             f'</div>' \
                             f'</div>'
            elif str(field['field_id']) == '6':
                all_options = ''
                for option in field['attrs']['options']:
                    if option == plan_data['field' + str(elem_id)]:
                        is_selected = 'selected'
                    else:
                        is_selected = ''
                    all_options = all_options + f'<option value="{option}" class="select_option" {is_selected}>{option}</option>'
                field_html = f'<div class="select_wrapper" field_id={field["field_id"]} style="height:{field["attrs"]["height"]}px">' \
                             f'<label class="input_label working" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                             f'<div class="select_wrap working">' \
                             f'<select class="{field_object.input_name.css_class} field_elem" field_id={field["field_id"]}>' \
                             f'{all_options}' \
                             f'</select>' \
                             f'</div>' \
                             f'</div>'
            else:
                field_html = ''

            fields_html.append(field_html)
        return JsonResponse({'plan_data': plan_data, 'fields_html': fields_html})
    else:
        return HttpResponseNotFound('Page Not Found')


def ajax_redact_plan(request):
    if request.is_ajax():
        plan_id = request.POST.get('plan_id')
        plan = Plan.objects.get(id=plan_id)
        plan.data = json.loads(request.POST.get('data'))
        plan.save()
        return JsonResponse({'data': plan.data})
    else:
        return HttpResponseNotFound('Page Not Found')


def ajax_delete_plan(request):
    if request.is_ajax():
        plan_id = request.POST.get('plan_id')
        plan = Plan.objects.get(id=plan_id)
        plan.delete()

        return JsonResponse({'data': 'success'})
    else:
        return HttpResponseNotFound('Page Not Found')


def help_page(request):
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            final_message = message + f'\n From: {email}'

            send_mail('Questions and wishes', final_message, 'SemPozh@mail.ru', ['SemPozh@mail.ru'], fail_silently=True)
            messages.success(request, 'Ваше письмо успешно отправлено!')
            return redirect('index')
    else:
        form = HelpForm()
    return render(request, 'planning/help.html', {'form': form})
