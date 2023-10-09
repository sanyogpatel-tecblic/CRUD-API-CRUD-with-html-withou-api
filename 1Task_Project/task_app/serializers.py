from rest_framework import serializers
from .models import State,Region,Zone,District

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'state','region_id']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'zone','state_id']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'district','zone_id']
        
class SheetDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    employee_code = serializers.CharField()
    employee_name = serializers.CharField()
    designation = serializers.CharField()
    department = serializers.CharField()
    date_of_joining = serializers.DateField()
    bank_ac_no = serializers.CharField()
    bank_name = serializers.CharField()
    pan_no = serializers.CharField()
    uan_number = serializers.CharField()
    present_days = serializers.DecimalField(max_digits=5, decimal_places=2)
    paid_leaves = serializers.DecimalField(max_digits=5, decimal_places=2)
    weekly_off = serializers.DecimalField(max_digits=5, decimal_places=2)
    holidays = serializers.DecimalField(max_digits=5, decimal_places=2)
    lwp = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_salary_days = serializers.DecimalField(max_digits=5, decimal_places=2)
    basic_salary_actual_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    basic_salary_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    house_rent_allowance_actual_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    house_rent_allowance_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    conveyance_allowance_actual_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    conveyance_allowance_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    special_allowance_actual_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    special_allowance_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    pro_tax_actual_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    pro_tax_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    tds_actual_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    tds_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    provident_fund_actual_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    provident_fund_deduction = serializers.DecimalField(max_digits=10, decimal_places=2) 
    esic_actual_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    esic_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_earnings_actual_rate= serializers.DecimalField(max_digits=100, decimal_places=2)
    total_earnings_earnings= serializers.DecimalField(max_digits=100, decimal_places=2)
    total_deductions_actual_deductions= serializers.DecimalField(max_digits=100, decimal_places=2)
    total_deductions_deductions= serializers.DecimalField(max_digits=100, decimal_places=2)




