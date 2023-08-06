import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from training.models import ScholarshipPlan, ScholarshipEmp, ScholarshipEmpProgress
from settings_app.user_utils import c_unit, c_dep, c_user_de, c_user_deputy
from attendance.models import Attendance,AttendanceStatus, Year, Month
from django.contrib import messages
from settings_app.utils import getnewid
from datetime import datetime as dt 
from datetime import timedelta
import pandas as pd
from training.forms import ScholarshipPlanForm, ScholarshipEmpForm, ScholarshipEmpProgressForm, ScholarshipEmpThesisForm



@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoPlanAdd(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid, new_hashid = getnewid(ScholarshipPlan)
		form = ScholarshipPlanForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Bolso Estudo Aumenta Suseso')
			return redirect('hr-scho-detail',instance.hashed)
	else: form = ScholarshipPlanForm()
	context = {
		'group': group, 'form': form, 
		'title': 'Aumenta Planu Bolso Estudo', 'legend': 'Aumenta Planu Bolso Estudo'
	}
	return render(request, 'scholariship/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoPlanUpdate(request, hashid):
    group = request.user.groups.all()[0].name
    objects = get_object_or_404(ScholarshipPlan, hashed=hashid)
    if request.method == 'POST':
        form = ScholarshipPlanForm(request.POST,request.FILES, instance=objects )
        if form.is_valid():
            form.save()
            messages.success(request, f'Susesu Altera Plano')
            return redirect('hr-scho-detail', hashid)
    else: form = ScholarshipPlanForm(instance=objects)
    context = {
        'group': group, 'form': form, 
        'title': 'Altera Planu Bolso Estudo', 'legend': 'Altera Planu Bolso Estudo'
    }
    return render(request, 'scholariship/form.html', context)


@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoEmpAdd(request, hashid):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    if request.method == 'POST':
        newid, new_hashid = getnewid(ScholarshipEmp)
        form = ScholarshipEmpForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('emp')
            emp_check = ScholarshipEmp.objects.filter(emp=user, scholarship=splan).exists()
            if emp_check:
                messages.error(request, 'Funsionario refere rejistu tiha ona!')
            else:
                instance = form.save(commit=False)
                instance.id = newid
                instance.scholarship = splan
                instance.datetime = datetime.datetime.now()
                instance.user = request.user
                instance.hashed = new_hashid
                instance.save()
                messages.success(request, f'Susesu Aumenta Funsionario ba Bolso Estudo')
                return redirect('hr-scho-detail', hashid)
    else: form = ScholarshipEmpForm()
    context = {
        'group': group, 'form': form, 'page': 'emp-add', 'hashid': hashid,
        'title': 'Aumenta Pessoal ba Bolso Estudo', 'legend': 'Aumenta Pessoal ba Bolso Estudo'
    }
    return render(request, 'scholariship/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoEmpUpdate(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    objects = get_object_or_404(ScholarshipEmp, hashed=hashid2)
    if request.method == 'POST':
        form = ScholarshipEmpForm(request.POST, instance=objects)
        if form.is_valid():
            user = form.cleaned_data.get('emp')
            emp_check = ScholarshipEmp.objects.filter(emp=user, scholarship=splan).exists()
            if emp_check:
                messages.error(request, 'Funsionario refere rejistu tiha ona!')
            else:
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, f'Susesu Altera')
                return redirect('hr-scho-detail', splan.hashed)
    else: form = ScholarshipEmpForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'emp-add', 'hashid': hashid,
        'title': 'Altera Pessoal ba Bolso Estudo', 'legend': 'Altera Pessoal ba Bolso Estudo'
    }
    return render(request, 'scholariship/form.html', context)


@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoEmpThesisAdd(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    objects = get_object_or_404(ScholarshipEmp, hashed=hashid2)
    if request.method == 'POST':
        form = ScholarshipEmpThesisForm(request.POST, instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, f'Susesu Aumenta')
            return redirect('hr-scho-emp-detail', splan.hashed, hashid2)
    else: form = ScholarshipEmpThesisForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'emp-progress-add',  'hashid': hashid, 'hashid2': hashid2,
        'title': 'Aumenta Titulo Monografia', 'legend': 'Aumenta Titulo Monografia'
    }
    return render(request, 'scholariship/form.html', context)



@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoEmpDelete(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    objects = get_object_or_404(ScholarshipEmp, hashed=hashid2)
    objects.delete()
    messages.success(request, f'Susesu Delete')
    return redirect('hr-scho-detail', splan.hashed)

@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoPlanLock(request, hashid):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    splan.is_lock = True
    splan.save()
    messages.success(request, f'Susesu Chave')
    return redirect('hr-scho-detail', splan.hashed)


@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrSchoUpdaAtt(request, hashid, pk):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    semp = get_object_or_404(ScholarshipEmp, pk=pk)
    per = pd.date_range(start=splan.start_date, end=splan.end_date, freq='B')
    attstatus = get_object_or_404(AttendanceStatus, pk=11)
    for i in per:
        newid, hashedid = getnewid(Attendance)
        month = get_object_or_404(Month, pk=i.month)
        year = get_object_or_404(Year, year=i.year)
        year = Year.objects.filter(year=i.year).last()
        if not year:
            Year.objects.create(year=i.year)
        
        year = Year.objects.filter(year=i.year).last()
        created = Attendance.objects.create(
        id = newid,
        unit = semp.emp.curempdivision.unit,
        employee = semp.emp,
        year = year,
        month = month,
        date = i,
        status_am = attstatus,
        status_pm = attstatus,
        datetime=datetime.datetime.now(),
        user=request.user,
        hashed = hashedid)
        semp.is_update = True
        semp.save()
    messages.success(request, 'Susesu Altera Absensia')
    return redirect('hr-scho-detail', splan.hashed)




@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoEmpProgAdd(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    emp = get_object_or_404(ScholarshipEmp, hashed=hashid2)
    if request.method == 'POST':
        newid, new_hashid = getnewid(ScholarshipEmpProgress)
        form = ScholarshipEmpProgressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.scholarshipemp = emp
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Susesu Aumenta Progresu')
            return redirect('hr-scho-emp-detail', hashid, hashid2)
    else: form = ScholarshipEmpProgressForm()
    context = {
        'group': group, 'form': form, 'page': 'emp-progress-add', 'hashid': hashid, 'hashid2': hashid2,
        'title': 'Aumenta Progresu', 'legend': 'Aumenta Progresu'
    }
    return render(request, 'scholariship/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr'])
def hrSchoEmpProgUpdate(request, hashid, hashid2, pk):
    group = request.user.groups.all()[0].name
    splan = get_object_or_404(ScholarshipPlan, hashed=hashid)
    emp = get_object_or_404(ScholarshipEmp, hashed=hashid2)
    objects = get_object_or_404(ScholarshipEmpProgress, pk=pk)
    if request.method == 'POST':
        form = ScholarshipEmpProgressForm(request.POST, instance=objects)
        if form.is_valid():
            form.save()
            messages.success(request, f'Susesu Altera')
            return redirect('hr-scho-emp-detail', hashid, hashid2)
    else: form = ScholarshipEmpProgressForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'emp-progress-add', 'hashid': hashid, 'hashid2': hashid2,
        'title': 'Aumenta Progresu', 'legend': 'Aumenta Progresu'
    }
    return render(request, 'scholariship/form.html', context)