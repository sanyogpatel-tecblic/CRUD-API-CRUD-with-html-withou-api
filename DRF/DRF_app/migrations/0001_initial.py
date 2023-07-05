# Generated by Django 4.2.2 on 2023-07-05 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=264, unique=True)),
                ('password', models.CharField(max_length=264, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=10000)),
                ('status', models.CharField(default=0, max_length=2)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DRF_app.user')),
            ],
        ),
    ]
