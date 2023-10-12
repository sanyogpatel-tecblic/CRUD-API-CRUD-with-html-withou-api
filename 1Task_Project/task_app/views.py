from django.shortcuts import render
from rest_framework.response import Response
from .models import Region,State,Zone,District
from task_app.serializers import StateSerializer,RegionSerializer,ZoneSerializer,DistrictSerializer
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import SheetDataSerializer
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import SheetDataSerializer

from django.core.mail import EmailMessage


from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa


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
            basic_salary_actual_rate = row.get('basic_salary_actual_rate', 0)
            house_rent_allowance_actual_rate = row.get('house_rent_allowance_actual_rate', 0)
            conveyance_allowance_actual_rate = row.get('conveyance_allowance_actual_rate', 0)
            special_allowance_actual_rent = row.get('special_allowance_actual_rent', 0)

            total_earnings_actual_rate = (
                basic_salary_actual_rate
                + house_rent_allowance_actual_rate
                + conveyance_allowance_actual_rate
                + special_allowance_actual_rent
            )
            
            row['total_earnings_actual_rate'] = total_earnings_actual_rate
            print(f'Total Earnings Actual Rate: {total_earnings_actual_rate}')
            
            total_earnings_earnings= (
                row['basic_salary_earnings']
                + row['house_rent_allowance_earnings']
                + row['conveyance_allowance_earnings']
                + row['special_allowance_earnings']
            )
            row['total_earnings_earnings'] = total_earnings_earnings
            print(f'Total Earnings Actual Rate Earnings: {total_earnings_earnings}')
            
            total_deductions_actual_deductions = (
                row['pro_tax_actual_deduction']
                + row['tds_actual_deduction']
                + row['provident_fund_actual_deduction']
                + row['esic_actual_deduction']
            )

            row['total_deductions_actual_deductions'] = total_deductions_actual_deductions
            print(f'Total deductions Actual Deductions: {total_deductions_actual_deductions}')
            
            total_deductions_deductions = (
                row['pro_tax_deduction']
                + row['tds_deduction']
                + row['provident_fund_deduction']
                + row['esic_deduction']
            )

            row['total_deductions_deductions'] = total_deductions_deductions
            print(f'Total deductions: {total_deductions_deductions}')

            email = row['email']
            serializer = SheetDataSerializer(row)

            pdf_content = render_to_pdf('email_template.html', serializer.data)

            email = EmailMessage(
                subject,
                'Please find attached the PDF with Google Sheet Data.',
                from_email,
                [email],
            )
            email.attach('Salary Slip.pdf', pdf_content.getvalue(), 'application/pdf')

            email.send(fail_silently=False)

        return Response({'message': 'Emails sent successfully.'}, status=status.HTTP_200_OK)


