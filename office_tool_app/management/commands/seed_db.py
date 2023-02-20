from django.core.management.base import BaseCommand
from office_tool_app.factories import UserFactory, GroupFactory, AddressHomeFactory, AddressCoreFactory, VacationFactory, MessagesFactory, DelegationFactory, MedicalLeaveFactory
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **options):
        with transaction.atomic():
            users = UserFactory.create_batch(1)
            # groups = GroupFactory.create_batch(5)
            address_home = AddressHomeFactory.create_batch(5)
            address_core = AddressCoreFactory.create_batch(5)
            vacation = VacationFactory.create_batch(5)
            messages = MessagesFactory.create_batch(5)
            delegation = DelegationFactory.create_batch(5)
            medical_leave = MedicalLeaveFactory.create_batch(5)