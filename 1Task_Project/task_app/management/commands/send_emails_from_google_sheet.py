# app_name/management/commands/send_emails_from_google_sheet.py
from django.core.management.base import BaseCommand
from task_app.models import GoogleSheetData
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send emails to recipients from Google Sheet data'

    def handle(self, *args, **options):
        google_sheet_data = GoogleSheetData.objects.all()
        for data in google_sheet_data:
            subject = 'Google Sheet Data'
            message = f'ID: {data.id}\nEmail: {data.email}\nAmount: {data.amount}'
            from_email = 'sanyogpatel.tecblic@example.com'
            recipient_list = [data.email]
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS(f'Sent email to {data.email}'))
