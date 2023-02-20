from django import forms
from django.forms.widgets import DateInput
from datetime import datetime
from django.core.exceptions import ValidationError
from office_tool_app.models import User, Group, Vacation, Messages, Delegation, AddressCore, AddressHome, MedicalLeave


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    birth_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'pesel', 'email', 'birth_date', 'father_name',
                  'mother_name', 'family_name', 'group', 'position']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['re_password']:
            raise ValidationError('Passwords are not the same!')


class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'pesel', 'email', 'birth_date', 'father_name',
                  'mother_name', 'family_name', 'position']


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name',]


class AddressHomeForm(forms.ModelForm):

    class Meta:
        model = AddressHome
        fields = ['city', 'province', 'country_region', 'postal_code']


class AddressCoreForm(forms.ModelForm):

    class Meta:
        model = AddressCore
        fields = ['city', 'province', 'country_region', 'postal_code']


class VacationForm(forms.ModelForm):
    vacation_from = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    vacation_to = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Vacation
        fields = ['replacement', 'vacation_from', 'vacation_to']

    def clean(self):
        cleaned_data = super().clean()
        vacation_from = cleaned_data.get('vacation_from')
        vacation_to = cleaned_data.get('vacation_to')
        if vacation_from and vacation_to:
            today = datetime.now().date()
            if vacation_from > vacation_to:
                raise ValidationError(
                    "End date can not be earlier then start date!")
            if (vacation_from < today) or (vacation_to < today):
                raise ValidationError("Dates can not be from the past!")


class MessagesForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ['from_employee', 'to_employee', 'message']


class DelegationForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Delegation
        fields = ['start_date', 'end_date', 'delegation_country']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            today = datetime.now().date()
            if start_date > end_date:
                raise ValidationError(
                    "End date can not be earlier then start date!")
            if (start_date < today) or (end_date < today):
                raise ValidationError("Dates can not be from the past!")


class MedicalLeaveForm(forms.ModelForm):
    from_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = MedicalLeave
        fields = ['from_date', 'to_date']

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date:
            today = datetime.now().date()
            if from_date > to_date:
                raise ValidationError(
                    "End date can not be earlier then start date!")
            if (from_date < today) or (to_date < today):
                raise ValidationError("Dates can not be from the past!")
