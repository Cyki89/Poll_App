import os
import django
from django.core.management.base import BaseCommand
from random import randint
from ad_service.models import ADUser, ADGroup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()


AD_GROUPS = [
    "Admins",
    "Purchases",
    "HumanResources",
    "ContinousImprovement",
    "TechnologyGroup",
]

NAMES = """Mark Cuban
Elton Jones
David Paterson
Austin River
Michael Wright
Drew Gallagher
Drew Keller
Andy O'Brien
Thomas Gonzales
Jeff Edwards
Ronald Watson
Kenny O'Neal
George Lewis
Edward Craig
Erik Fuller
Michael Parker
Steve Jefferson
Michael Mitchell
Anthony Austin
Russell Davies"""


class Command(BaseCommand):
    help = "Populates the database with collections and products"

    def handle(self, *args, **options):
        # ADGroup.objects.bulk_create([ADGroup(name=group) for group in AD_GROUPS])

        # names = NAMES.split("\n")
        # for idx, name in enumerate(names):
        #     first_name, last_name = name.split()
        #     username = f"{first_name}.{last_name}"
        #     email = f"{username}@gmail.com"

        #     user = ADUser.objects.create(
        #         first_name=first_name,
        #         last_name=last_name,
        #         username=username,
        #         email=email,
        #     )

        #     if idx % 3 != 0:
        #         user.groups.add(ADGroup.objects.get(id=randint(0, len(AD_GROUPS) - 1)))

        users = ADUser.objects.all()
        for user in users:
            user.set_password(user.first_name)
            user.save()
