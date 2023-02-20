from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    pesel = models.BigIntegerField(null=True, validators=[MinValueValidator(10000000000), MaxValueValidator(99999999999)])
    birth_date = models.DateField(null=True)
    father_name = models.CharField(max_length=128, null=True)
    mother_name = models.CharField(max_length=128, null=True)
    family_name = models.CharField(max_length=128, null=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length=128, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        permissions = [('can_manage_employees', 'can manage employees')]


class Group(models.Model):
    name_choice = (
        ('manager', 'management'),
        ('employee', 'non-managerial employees'),
    )
    name = models.CharField(max_length=128, choices=name_choice)

    def __str__(self):
        return f'{self.name}'


class AddressHome(models.Model):
    employee = models.OneToOneField(User, related_name="address_home_employee", on_delete=models.CASCADE)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    country_region = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=6)


class AddressCore(models.Model):
    employee = models.OneToOneField(User, related_name="address_core_employee", on_delete=models.CASCADE)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    country_region = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=6)


class Vacation(models.Model):
    status_choice = (
        ('accepted', 'accepted_vacation'),
        ('rejected', 'rejected_vacation'),
        ('pending', 'pending_application'),
    )
    employee = models.ForeignKey(User, related_name="vacation_employee", on_delete=models.CASCADE)
    replacement = models.ForeignKey(User, related_name="vacation_replacement", on_delete=models.CASCADE)
    vacation_from = models.DateField()
    vacation_to = models.DateField()
    status = models.CharField(max_length=16, choices=status_choice)

    def __str__(self):
        return f'Vacation id: {self.id} from: {self.vacation_from} to: {self.vacation_to}'


class Messages(models.Model):
    from_employee = models.ForeignKey(User, related_name="messages_from_employee", on_delete=models.CASCADE)
    to_employee = models.ForeignKey(User, related_name="messages_to_employee", on_delete=models.CASCADE)
    sending_date = models.DateTimeField(auto_now_add=True, blank=True)
    message = models.TextField()


class Delegation(models.Model):
    status_choice = (
        ('accepted', 'accepted_delegation'),
        ('rejected', 'rejected_delegation'),
        ('pending', 'pending_application'),
    )
    delegation_country_choice = (
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('IT', 'Italy'),
        ('PL', 'Poland'),
        ('CZ', 'Czech_republic'),
        ('SL', 'Slovakia'),
    )
    employee = models.ForeignKey(User, related_name="delegation_employee", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    delegation_country = models.CharField(max_length=2, choices=delegation_country_choice)
    status = models.CharField(max_length=16, choices=status_choice)

    def __str__(self):
        return f'Delegation country: {self.delegation_country} from: {self.start_date} to: {self.end_date}'


class MedicalLeave(models.Model):
    employee = models.ForeignKey(User, related_name="medical_employee", on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f'Medical Leave id: {self.id} from: {self.from_date} to: {self.to_date}'
