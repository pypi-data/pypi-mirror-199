import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import CurEmpDivision, CurEmpPosition, EmpSpecialize, FormalEducation
from settings_app.decorators import allowed_users
from django.contrib import messages
from training.models import TrainingPlan, TrainingCriteria
from training.forms import *
from settings_app.utils import getnewid
from settings_app.user_utils import c_dep, c_unit

###
@login_required
@allowed_users(allowed_roles=['unit'])
def cTPlanAdd(request):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	if request.method == 'POST':
		newid, new_hashid = getnewid(TrainingPlan)
		form = TrainingPlanForm(unit, request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.unit = unit
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('train-c-plan-detail', instance.hashed)
	else: form = TrainingPlanForm(unit)
	context = {
		'group': group, 'form': form, 'page': 'plist',
		'title': 'Aumenta Planu', 'legend': 'Aumenta Planu Treinmanto'
	}
	return render(request, 'training/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cTPlanUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	objects = get_object_or_404(TrainingPlan, hashed=hashid)
	if request.method == 'POST':
		form = TrainingPlanForm(unit, request.POST, request.FILES,  instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('train-c-plan-detail', objects.hashed)
	else: form = TrainingPlanForm(unit, instance=objects)
	context = {
		'group': group, 'form': form, 'page': 'plist',
		'title': 'Altera Planu', 'legend': 'Altera Planu'
	}
	return render(request, 'training/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['unit'])
def cTEmpAdd(request, hashid):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(TrainingEmp)
		form = TrainingEmpForm(unit, request.POST)
		if form.is_valid():
			emp = form.cleaned_data.get('employee')
			empdiv = CurEmpDivision.objects.filter(employee=emp).first()
			emppos = CurEmpPosition.objects.filter(employee=emp).first()
			empform = FormalEducation.objects.filter(employee=emp).last()
			trainningemp = TrainingEmp.objects.filter(employee=emp).exists()
			if trainningemp:
				messages.warning(request, 'Funsionario Iha Ona')
			else:
				instance = form.save(commit=False)
				instance.id = newid
				instance.plan = tplan
				if empdiv.unit: instance.unit = empdiv.unit
				elif empdiv.department: instance.department = empdiv.department
				if emppos.position: instance.position = emppos.position
				if empform: instance.diploma = empform.education_level
				instance.datetime = datetime.datetime.now()
				instance.user = request.user
				instance.save()
				messages.success(request, f'Aumenta sucessu.')
				return redirect('train-c-plan-detail', hashid=hashid)
	else: form = TrainingEmpForm(unit)
	context = {
		'group': group, 'form': form, 'tplan': tplan, 'page': 'pdetail',
		'title': 'Aumenta Funsionario', 'legend': 'Aumenta Funsionario'
	}
	return render(request, 'training/form.html', context)



### TRAINING DEPARTMENT ###
@login_required
@allowed_users(allowed_roles=['unit'])
def cTDepAdd(request, hashid):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	if request.method == 'POST':
		form = TrainingDepForm(request.POST)
		if form.is_valid():
			newid, _ = getnewid(TrainingEmp)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = tplan
			instance.user = request.user
			instance.datetime = datetime.datetime.now()
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('train-c-plan-detail', hashid=hashid)
	else:
		form = TrainingDepForm()
	context = {
		'group': group,
		'form': form,
		'tplan': tplan,
		'page': 'pdetail',
		'title': 'Aumenta Ekipa',
		'legend': 'Aumenta Ekipa'
	}
	return render(request, 'training/form2.html', context)



@login_required
@allowed_users(allowed_roles=['unit'])
def cTDepUpdate(request, hashid, pk):
	group = request.user.groups.all()[0].name
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	dep = get_object_or_404(TrainingDep, pk=pk)
	if request.method == 'POST':
		newid, _ = getnewid(TrainingEmp)
		form = TrainingDepForm(request.POST, instance=dep)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = tplan
			instance.user = request.user
			instance.save()
			messages.success(request, f'Delete sucessu.')
			return redirect('train-c-plan-detail', hashid=hashid)
	else: form = TrainingDepForm(instance=dep)
	context = {
		'group': group, 'form': form, 'tplan': tplan, 'page': 'pdetail',
		'title': 'Altera Ekipa', 'legend': 'Altera Ekipa'
	}
	return render(request, 'training/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cTDepDelete(request, hashid, pk):
	dep = get_object_or_404(TrainingDep, pk=pk)
	dep.delete()
	messages.success(request, f'Delete sucessu.')
	return redirect('train-c-plan-detail', hashid=hashid)

### END TRAINING DEPARTMENT ###


### TRAINNING EMP GAP ###
@login_required
@allowed_users(allowed_roles=['unit'])
def cTEmpGapAdd(request, hashid):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	if request.method == 'POST':
		form = TrainingPlanEmpGapForm(unit,tplan, request.POST)
		if form.is_valid():
			newid, _ = getnewid(TrainingPlanGap)
			gap = request.POST.get('gap')
			tgap = get_object_or_404(TrainingGap, pk=gap)
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = tplan
			instance.employee = tgap.employee
			instance.user = request.user
			instance.datetime = datetime.datetime.now()
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('train-c-plan-detail', hashid=hashid)
	else:
		form = TrainingPlanEmpGapForm(unit,tplan)
	context = {
		'group': group,
		'form': form,
		'tplan': tplan,
		'page': 'pdetail',
		'title': 'Aumenta Funsionario Baseia ba GAP Analysis',
		'legend': 'Aumenta Funsionario Baseia ba GAP Analysis'
	}
	return render(request, 'training/form2.html', context)


@login_required
@allowed_users(allowed_roles=['unit'])
def cTEmpGapUpdate(request, hashid, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	tgap = get_object_or_404(TrainingPlanGap, pk=pk)
	if request.method == 'POST':
		form = TrainingPlanEmpGapForm(unit,tplan, request.POST, instance=tgap)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('train-c-plan-detail', hashid=hashid)
	else:
		form = TrainingPlanEmpGapForm(unit,tplan, instance=tgap)
	context = {
		'group': group,
		'form': form,
		'tplan': tplan,
		'page': 'pdetail',
		'title': 'Altera Funsionario Baseia ba GAP Analysis',
		'legend': 'Altera Funsionario Baseia ba GAP Analysis'
	}
	return render(request, 'training/form2.html', context)


@login_required
@allowed_users(allowed_roles=['unit'])
def cTEmpGapDelete(request, hashid, pk):
	tgap = get_object_or_404(TrainingPlanGap, pk=pk)
	tgap.delete()
	messages.success(request, f'Altera sucessu.')
	return redirect('train-c-plan-detail', hashid=hashid)

### END TRAINNING EMP GAP ###


@login_required
@allowed_users(allowed_roles=['unit'])
def cTEmpDelete(request, hashid, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	objects = get_object_or_404(TrainingEmp, pk=pk)
	objects.delete()
	messages.success(request, f'Hapafa sucessu.')
	return redirect('train-c-plan-detail', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['unit'])
def cTPlanLock(request, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	objects = get_object_or_404(TrainingPlan, pk=pk)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Taka.')
	return redirect('train-c-plan-detail', hashid=objects.hashed)

@login_required
@allowed_users(allowed_roles=['unit'])
def cTPlanUnLock(request, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	objects = get_object_or_404(TrainingPlan, pk=pk)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Loke.')
	return redirect('train-c-plan-detail', hashid=objects.hashed)

@login_required
@allowed_users(allowed_roles=['unit'])
def cTPlanSend(request, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	objects = get_object_or_404(TrainingPlan, pk=pk)
	objects.is_send = True
	objects.is_approve = True
	objects.save()
	messages.success(request, f'Manda ona.')
	return redirect('train-c-plan-detail', hashid=objects.hashed)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def cTPlanCertify(request, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	objects = get_object_or_404(TrainingPlan, pk=pk)
	objects.is_certify = True
	objects.save()
	messages.success(request, f'Certifika ona.')
	return redirect('train-hr-plan-detail', hashid=objects.hashed)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deTPlanApprove(request, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	objects = get_object_or_404(TrainingPlan, pk=pk)
	objects.is_approve = True
	objects.save()
	messages.success(request, f'Aprova ona.')
	return redirect('train-de-plan-detail', hashid=objects.hashed)
#
@login_required
@allowed_users(allowed_roles=['unit'])
def cTCritAdd(request, hashid, pk):
	group = request.user.groups.all()[0].name
	_, dep = c_dep(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temp = get_object_or_404(TrainingEmp, pk=pk)
	if request.method == 'POST':
		newid, _ = getnewid(TrainingCriteria)
		form = TrainingCritForm1(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = tplan
			instance.training_emp = temp
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('train-c-crit-list', hashid=hashid, pk=pk)
	else: form = TrainingCritForm1()
	context = {
		'group': group, 'form': form, 'tplan': tplan, 'temp': temp, 'page': 'ccrit',
		'title': 'Kriteria Materia', 'legend': 'Aumenta Kriteria'
	}
	return render(request, 'training/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cTCritUpdate(request, hashid, pk, pk2):
	group = request.user.groups.all()[0].name
	_, dep = c_dep(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temp = get_object_or_404(TrainingEmp, pk=pk)
	obejcts = get_object_or_404(TrainingCriteria, pk=pk2)
	if request.method == 'POST':
		form = TrainingCritForm1(request.POST, instance=obejcts)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('train-c-crit-list', hashid=hashid, pk=pk)
	else: form = TrainingCritForm1(instance=obejcts)
	context = {
		'group': group, 'form': form, 'tplan': tplan, 'temp': temp, 'page': 'ccrit',
		'title': 'Altera Kriteria', 'legend': 'Altera Kriteria'
	}
	return render(request, 'training/form.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cTCritDelete(request, hashid, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(TrainingCriteria, pk=pk2)
	objects.delete()
	messages.success(request, f'Hapafa sucessu.')
	return redirect('train-c-crit-list', hashid=hashid, pk=pk)
###
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTCritAdd(request, hashid, pk):
	group = request.user.groups.all()[0].name
	_, dep = c_dep(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temp = get_object_or_404(TrainingEmp, pk=pk)
	if request.method == 'POST':
		newid, _ = getnewid(TrainingCriteria)
		form = TrainingCritForm2(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.plan = tplan
			instance.training_emp = temp
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('train-hr-crit-list', hashid=hashid, pk=pk)
	else: form = TrainingCritForm2()
	context = {
		'group': group, 'form': form, 'tplan': tplan, 'temp': temp, 'page': 'hrcrit',
		'title': 'Kriteria Materia', 'legend': 'Aumenta Kriteria'
	}
	return render(request, 'training/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTAddSubject(request, pk):
	group = request.user.groups.all()[0].name
	objects = TrainingEmp.objects.get(pk=pk)
	if request.method == 'POST':
		form = TrainingEmpSubjectForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('train-hr-plan-detail', hashid=objects.plan.hashed)
	else: form = TrainingEmpSubjectForm(instance=objects)
	context = {
		'group': group, 'form': form,
		'title': 'Aumenta Materia', 'legend': 'Aumenta Materia'
	}
	return render(request, 'training/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTCritUpdate(request, hashid, pk, pk2):
	group = request.user.groups.all()[0].name
	_, dep = c_dep(request.user)
	tplan = get_object_or_404(TrainingPlan, hashed=hashid)
	temp = get_object_or_404(TrainingEmp, pk=pk)
	obejcts = get_object_or_404(TrainingCriteria, pk=pk2)
	if request.method == 'POST':
		form = TrainingCritForm2(request.POST, instance=obejcts)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('train-hr-crit-list', hashid=hashid, pk=pk)
	else: form = TrainingCritForm2(instance=obejcts)
	context = {
		'group': group, 'form': form, 'tplan': tplan, 'temp': temp, 'page': 'hrcrit',
		'title': 'Altera Kriteria', 'legend': 'Altera Kriteria'
	}
	return render(request, 'training/form.html', context)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTCritDelete(request, hashid, pk, pk2):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(TrainingCriteria, pk=pk2)
	objects.delete()
	messages.success(request, f'Hapafa sucessu.')
	return redirect('train-hr-crit-list', hashid=hashid, pk=pk)