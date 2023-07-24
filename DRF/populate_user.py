# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings')

# import django
# django.setup()

# import random
# from DRF_app.models import User_Faker
# from faker import Faker

# fakegen = Faker()

# users = ['Brazil', 'UK', 'USA']
# generated_emails = set()

# def generate_unique_email():
#     fake_email = fakegen.email()
#     while fake_email in generated_emails or User_Faker.objects.filter(email=fake_email).exists():
#         fake_email = fakegen.email()
#     generated_emails.add(fake_email)
#     return fake_email

# def generate_random_role_id():
#     return random.randint(1, 4)

# def create_fake_user():
#     fake_name = fakegen.first_name()
#     fake_last_name = fakegen.last_name()
#     fake_email = generate_unique_email()
#     return User_Faker(first_name=fake_name, last_name=fake_last_name, email=fake_email)

# if __name__ == '__main__':
#     print('Populating script')
#     fake_users = [create_fake_user() for _ in range(50000)]
#     for user in fake_users:
#         user.role_id = generate_random_role_id()
#     User_Faker.objects.bulk_create(fake_users)
#     print('Populating Complete')
