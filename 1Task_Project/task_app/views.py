from django.shortcuts import render
from rest_framework.response import Response
from .models import Region,State,Zone,District
from task_app.serializers import StateSerializer,RegionSerializer,ZoneSerializer,DistrictSerializer
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response


@api_view(['GET'])
def GetRegion(request):
    region = Region.objects.all()
    serializer = RegionSerializer(region,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetState(request):
    region = request.query_params.get('region')
    states = State.objects.filter(region__region__iexact=region,region__region__icontains=region)
    serializer = StateSerializer(states, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetZone(request):   
    state = request.query_params.get('state')
    zone =Zone.objects.filter(state__state__iexact= state)
    serializer = ZoneSerializer(zone, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetDistrict(request):
    zone = request.query_params.get('zone')
    words = zone.split() 
    query = Q()

    for word in words:
        query |= Q(zone__zone__icontains=word)

    district = District.objects.filter(query)
    serializer = DistrictSerializer(district, many=True)
    return Response(serializer.data)


# myapp/views.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import SheetDataSerializer

# myapp/views.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import SheetDataSerializer

from rest_framework import serializers
import json

from django.core.mail import EmailMessage

# Import necessary libraries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Google_Sheet_Data.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class SendEmailToAll(APIView):
    def post(self, request):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive",  
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        gc = gspread.authorize(credentials)

        sheet = gc.open('task')
        worksheet = sheet.get_worksheet(0) 
        data = worksheet.get_all_records()

        subject = 'Google Sheet Data'
        from_email = 'sanyog.patel@tecblic.com'

        for row in data:
            email = row['email']
            serializer = SheetDataSerializer(row)

            pdf_content = render_to_pdf('task_app/email_template.html', serializer.data)

            email = EmailMessage(
                subject,
                'Please find attached the PDF with Google Sheet Data.',
                from_email,
                [email],
            )
            email.attach('Google_Sheet_Data.pdf', pdf_content.getvalue(), 'application/pdf')

            email.send(fail_silently=False)

        return Response({'message': 'Emails sent successfully.'}, status=status.HTTP_200_OK)





