import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')

import django
django.setup()

import random

from first_app.models import User
from faker import Faker

fakegen = Faker()

users = ['Canada', 'USA', 'India']

def add_user():
    t = User.objects.get_or_create(first_name=random.choice(users))[0]
    t.save()
    return t

def populate(N=5):
    for entry in range(N):
        user = add_user()
        fake_name = fakegen.first_name()
        fake_last_name = fakegen.last_name()
        fake_email = fakegen.email()

        user.first_name = fake_name
        user.last_name = fake_last_name
        user.email = fake_email
        user.save()

if __name__ == '__main__':
    print('Populating script')
    populate(20)
    print('Populating Complete')
