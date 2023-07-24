# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings')

# import django
# django.setup()

# import random
# from DRF_app.models import Task_Faker, User_Faker
# from faker import Faker

# fakegen = Faker()

# def generate_random_user_id():
#     # Get the count of existing users in the User_Faker table
#     user_count = User_Faker.objects.count()
#     # Generate a random index within the range of existing user ids
#     random_index = random.randint(0, user_count - 1)
#     # Get the user_id of the user at the random index
#     user_id = User_Faker.objects.values_list('id', flat=True).order_by('id')[random_index]
#     return user_id

# def generate_random_role_id():
#     return random.randint(1, 4)

# def create_fake_task():
#     task = fakegen.word()
#     user_id = generate_random_user_id()
#     role_id = generate_random_role_id()
#     return Task_Faker(task=task, user_id=user_id,role_id = role_id)


# if __name__ == '__main__':
#     print('Populating script')
#     fake_tasks = [create_fake_task() for _ in range(50000)]
#     Task_Faker.objects.bulk_create(fake_tasks)
#     print('Populating Complete')
