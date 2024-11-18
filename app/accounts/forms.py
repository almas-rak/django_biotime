from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Логин"}),
        label='')
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Пароль"}),
        label=""
    )


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Старый пароль"}),
        label=""
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Новый пароль"}),
        label=""
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Потверждение нового пароля"}),
        label=""
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise forms.ValidationError("Новый пароль и его подтверждение не совпадают.")
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Имя пользователя"}),
        label=""
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Новый пароль"}),
        label=""
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Потверждение пароля"}),
        label=""
    )
