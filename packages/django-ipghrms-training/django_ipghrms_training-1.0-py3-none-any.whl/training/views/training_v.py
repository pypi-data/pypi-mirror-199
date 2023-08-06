import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from training.models import *
from settings_app.user_utils import c_unit, c_dep, c_user_de, c_user_deputy
from attendance.models import Attendance,AttendanceStatus, Year, Month
from django.contrib import messages
from settings_app.utils import getnewid
from datetime import datetime as dt 
from datetime import timedelta
import pandas as pd
from django.db.models import Q, Count, Subquery,OuterRef
import numpy as np
from training.utils import sumary_check_year, sumary_check_tr_year
from contract.models import EmpPlacement, EmpContractToR
from training.forms import TrainingEmpGapForm


@login_required
@allowed_users(allowed_roles=['unit'])
def cTDash(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = TrainingPlan.objects.filter(unit=unit).all().order_by('-year','id')
	context = {
		'group': group, 'unit': unit, 'objects': objects,
		'title': f'Painel Treinamento', 'legend': f'Painel Treinamento'
	}
	return render(request, 'training/c_dash.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTDash(request):
	group = request.user.groups.all()[0].name
	objects = TrainingPlan.objects.filter().all().order_by('-year','id')
	context = {
		'group': group, 'objects': objects,
		'title': f'Painel Treinamento', 'legend': f'Painel Treinamento'
	}
	return render(request, 'training/hr_dash.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deTDash(request):
	group = request.user.groups.all()[0].name
	objects = TrainingPlan.objects.filter().all().order_by('-year','id')
	context = {
		'group': group, 'objects': objects,
		'title': f'Painel Treinamento  & Bolso Estudo', 'legend': f'Painel Treinamento  & Bolso Estudo'
	}
	return render(request, 'training/de_dash.html', context)
###
@login_required
@allowed_users(allowed_roles=['unit'])
def cTPlanList(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = TrainingPlan.objects.filter(unit=unit).all().order_by('-year','id')
	years = TrainingPlan.objects.filter().distinct().values('year__year').all()
	context = {
		'group': group, 'unit': unit, 'objects': objects,
		'title': f'Lista Planu Treinamento', 'legend': f'Lista Planu Treinamento', 'years':years
	}
	return render(request, 'training/c_plan_list.html', context)


		

@login_required
@allowed_users(allowed_roles=['hr','de'])
def hrTSumaryList(request):
	group = request.user.groups.all()[0].name
	years = TYear.objects.exclude(Q(pk=1)|Q(pk=2)|Q(pk=3))
	employee = Employee.objects.filter(status_id=1)
	objects = []
	for emp in employee:
		empTr = sumary_check_year(emp)
		objects.append([emp, empTr])
	context = {
		'group': group,  'objects': objects,
		'title': f'Sumariu Geral Treinamento', 'legend': f'Sumariu Geral Treinamento', 'years':years
	}
	return render(request, 'training/summary.html', context)

@login_required
@allowed_users(allowed_roles=['hr','de'])
def hrTSumaryYearList(request, year):
	group = request.user.groups.all()[0].name
	years = get_object_or_404(TYear, year=year)
	employee = Employee.objects.filter(status_id=1)
	objects = []
	for emp in employee:
		empTr = sumary_check_tr_year(emp, years)
		objects.append([emp, empTr])
	context = {
		'group': group,  'objects': objects,
		'title': f'Sumariu Geral Treinamento iha Tinan {year}', 'legend': f'Sumariu Geral Treinamento iha tinan {year}', 'years':years
	}
	return render(request, 'training/summary_year.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cTPlanDetail(request, hashid):
	_, unit = c_unit(request.user)
	group = request.user.groups.all()[0].name
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temps = TrainingEmp.objects.filter(plan=tplan).all()
	tdep = TrainingDep.objects.filter(plan=tplan)
	employees = Employee.objects.filter(curempdivision__unit=unit, traininggap__isnull=False)
	tgap_dict = {}
	for emp in employees:
		gap = TrainingPlanGap.objects.filter(plan=tplan, gap__employee__pk=emp.pk)
		if gap:
			if emp in tgap_dict:
				tgap_dict[emp].extend(gap)
			else:
				tgap_dict[emp] = list(gap)

	tgap_list = []
	for emp, gap_list in tgap_dict.items():
		gap_dict = {}
		for gap in gap_list:
			if gap.gap in gap_dict:
				gap_dict[gap.gap].append(gap.gap)
			else:
				gap_dict[gap.gap] = [gap.gap]
		gap_items = [(gap, list(set(comments))) for gap, comments in gap_dict.items()]
		tgap_list.append((emp, gap_items))





	today = datetime.date.today()
	context = {
		'group': group, 'tplan': tplan, 'temps': temps, 'today': today,
		'title': f'Detalha Planu Treinamento', 'legend': f'Detalha Planu Treinamento',
		'tdep':tdep, 'tgap_list':tgap_list
	}
	return render(request, 'training/c_plan_detail.html', context)

@login_required
@allowed_users(allowed_roles=['hr', 'unit'])
def cTCritList(request, hashid, pk):
	group = request.user.groups.all()[0].name
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temp = get_object_or_404(TrainingEmp, pk=pk)
	ucrits = TrainingCriteria.objects.filter(plan=tplan, training_emp=temp, criteria__category="Unidade").all().order_by('id')
	hrcrits = TrainingCriteria.objects.filter(plan=tplan, training_emp=temp, criteria__category="RH").all().order_by('id')
	context = {
		'group': group, 'tplan': tplan, 'temp': temp, 'ucrits': ucrits, 'hrcrits': hrcrits,
		'title': f'Kriteria Husi Unidade', 'legend': f'Kriteria Husi Unidade'
	}
	return render(request, 'training/c_crit_list.html', context)
###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTPlanList(request):
	group = request.user.groups.all()[0].name
	c_emp, dep = c_unit(request.user)
	objects = TrainingPlan.objects.filter(is_send=True).all().order_by('-year','id')
	context = {
		'group': group, 'dep': dep, 'objects': objects,
		'title': f'Lista Planu Treinamento', 'legend': f'Lista Planu Treinamento'
	}
	return render(request, 'training/hr_plan_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTPlanDetail(request, hashid):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temps = TrainingEmp.objects.filter(plan=tplan).all()
	today = datetime.date.today()
	tdep = TrainingDep.objects.filter(plan=tplan)
	employees = Employee.objects.filter(traininggap__isnull=False)
	employee_list = []
	training_plan_gaps = TrainingPlanGap.objects.filter(plan=tplan)
	for training_plan_gap in training_plan_gaps:
		if training_plan_gap.employee not in employee_list:
			employee_list.append(training_plan_gap.employee)
	for training_emp in temps:
		if training_emp.employee not in employee_list:
			employee_list.append(training_emp.employee)
	tgap_dict = {}
	for emp in employees:
		gap = TrainingPlanGap.objects.filter(plan=tplan, gap__employee__pk=emp.pk)
		if gap:
			if emp in tgap_dict:
				tgap_dict[emp].extend(gap)
			else:
				tgap_dict[emp] = list(gap)

	tgap_list = []
	for emp, gap_list in tgap_dict.items():
		gap_dict = {}
		for gap in gap_list:
			if gap.gap in gap_dict:
				gap_dict[gap.gap].append(gap.gap)
			else:
				gap_dict[gap.gap] = [gap.gap]
		gap_items = [(gap, list(set(comments))) for gap, comments in gap_dict.items()]
		tgap_list.append((emp, gap_items))
	context = {
		'group': group, 'tplan': tplan, 'temps': temps, 'today': today,
		'title': f'Detalha Planu Treinamento', 'legend': f'Detalha Planu Treinamento',
		'tdep':tdep, 'tgap_list':tgap_list, 'employee_list':employee_list
	}	
	return render(request, 'training/hr_plan_detail.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTCritList(request, hashid, pk):
	group = request.user.groups.all()[0].name
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temp = get_object_or_404(TrainingEmp, pk=pk)
	ucrits = TrainingCriteria.objects.filter(plan=tplan, training_emp=temp, criteria__category="Unidade").all().order_by('id')
	hrcrits = TrainingCriteria.objects.filter(plan=tplan, training_emp=temp, criteria__category="RH").all().order_by('id')
	context = {
		'group': group, 'tplan': tplan, 'temp': temp, 'ucrits': ucrits, 'hrcrits': hrcrits,
		'title': f'Kriteria Husi Rekursu Humanu', 'legend': f'Kriteria Husi Rekursu Humanu'
	}
	return render(request, 'training/hr_crit_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTUpdaStatus(request, hashid, pk):
	group = request.user.groups.all()[0].name
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	emp = get_object_or_404(Employee, pk=pk)
	temp = TrainingEmp.objects.filter(plan=tplan, employee=emp)
	tempgap = TrainingPlanGap.objects.filter(plan=tplan, employee=emp)
	newid, hashedid = getnewid(Attendance)
	per = pd.date_range(start=tplan.start_date, end=tplan.end_date, freq='B')
	attstatus = get_object_or_404(AttendanceStatus, pk=5)
	for i in per:
		newid, hashedid = getnewid(Attendance)
		year = get_object_or_404(Year, year=i.year)
		month = get_object_or_404(Month, pk=i.month)
		created = Attendance.objects.create(
		id = newid,
		unit = emp.curempdivision.unit,
		employee = emp,
		year = year,
		month = month,
		date = i,
		status_am = attstatus,
		status_pm = attstatus,
		datetime=datetime.datetime.now(),
		user=request.user,
		hashed = hashedid)
		# tplan.is_update = True
		# tplan.save()

	for i in temp:
		i.is_update = True
		i.save()
	for j in tempgap:
		j.is_update = True
		j.save()


	messages.success(request, 'Susesu Altera')
	return redirect('train-hr-plan-detail', hashid)
###
@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deTPlanList(request):
	group = request.user.groups.all()[0].name
	c_emp, dep = c_unit(request.user)
	objects = TrainingPlan.objects.filter(is_send=True).all().order_by('-year','id')
	
	context = {
		'group': group, 'dep': dep, 'objects': objects,
		'title': f'Lista Planu Treinamento', 'legend': f'Lista Planu Treinamento'
	}
	return render(request, 'training/de_plan_list.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deTPlanDetail(request, hashid):
	group = request.user.groups.all()[0].name
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temps = TrainingEmp.objects.filter(plan=tplan).all()
	tdep = TrainingDep.objects.filter(plan=tplan)
	today = datetime.date.today()
	employees = Employee.objects.filter(traininggap__isnull=False)
	tgap_dict = {}
	for emp in employees:
		gap = TrainingPlanGap.objects.filter(plan=tplan, gap__employee__pk=emp.pk)
		if gap:
			if emp in tgap_dict:
				tgap_dict[emp].extend(gap)
			else:
				tgap_dict[emp] = list(gap)

	tgap_list = []
	for emp, gap_list in tgap_dict.items():
		gap_dict = {}
		for gap in gap_list:
			if gap.gap in gap_dict:
				gap_dict[gap.gap].append(gap.gap)
			else:
				gap_dict[gap.gap] = [gap.gap]
		gap_items = [(gap, list(set(comments))) for gap, comments in gap_dict.items()]
		tgap_list.append((emp, gap_items))
	context = {
		'group': group, 'tplan': tplan, 'temps': temps, 'today': today,
		'title': f'Detalha Planu Treinamento', 'legend': f'Detalha Planu Treinamento',
		'tdep':tdep, 'tgap_list':tgap_list,
	}
	return render(request, 'training/de_plan_detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['unit'])
def cTRawData(request):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	objects = []
	plans = TrainingPlan.objects.filter(unit=unit).all().order_by('-year','id')
	for i in plans:
		employee_list = []
		emps = TrainingEmp.objects.filter(plan=i).all()
		training_plan_gaps = TrainingPlanGap.objects.filter(plan=i)
		tdep = TrainingDep.objects.filter(plan=i)
		for training_plan_gap in training_plan_gaps:
			if training_plan_gap.employee not in employee_list:
				employee_list.append(training_plan_gap.employee)
		for training_emp in emps:
			if training_emp.employee not in employee_list:
				employee_list.append(training_emp.employee)
		objects.append([i,emps,tdep, employee_list])
	context = {
		'group': group, 'unit': unit, 'objects': objects,
		'title': f'Lista Treinamento', 'legend': f'Lista Treinamento'
	}
	return render(request, 'training/c_raw_data.html', context)

@login_required
# @allowed_users(allowed_roles=['unit'])
def TRawData(request):
	group = request.user.groups.all()[0].name
	objects = []
	plans = TrainingPlan.objects.filter().all().order_by('-year','id')
	for i in plans:
		emps = TrainingEmp.objects.filter(plan=i).all()
		tot = emps.count()
		objects.append([i,emps,tot])
	context = {
		'group': group, 'objects': objects,
		'title': f'Raw Data Treinamento', 'legend': f'Raw Data Treinamento'
	}
	return render(request, 'training/raw_data.html', context)
from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def TrainEmpSubjectFile(request, pk):
	emp = get_object_or_404(TrainingEmp, pk=pk)
	file = str(settings.BASE_DIR)+str(emp.subject.url)
	try:
		if file:
			return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')

@login_required
def TrainEmpPareserFile(request, hashid):
	train = get_object_or_404(TrainingPlan, hashed=hashid)
	file = str(settings.BASE_DIR)+str(train.file.url)
	try:
		if file:
			return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')
	

# TRAINING GAP
@login_required
@allowed_users(allowed_roles=['unit'])
def TrainingGapEmpList(request, pk):
	unit = Unit.objects.get(pk=pk)
	staffs = EmpPlacement.objects.filter(unit=unit, is_active=True).all()

	context = {
		'title': f'Lista Funsionario iha Divizaun {unit.name}',
		'legend': f'Lista Funsionario iha Divizaun {unit.name}',
		'staffs': staffs, 'unit':unit
	}

	return render(request, 'gap/list.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def TrainingGapList(request, hashid, pk):
	objects = []
	unit = get_object_or_404(Unit, pk=pk)
	employee = get_object_or_404(Employee, hashed=hashid)
	tor = EmpContractToR.objects.filter(employee=employee, contract__is_active=True)
	checkgap = TrainingGap.objects.filter(employee=employee, is_lock=False).exists()
	for obj in tor:
		gap = TrainingGap.objects.filter(tor=obj, employee=employee)
		objects.append([obj,gap])
	context = {
		'title': f'Lista Tranning GAP Analysis bazeia ba ToR',
		'legend': f'Lista Tranning GAP Analysis bazeia ba ToR',
		'employee': employee, 'objects': objects, 'unit':unit, 'checkgap':checkgap
	}

	return render(request, 'gap/emp_gap_list.html', context)


@login_required
@allowed_users(allowed_roles=['unit'])
def TrainingGapAdd(request, hashid, pk, hashid2):
	employee = get_object_or_404(Employee, hashed=hashid)
	unit = get_object_or_404(Unit, pk=pk)
	tor = get_object_or_404(EmpContractToR, hashed=hashid2)
	if request.method == 'POST':
		newid, new_hashid = getnewid(TrainingGap)
		form = TrainingEmpGapForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee= employee
			instance.tor = tor
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('train-unit-gap-emp-list', hashid=employee.hashed, pk=unit.pk)
	else: form = TrainingEmpGapForm()
	context = {
		'form': form, 'page': 'plist',
		'title': 'Aumenta Training GAP Analysis', 'legend': 'Aumenta Training GAP Analysis'
	}
	return render(request, 'gap/form.html', context)


@login_required
@allowed_users(allowed_roles=['unit'])
def TrainingGapUpdate(request, hashid, pk, hashid2):
	employee = get_object_or_404(Employee, hashed=hashid)
	unit = get_object_or_404(Unit, pk=pk)
	gap = get_object_or_404(TrainingGap, hashed=hashid2)
	if request.method == 'POST':
		form = TrainingEmpGapForm(request.POST, instance=gap)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('train-unit-gap-emp-list', hashid=employee.hashed, pk=unit.pk)
	else: form = TrainingEmpGapForm(instance=gap)
	context = {
		'form': form, 'page': 'plist',
		'title': 'Altera Training GAP Analysis', 'legend': 'Altera Training GAP Analysis'
	}
	return render(request, 'gap/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def TrainingGapDelete(request, hashid, pk, hashid2):
	employee = get_object_or_404(Employee, hashed=hashid)
	unit = get_object_or_404(Unit, pk=pk)
	gap = get_object_or_404(TrainingGap, hashed=hashid2)
	gap.delete()
	messages.success(request, f'Delete sucessu.')
	return redirect('train-unit-gap-emp-list', hashid=employee.hashed, pk=unit.pk)


@login_required
@allowed_users(allowed_roles=['unit'])
def TrainingGapLock(request, hashid, pk):
	employee = get_object_or_404(Employee, hashed=hashid)
	unit = get_object_or_404(Unit, pk=pk)
	gap = TrainingGap.objects.filter(employee=employee, is_lock = False)
	for obj in gap:
		obj.is_lock = True
		obj.save()
	messages.success(request, f'Chave sucessu.')
	return redirect('train-unit-gap-emp-list', hashid=employee.hashed, pk=unit.pk)
