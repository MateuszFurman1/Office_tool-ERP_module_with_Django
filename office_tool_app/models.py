from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pesel = models.PositiveIntegerField(null=True)
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


class Address(models.Model):
    address_choice = (
        ('home', 'home_address'),
        ('cor', 'correspondence_address'),
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=16, choices=address_choice)
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
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    delegation_country = models.CharField(max_length=2, choices=delegation_country_choice)
    status = models.CharField(max_length=16, choices=status_choice)


class MedicalLeave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        permissions = [('can_add_medical_leave', 'can add medical leave')]