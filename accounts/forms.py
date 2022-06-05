import pytz

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.forms import (
    AuthenticationForm, ReadOnlyPasswordHashField, PasswordResetForm, 
    SetPasswordForm
)


User = get_user_model()

COUNTRY_CHOICES = tuple([(country, country) for country in pytz.common_timezones])


class UserCreationForm(forms.ModelForm):
    country = forms.ChoiceField(label='TimeZone', choices=COUNTRY_CHOICES)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'country')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = str(field.label) + '*'
            field.widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        at_position = email.find('@') + 1
        email = email[:at_position] + email[at_position:].lower()
        User.objects.filter(email=email, is_active=False).delete()
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('passwords do not match')

    def save(self, commit=False):
        user = super().save(commit=False)
        user.is_active = False
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='Remember Me', required=False)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['remember'].widget.attrs['class'] = 'form-remember'
        self.fields['username'].widget.attrs['placeholder'] = str(self.fields['username'].label) + '*'
        self.fields['password'].widget.attrs['placeholder'] = str(self.fields['password'].label) + '*'


class UserPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        

class UserSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



# Useredit Form (Admin Page)
class UserChangeForm(forms.ModelForm):
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    create_at = forms.DateTimeField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    password = ReadOnlyPasswordHashField()

    class Meta:
        models = User
        fields = ('email', 'password', 'country', 'is_staff', 'is_active', 'is_superuser', 'create_at', 'update_at')

    def clean_password(self):
        return self.initial['password']


class UserEditForm(forms.ModelForm):
    country = forms.ChoiceField(label='TimeZone', choices=COUNTRY_CHOICES)

    class Meta:
        model = User
        fields = ('email', 'country')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = str(field.label) + '*'
            field.widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        at_position = email.find('@') + 1
        email = email[:at_position] + email[at_position:].lower()
        User.objects.filter(email=email, is_active=False).delete()
        return email

