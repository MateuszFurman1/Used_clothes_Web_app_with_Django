from django.core.management.base import BaseCommand
from Used_clothes_app.factories import DonationFactory, UserFactory, CategoryFactory, InstitutionFactory
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **options):
        # # Create user instance of the User model using the UserFactory
        # user = UserFactory.create_batch(1)
        
        # # Create 5 instances of the Category model using the CategoryFactory
        # categories = CategoryFactory.create_batch(5)
        
        # # Create 5 instances of the Institution model using the InstitutionFactory
        # institutions = InstitutionFactory.create_batch(5)

        # # Create 5 instances of the Donation model using the DonationFactory
        # donations = DonationFactory.create_batch(5)

        # self.stdout.write(self.style.SUCCESS(
        #     'Successfully seeded the database with dummy data.'))
        
        with transaction.atomic():
            users = UserFactory.create_batch(10)
            categories = CategoryFactory.create_batch(10)
            institutions = InstitutionFactory.create_batch(10)
            donations = DonationFactory.create_batch(10)

