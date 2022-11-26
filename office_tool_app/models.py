from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pesel = models.PositiveIntegerField()
    birth_date = models.DateField()
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=200)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, blank=True)
    position = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True, blank=True)


class Group(models.Model):
    name_choice = [
        ('manager', 'management'),
        ('employee', 'non-managerial employees'),
    ]
    name = models.CharField(max_length=100, choices=name_choice)


class Address(models.Model):
    address_choice = [
        ('home', 'home_address'),
        ('cor', 'correspondence_address'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(choices=address_choice)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country_region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)


class Vacation(models.Model):
    status_choice = [
        ('accepted', 'accepted_vacation'),
        ('rejected', 'rejected_vacation'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    replacement = models.ForeignKey(User, on_delete=models.CASCADE)
    vacation_from = models.DateField()
    vacation_to = models.DateField()
    status = models.CharField(choices=status_choice)

    class Meta:
        unique_together = ('employee', 'replacement')


class Messages(models.Model):
    from_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    to_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()


class Delegation(models.Model):
    status_choice = [
        ('accepted', 'accepted_vacation'),
        ('rejected', 'rejected_vacation'),
    ]
    delegation_country_choice = [
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('IT', 'Italy'),
        ('PL', 'Poland'),
        ('CZ', 'Czech_republic'),
        ('SL', 'Slovakia'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    delegation_country = models.CharField(choices=delegation_country_choice)
    status = models.CharField(choices=status_choice)