from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form__data'}), required=True)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form__data'}), required=True)
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form__data'}), required=True)
    email = forms.CharField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form__data'}), required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form__data'}), required=True)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form__data'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        error_chars = [',', '.', '<', '>', '{', '}']
        for char in username:
            for sing in error_chars:
                if char == sing:
                    raise forms.ValidationError("Были введены недопустимые символы.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("Пользователь с такой почтой уже существует.")
        return email


class AuthUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form__data'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form__data'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Неверный логин или пароль. Проверьте правильность введенных данных.")
        return self.cleaned_data


class EmailPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form__data'}), required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserPasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form__data'}),
                                required=True)
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput(attrs={'class': 'form__data'}),
                                required=True)

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
