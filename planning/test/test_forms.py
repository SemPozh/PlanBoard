from django.test import TestCase
from planning.forms import UserRegisterForm, UserLoginForm, ResetPasswordForm, ChangePasswordForm


class UserRegisterFormTest(TestCase):
    def test_register_form_username_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Ваш логин')

    def test_register_form_username_placeholder(self):
        form = UserRegisterForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Логин')

    def test_register_form_email_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Ваша почта')

    def test_register_form_email_placeholder(self):
        form = UserRegisterForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Почта')

    def test_register_form_password1_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['password1'].label is None or form.fields['password1'].label == 'Ваш пароль')

    def test_register_form_password1_placeholder(self):
        form = UserRegisterForm()
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Пароль')

    def test_register_form_password2_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['password2'].label is None or form.fields['password2'].label == 'Подтверждение пароля')

    def test_register_form_password2_placeholder(self):
        form = UserRegisterForm()
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Подтверждение пароля')


class UserLoginFormTest(TestCase):
    def test_login_form_username_label(self):
        form = UserLoginForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Логин')

    def test_login_form_username_placeholder(self):
        form = UserLoginForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Логин')

    def test_login_form_password_label(self):
        form = UserLoginForm()
        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'Пароль')

    def test_login_form_password_placeholder(self):
        form = UserLoginForm()
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Пароль')


class ResetPasswordFormTest(TestCase):
    def test_reset_password_form_email_label(self):
        form = ResetPasswordForm()
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Ваша почта')

    def test_reset_password_form_email_placeholder(self):
        form = ResetPasswordForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Почта')


class ChangePasswordFormTest(TestCase):
    def test_change_password_form_password1_label(self):
        form = ChangePasswordForm()
        self.assertTrue(form.fields['password1'].label is None or form.fields['password1'].label == 'Ваш пароль')

    def test_change_password_form_password1_placeholder(self):
        form = ChangePasswordForm()
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Пароль')

    def test_change_password_form_password2_label(self):
        form = ChangePasswordForm()
        self.assertTrue(form.fields['password2'].label is None or form.fields['password2'].label == 'Подтверждение пароля')

    def test_change_password_form_password2_placeholder(self):
        form = ChangePasswordForm()
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Подтверждение пароля')





