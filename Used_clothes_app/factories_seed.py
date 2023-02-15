import factory
from django.contrib.auth import get_user_model
from Used_clothes_app.models import Category, Institution, Donation


user = UserFactory()
category = CategoryFactory(5)
institution = InstitutionFactory(5)
donation = DonationFactory(5)