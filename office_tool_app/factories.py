# import factory
# from django.contrib.auth import get_user_model
# from office_tool_app.models import Category, Institution, Donation
# from django.db import transaction


# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = get_user_model()

#     email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))
#     first_name = factory.Faker('first_name')
#     last_name = factory.Faker('last_name')
#     is_staff = True


# class CategoryFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Category

#     name = factory.Sequence(lambda n: 'Category {}'.format(n))


# class InstitutionFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Institution

#     name = factory.Sequence(lambda n: 'Institution {}'.format(n))
#     description = 'Description'
#     goals = 'Goals'
#     type = 'FU'


# class DonationFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Donation

#     quantity = 1
#     institution = factory.SubFactory(InstitutionFactory)
#     address = 'Address'
#     phone_number = '123456789'
#     city = 'City'
#     zip_code = '12345'
#     pick_up_date = factory.Faker('date_this_year')
#     pick_up_time = factory.Faker('time')
#     pick_up_comment = 'Comment'
#     user = factory.SubFactory(UserFactory)
