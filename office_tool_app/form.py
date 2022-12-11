from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from office_tool_app.models import User, Group, Vacation, Messages, Delegation, AddressCore, AddressHome, MedicalLeave


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'pesel', 'email', 'birth_date', 'father_name',
                  'mother_name', 'family_name', 'group', 'position']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['re_password']:
            raise ValidationError('Passwords are not the same!')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'pesel', 'email', 'birth_date', 'father_name',
                  'mother_name', 'family_name', 'group', 'position']


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = '__all__'


class AddressHomeForm(forms.ModelForm):

    class Meta:
        model = AddressHome
        exclude = ('employee',)


class AddressCoreForm(forms.ModelForm):

    class Meta:
        model = AddressCore
        exclude = ('employee',)


class VacationForm(forms.ModelForm):

    class Meta:
        model = Vacation
        exclude = ('employee', 'status',)

    def clean(self):
        cleaned_data = super().clean()
        vacation_from = cleaned_data['vacation_from']
        vacation_to = cleaned_data['vacation_to']
        today = datetime.now().date()
        if vacation_from > vacation_to:
            raise ValidationError("End date can not be earlier then start date!")
        if (vacation_from < today) or (vacation_to < today):
            raise ValidationError("Dates can not be from the past!")


class MessagesForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = '__all__'


class DelegationForm(forms.ModelForm):

    class Meta:
        model = Delegation
        exclude = ('employee', 'status',)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        today = datetime.now().date()
        if start_date > end_date:
            raise ValidationError("End date can not be earlier then start date!")
        if (start_date < today) or (end_date < today):
            raise ValidationError("Dates can not be from the past!")


class MedicalLeaveForm(forms.ModelForm):

    class Meta:
        model = MedicalLeave
        exclude = ('employee',)

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data['from_date']
        to_date = cleaned_data['to_date']
        today = datetime.now().date()
        if from_date > to_date:
            raise ValidationError("End date can not be earlier then start date!")
        if (from_date < today) or (to_date < today):
            raise ValidationError("Dates can not be from the past!")
