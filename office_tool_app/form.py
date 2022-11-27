from django import forms
from django.core.exceptions import ValidationError
from office_tool_app.models import CustomUser, Group, Address, Vacation, Messages, Delegation


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'pesel', 'birth_date', 'father_name',
                  'mother_name', 'family_name', 'group', 'position']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['re_password']:
            raise ValidationError('Passwords are not the same!')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'pesel', 'birth_date', 'father_name',
                  'mother_name', 'family_name', 'group', 'position']


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = '__all__'


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'


class VacationForm(forms.ModelForm):

    class Meta:
        model = Vacation
        fields = '__all__'


class MessagesForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = '__all__'


class DelegationForm(forms.ModelForm):

    class Meta:
        model = Delegation
        fields = '__all__'
