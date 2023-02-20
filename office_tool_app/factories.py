import factory
from django.contrib.auth import get_user_model
from .models import Group, AddressHome, AddressCore, Vacation, Messages, Delegation, MedicalLeave


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda o: '{}.{}@example.com'.format(o.first_name, o.last_name).lower())
    pesel = factory.Faker('random_int', min=10000000000, max=99999999999)
    birth_date = factory.Faker('date_of_birth')
    father_name = factory.Faker('first_name')
    mother_name = factory.Faker('first_name')
    family_name = factory.Faker('last_name')
    position = factory.Faker('job')
    updated = factory.Faker('date_time_this_month')
    joined = factory.Faker('date_time_this_month')

    @factory.post_generation
    def group(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.group = extracted
        else:
            from .models import Group
            # check if a group with the name "employee" exists
            group = Group.objects.filter(name='employee').first()
            if group:
                self.group = group
            else:
                self.group = Group.objects.create(name='employee')


# class GroupFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Group

#     name = factory.Faker('random_element', elements=['manager', 'employee'])


class AddressHomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AddressHome

    city = factory.Faker('city')
    province = factory.Faker('state')
    country_region = factory.Faker('country')
    postal_code = factory.Faker('postalcode')

    employee = factory.SubFactory(UserFactory)


class AddressCoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AddressCore

    city = factory.Faker('city')
    province = factory.Faker('state')
    country_region = factory.Faker('country')
    postal_code = factory.Faker('postalcode')

    employee = factory.SubFactory(UserFactory)


class VacationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacation

    vacation_from = factory.Faker('date_this_year')
    vacation_to = factory.Faker('date_this_year', before_today=False)
    status = factory.Faker('random_element', elements=['accepted', 'rejected', 'pending'])

    employee = factory.SubFactory(UserFactory)
    replacement = factory.SubFactory(UserFactory)


class MessagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Messages

    from_employee = factory.SubFactory(UserFactory)
    to_employee = factory.SubFactory(UserFactory)
    message = factory.Faker('text')


class DelegationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Delegation

    start_date = factory.Faker('date_this_year')
    end_date = factory.Faker('date_this_year', before_today=False)
    status = factory.Faker('random_element', elements=['accepted', 'rejected', 'pending'])
    delegation_country = factory.Faker('random_element', elements=['FR', 'DE', 'IT', 'PL', 'CZ', 'SL'])

    employee = factory.SubFactory(UserFactory)


class MedicalLeaveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MedicalLeave

    from_date = factory.Faker('date_this_year')
    to_date = factory.Faker('date_this_year', before_today=False)

    employee = factory.SubFactory(UserFactory)