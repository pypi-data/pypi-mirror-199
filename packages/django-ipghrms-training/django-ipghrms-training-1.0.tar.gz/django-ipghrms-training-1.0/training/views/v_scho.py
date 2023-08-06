import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from training.models import ScholarshipPlan, ScholarshipEmp, ScholarshipEmpProgress, TYear
from settings_app.user_utils import c_unit, c_dep, c_user_de, c_user_deputy
from attendance.models import Attendance,AttendanceStatus, Year, Month
from django.contrib import messages
from settings_app.utils import getnewid
from datetime import datetime as dt 
from datetime import timedelta
import pandas as pd




@login_required
@allowed_users(allowed_roles=['hr', 'de', 'deputy'])
def hrSchoRawData(request):
    group = request.user.groups.all()[0].name
    c_emp, unit = c_unit(request.user)
    objects = ScholarshipEmp.objects.all()
    years = ScholarshipEmp.objects.filter().distinct().values('scholarship__year__year').all()

    context = {
        'group': group, 'unit': unit, 'objects': objects, 'years': years,
        'title': f'Raw Data Bolso Estudo', 'legend': f'Raw Data Bolso Estudo'
    }
    return render(request, 'scholariship/raw_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr', 'de', 'deputy'])
def hrSchoRawDataYear(request,year):
    group = request.user.groups.all()[0].name
    year = TYear.objects.get(year=year)
    c_emp, unit = c_unit(request.user)
    objects = ScholarshipEmp.objects.filter(scholarship__year=year)
    years = ScholarshipEmp.objects.filter().distinct().values('scholarship__year__year').all()
    
    context = {
        'group': group, 'unit': unit, 'objects': objects, 'years': years,
        'title': f'Raw Data Bolso Estudo iha tinan {year}', 'legend': f'Raw Data Bolso Estudo iha tinan {year}'
    }
    return render(request, 'scholariship/raw_list.html', context)
    
@login_required
@allowed_users(allowed_roles=['hr', 'de', 'deputy'])
def hrSchoList(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = ScholarshipPlan.objects.all()
	context = {
		'group': group, 'unit': unit, 'objects': objects,
		'title': f'Lista Bolso Estudo', 'legend': f'Lista Bolso Estudo'
	}
	return render(request, 'scholariship/list.html', context)

@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoDetail(request, hashid):
    group = request.user.groups.all()[0].name
    schol = get_object_or_404(ScholarshipPlan, hashed=hashid)
    objects = ScholarshipEmp.objects.filter(scholarship=schol)
    context = {
        'group': group, 'objects': objects, 'schol': schol,
        'title': f'Detalha Bolso Estudo', 'legend': f'Detalha Bolso Estudo'
    }
    return render(request, 'scholariship/detail.html', context)

@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoEmpDetail(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    schol = get_object_or_404(ScholarshipPlan, hashed=hashid)
    emp = get_object_or_404(ScholarshipEmp, hashed=hashid2)
    objects = ScholarshipEmpProgress.objects.filter(scholarshipemp=emp)
    context = {
        'group': group, 'objects': objects, 'schol': schol, 'emp':emp,
        'title': f'Detalha Pessoal Bolso Estudo', 'legend': f'Detalha Pessoal Bolso Estudo'
    }
    return render(request, 'scholariship/emp_detail.html', context)
