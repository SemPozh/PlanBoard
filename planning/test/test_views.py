from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test.client import Client
from planning.models import Template, Input, Field, Type, Plan
import json


class IndexViewTest(TestCase):
    # Test index view

    def test_index_view_url_exists(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_url_available_by_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_index_view_uses_correct_template(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'planning/index.html')


class RegisterViewTest(TestCase):
    def test_register_view_url_exists(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

    def test_register_view_url_available_by_name(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_register_view_uses_correct_template(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'planning/register.html')

    def test_register_view_success_redirect(self):
        resp = self.client.post(reverse('register'), {'username': 'user1', 'email': 'user1@mail.ru', 'password1': 'user1-password', 'password2': 'user1-password'})
        self.assertRedirects(resp, reverse('index'))

    def test_register_view_incorrect_email(self):
        resp = self.client.post(reverse('register'),
                                {'username': 'user1', 'email': 'user1', 'password1': 'user1-password',
                                 'password2': 'user1-password'})
        self.assertFormError(resp, 'form', 'email', 'Введите правильный адрес электронной почты.')


class LoginViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='user1', email='user1@mail.ru', password='user1-password')
        self.test_user.save()

    def test_login_view_url_exists(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_login_view_url_available_by_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view_uses_correct_template(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'planning/login.html')

    def test_login_view_success_redirect(self):
        resp = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1-password'})
        self.assertRedirects(resp, reverse('index'))


class ResetPasswordViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='user1', email='user1@mail.ru', password='user1-password')
        self.test_user.save()

    def test_reset_password_view_url_exists(self):
        resp = self.client.get('/reset-password/')
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_view_url_available_by_name(self):
        resp = self.client.get(reverse('reset_password'))
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_view_uses_correct_template(self):
        resp = self.client.get(reverse('reset_password'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'planning/reset_password.html')

    def test_reset_password_view_success_redirect(self):
        resp = self.client.post(reverse('reset_password'), {'email': 'user1@mail.ru'})
        self.assertRedirects(resp, reverse('info'))


class InfoViewTest(TestCase):
    def test_info_view_url_exists(self):
        resp = self.client.get('/info/')
        self.assertEqual(resp.status_code, 200)

    def test_info_view_url_available_by_name(self):
        resp = self.client.get(reverse('info'))
        self.assertEqual(resp.status_code, 200)

    def test_info_view_uses_correct_template(self):
        resp = self.client.get(reverse('info'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'planning/info.html')


class ChangePasswordViewTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(id=2, username='user1', email='user1@mail.ru', password='user1-password')
        test_user.save()

    def test_change_password_view_url_exists(self):
        resp = self.client.get('/change-password/c81e728d9d4c2f636f067f89cc14862c/')
        self.assertEqual(resp.status_code, 200)

    def test_change_password_view_url_available_by_name(self):
        resp = self.client.get(reverse('change_password', kwargs={'id_hash': 'c81e728d9d4c2f636f067f89cc14862c'}))
        self.assertEqual(resp.status_code, 200)

    def test_change_password_view_uses_correct_template(self):
        resp = self.client.get(reverse('change_password', kwargs={'id_hash': 'c81e728d9d4c2f636f067f89cc14862c'}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'planning/change_password.html')

    def test_change_password_view_success(self):
        resp = self.client.post(reverse('change_password', kwargs={'id_hash': 'c81e728d9d4c2f636f067f89cc14862c'}), {'password1': 'user1-pwd', 'password2': 'user1-pwd'})
        self.assertRedirects(resp, reverse('index'))


class MyPlansViewTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(id=2, username='user1', email='user1@mail.ru', password='user1-password')
        def_template_data = {"data": [{"attrs": {"label": "ФИО", "height": "",
                                                 "options": ["Some option", "Another option"], "maxvalue": "",
                                                 "minvalue": "", "maxlength": "", "canBeBlank": "0",
                                                 "default_value": "Unnamed"}, "elem_id": 1, "field_id": "1"}, {
                                          "attrs": {"label": "День рождения", "height": "",
                                                    "options": ["Some option", "Another option"], "maxvalue": "",
                                                    "minvalue": "", "maxlength": "", "canBeBlank": "1",
                                                    "default_value": ""}, "elem_id": 2, "field_id": "7"}]}
        template_title = 'Дни рождения'
        Template.objects.create(id=1, user=test_user, title=template_title, fields=def_template_data)
        test_user.save()
        Input.objects.create(id=1, title="text", css_class='input_text_css')
        Input.objects.create(id=2, title="date", css_class='input_date_css')
        Type.objects.create(id=1, title="string")
        Type.objects.create(id=4, title="date")
        Field.objects.create(id=1, title="Обычное поле", type_of_data_id=1, input_name_id=1)
        Field.objects.create(id=7, title="Поле даты", type_of_data_id=4, input_name_id=2)
        test_plan = Plan.objects.create(id=1, user=test_user, template_id=1, data={"plan_data": {"field1": "Unnamed2", "field2": "2021-11-07"}})

    def test_my_plans_view_url_exists(self):
        resp = self.client.get('/my-plans/')
        self.assertEqual(resp.status_code, 302)

    def test_my_plans_view_url_available_and_redirect_by_name(self):
        resp = self.client.get(reverse('my-plans'))
        self.assertRedirects(resp, '/login/')

    def test_my_plans_view_url_available_and_works_by_name(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('my-plans'))
        self.assertEqual(resp.status_code, 200)

    def test_my_plans_view_uses_correct_template(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('my-plans'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'planning/my_plans.html')

    def test_my_plans_view_user_templates(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('my-plans'))
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.context['templates']), 1)

    def test_my_plans_view_user_plans(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('my-plans'))
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.context['user_plans']), 1)

    def test_my_plans_add_plan_view(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('ajax_add_plan'), {'template_id': '1'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(resp.content != '')

    def test_my_plans_add_plan_view_only_ajax_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('ajax_add_plan'), {'template_id': '1'})
        self.assertEqual(resp.status_code, 404)

    def test_my_plans_create_plan_view(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post(reverse('ajax_create_plan'), {'data': ['{"plan_data":{"field1":"Пожарский Семён Андреевич","field2":"2005-10-05"}}'], 'template_id': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(resp.content != '')

    def test_my_plans_create_plan_view_only_ajax_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post(reverse('ajax_add_plan'), {'data': ['{"plan_data":{"field1":"Пожарский Семён Андреевич","field2":"2005-10-05"}}'], 'template_id': 1})
        self.assertEqual(resp.status_code, 404)

    def test_my_plans_api_get_plans_by_template_id_response(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('api_get_plans_by_template_id'), {'template_id': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(resp.content != '' and resp.content != {})

    def test_my_plans_api_get_plans_by_template_id_404(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('api_get_plans_by_template_id'), {'template_id': 1})
        self.assertEqual(resp.status_code, 404)

    def test_my_plans_api_get_plan_data_response(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('api_get_plan_data'), {'plan_id': '1'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(resp.content != '' and resp.content != {})

    def test_my_plans_redact_plan_404(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('ajax_redact_plan'), {'plan_id': 1, 'data':{"plan_data": {"field1": "Unnamed2", "field2": "2021-11-07"}}})
        self.assertEqual(resp.status_code, 404)

    def test_my_plans_redact_plan_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post(reverse('ajax_redact_plan'), {'data': '{"plan_data":{"field1":"test","field2":"2021-11-02"}}', 'plan_id': '1'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTrue(resp.content != '')
        new_plan = Plan.objects.get(id=1)
        self.assertEqual(new_plan.data, {"plan_data":{"field1":"test","field2":"2021-11-02"}})

    def test_my_plans_delete_plan_404(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('ajax_delete_plan'), {'plan_id': 1})
        self.assertEqual(resp.status_code, 404)

    def test_my_plans_delete_plan_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post(reverse('ajax_delete_plan'), {'plan_id': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        try:
            plans = Plan.objects.get(id=1)
            exists = True
        except:
            exists = False
        self.assertFalse(exists)
        self.assertEqual(json.loads(resp.content), {'data': 'success'})


class HelpPageViewTest(TestCase):
    def setUp(self):
        pass

    def test_help_url_avail(self):
        resp = self.client.get('/help/')
        self.assertEqual(resp.status_code, 200)

    def test_help_reverse_url_avail(self):
        resp = self.client.get(reverse('help'))
        self.assertEqual(resp.status_code, 200)

    def test_help_page_uses_correct_template(self):
        resp = self.client.get(reverse('help'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'planning/help.html')

    def test_help_page_redirect(self):
        resp = self.client.post(reverse('help'), {'email': 'SomeEmail@mail.ru', 'message': 'Some message'})
        self.assertRedirects(resp, reverse('index'))


class AddTemplateTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(id=2, username='user1', email='user1@mail.ru', password='user1-password')
        def_template_data = {"data": [{"attrs": {"label": "ФИО", "height": "",
                                                 "options": ["Some option", "Another option"], "maxvalue": "",
                                                 "minvalue": "", "maxlength": "", "canBeBlank": "0",
                                                 "default_value": "Unnamed"}, "elem_id": 1, "field_id": "1"}, {
                                          "attrs": {"label": "День рождения", "height": "",
                                                    "options": ["Some option", "Another option"], "maxvalue": "",
                                                    "minvalue": "", "maxlength": "", "canBeBlank": "1",
                                                    "default_value": ""}, "elem_id": 2, "field_id": "7"}]}
        template_title = 'Дни рождения'
        Template.objects.create(id=1, user=test_user, title=template_title, fields=def_template_data)
        test_user.save()

        Input.objects.create(id=1, title="text", css_class='input_text_css')
        Input.objects.create(id=2, title="date", css_class='input_date_css')
        Input.objects.create(id=3, title="checkbox", css_class='input_checkbox_css')
        Input.objects.create(id=4, title="number", css_class='input_number_css')
        Input.objects.create(id=5, title="radio", css_class='input_radio_css')
        Input.objects.create(id=6, title="range", css_class='input_range_css')
        Input.objects.create(id=7, title="email", css_class='input_email_css')
        Type.objects.create(id=1, title="string")
        Type.objects.create(id=2, title="integer")
        Type.objects.create(id=3, title="list")
        Type.objects.create(id=4, title="date")
        Field.objects.create(id=1, title="Обычное поле", type_of_data_id=1, input_name_id=1)
        Field.objects.create(id=2, title="Большое поле", type_of_data_id=1, input_name_id=1)
        Field.objects.create(id=3, title="Числовое поле", type_of_data_id=2, input_name_id=4)
        Field.objects.create(id=4, title="Одиночный выбор", type_of_data_id=1, input_name_id=5)
        Field.objects.create(id=5, title="Множественный выбор", type_of_data_id=3, input_name_id=3)
        Field.objects.create(id=6, title="Поле с выбором", type_of_data_id=3, input_name_id=1)
        Field.objects.create(id=8, title="Поле для почты", type_of_data_id=1, input_name_id=7)
        Field.objects.create(id=9, title="Ползунок", type_of_data_id=2, input_name_id=6)
        Field.objects.create(id=7, title="Поле даты", type_of_data_id=4, input_name_id=2)

    def test_add_template_avail_by_url(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get('/my-plans/add-template/')
        self.assertEqual(resp.status_code, 200)

    def test_add_template_avail_by_reverse_url(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('add_template'))
        self.assertEqual(resp.status_code, 200)

    def test_add_template_redirect_for_undefined_user(self):
        resp = self.client.get(reverse('add_template'))
        self.assertRedirects(resp, reverse('login'))

    def test_redact_template_avail_by_url(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get('/my-plans/redact-template/1')
        self.assertEqual(resp.status_code, 200)

    def test_redact_template_redirect_for_undefined_user(self):
        resp = self.client.get('/my-plans/redact-template/1')
        self.assertRedirects(resp, reverse('login'))

    def test_api_get_template_data_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('api_get_template_data'), {'template_id': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.content)

    def test_api_get_template_data_404(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get('/api_get_template_data/', {'template_id': 1})
        self.assertEqual(resp.status_code, 404)

    def test_delete_template_404(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post('/ajax_delete_template/', {'template_id': 1})
        self.assertEqual(resp.status_code, 404)

    def test_delete_template_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post('/ajax_delete_template/', {'template_id': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(resp.status_code, 200)

    def test_save_template_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post(reverse('ajax_save_template'), {'data': ['{"template_data":{"data":[{"elem_id":1,"field_id":"1","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}},{"elem_id":2,"field_id":"1","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}},{"elem_id":3,"field_id":"1","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}}]},"template_title":"Some title"}'], 'template_title': ['Some title']}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(json.loads(resp.content), {'data': 1})

    def test_save_template_404(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.post(reverse('ajax_save_template'), {'data': ['{"template_data":{"data":[{"elem_id":1,"field_id":"1","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}},{"elem_id":2,"field_id":"1","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}},{"elem_id":3,"field_id":"1","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}}]},"template_title":"Some title"}'], 'template_title': ['Some title']})
        self.assertEqual(resp.status_code, 404)

    def test_ajax_redact_template_working(self):
        login = self.client.login(username='user1', password='user1-password')
        data = '{"template_data":{"data":[{"attrs":{"label":"","height":"","options":["Some option","Another option"],"maxvalue":"","minvalue":"","maxlength":"","canBeBlank":"0","default_value":""},"elem_id":1,"field_id":"1"},{"elem_id":2,"field_id":"2","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}}]},"template_title":"Some title"}'
        template_id = 1
        resp = self.client.post(reverse('ajax_redact_template'), {'data':data, 'template_id': template_id}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), {'data': []})

    def test_ajax_redact_template_404(self):
        login = self.client.login(username='user1', password='user1-password')
        data = '{"template_data":{"data":[{"attrs":{"label":"","height":"","options":["Some option","Another option"],"maxvalue":"","minvalue":"","maxlength":"","canBeBlank":"0","default_value":""},"elem_id":1,"field_id":"1"},{"elem_id":2,"field_id":"2","attrs":{"label":"","default_value":"","maxlength":"","maxvalue":"","minvalue":"","canBeBlank":"0","height":"","options":["Some option","Another option"]}}]},"template_title":"Some title"}'
        template_id = 1
        resp = self.client.post(reverse('ajax_redact_template'), {'data':data, 'template_id': template_id})
        self.assertEqual(resp.status_code, 404)

    def test_ajax_add_template_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('ajax_add_template'), {'field_id': 1, 'elem_id': 1}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(resp.status_code, 200)

    def test_ajax_add_template_response_working(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('ajax_add_template'), {'field_id': 1, 'elem_id': 1},
                               **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        input_html = f'<div class="input_wrapper">' \
                     f'<label class="input_label" for="name1"></label>' \
                     f'<input type="text" class="input_text_css field_elem" name="name1" field_id=1>' \
                     f'<a href="#popup1" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id=1></i></a>' \
                     f'<i class="fas fa-trash delete_input" elem_id=1 field_id=1></i>' \
                     f'</div>'
        self.assertEqual(json.loads(resp.content)['input_html'], input_html)


    def test_ajax_add_template_404(self):
        login = self.client.login(username='user1', password='user1-password')
        resp = self.client.get(reverse('ajax_add_template'), {'field_id': 1, 'elem_id': 1})
        self.assertEqual(resp.status_code, 404)
















