from django.core.management.base import BaseCommand
from Used_clothes_app.factories import DonationFactory, UserFactory, CategoryFactory, InstitutionFactory
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **options):
        with transaction.atomic():
            users = UserFactory.create_batch(5)
            categories = CategoryFactory.create_batch(5)
            institutions = InstitutionFactory.create_batch(5)
            donations = DonationFactory.create_batch(5)

