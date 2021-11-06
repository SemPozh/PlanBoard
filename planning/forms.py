from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    # User register
    username = forms.CharField(label="Ваш логин", widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.EmailField(label="Ваша почта", widget=forms.EmailInput(attrs={'placeholder': 'Почта'}))
    password1 = forms.CharField(label="Ваш пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Почта'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'})
        }


class UserLoginForm(AuthenticationForm):
    # User login
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class ResetPasswordForm(forms.Form):
    # Reset form to send message
    email = forms.EmailField(label="Ваша почта", widget=forms.EmailInput(attrs={'placeholder': 'Почта'}))


class ChangePasswordForm(forms.Form):
    # change password
    password1 = forms.CharField(label="Ваш пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}))


class HelpForm(forms.Form):
    email = forms.EmailField(label="Ваша почта", widget=forms.EmailInput(attrs={'placeholder': 'Почта', 'class': 'email_contact_input'}))
    message = forms.CharField(label="Обратная связь", widget=forms.Textarea(attrs={'placeholder': 'Ваш вопрос', 'class': 'message_contact_input'}))



