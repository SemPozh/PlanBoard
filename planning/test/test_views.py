from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


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


