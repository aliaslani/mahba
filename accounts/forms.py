from django.forms import Form
from django.forms import ModelForm
from accounts.models import CustomUser
from django import forms
from django.forms import ValidationError
from .constants import  COUNTRY_NAME, COUNTRY_CODES
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import MultiValueField, ChoiceField, CharField, MultiWidget
from django_jalali.forms import jDateField


class RegisterForm(Form):
    username = forms.CharField(max_length=50, label='نام کاربری', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=30, label='گذرواژه', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(max_length=30, label='تکرار گذرواژه', widget=forms.PasswordInput(attrs={'class':'form-control'}))


    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #     print(password, confirm_password)
    #     if not password == confirm_password:
    #         raise ValidationError('گذرواژه مطابقت ندارد')
    #     return self.cleaned_data.get('password')
    
    def clean(self):
        data = super().clean()
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not password == confirm_password:
            raise ValidationError('گذرواژه مطابقت ندارد')
        return data

class LoginForm(Form):
    username = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'}))
    password = forms.CharField(max_length=30, label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'گذرواژه'}))
    




class EditProfileForm(forms.ModelForm):
    phone_country_code = forms.ChoiceField(
        choices=COUNTRY_CODES,
                        label=('کشور'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone_local_number = forms.CharField(
        label=('شماره تلفن'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9123456789'})
    )

    class Meta:
        model = CustomUser
        fields = ['phone_country_code', 'phone_local_number', 'gender', 'birthdate', 'profile_picture']
        widgets = {
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('phone_country_code')
        local_number = cleaned_data.get('phone_local_number')

        if country_code and local_number:
            full_number = f"{country_code}{local_number}"
            cleaned_data['phone_number'] = full_number
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        full_phone = self.cleaned_data.get('phone_number')
        if full_phone:
            instance.phone_number = full_phone
        if commit:
            instance.save()
        return instance