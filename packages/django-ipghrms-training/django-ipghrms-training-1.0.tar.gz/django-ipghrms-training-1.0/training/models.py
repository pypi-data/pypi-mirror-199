from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from employee.models import Employee
from custom.models import EducationLevel, Unit, Department, Position, University, Country
from settings_app.upload_utils import upload_training,upload_scholarship, upload_training_subject
from django.core.validators import FileExtensionValidator
from django.utils.timesince import timesince
from contract.models import EmpContractToR

class TType(models.Model):
	name = models.CharField(max_length=50, null=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class TYear(models.Model):
	year = models.IntegerField(null=True)
	def __str__(self):
		template = '{0.year}'
		return template.format(self)

class TCriteria(models.Model):
	subject = models.CharField(max_length=200, null=True)
	category = models.CharField(choices=[('Unidade','Unidade'),('RH','RH')], max_length=10, null=True, blank=False)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		template = '{0.category} - {0.subject}'
		return template.format(self)
	

class TrainingGap(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="trainningempgap")
	tor = models.ForeignKey(EmpContractToR, on_delete=models.SET_NULL, null=True, blank=True)
	comment = models.CharField(max_length=255, null=True, blank=True)
	datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	is_done = models.BooleanField(default=False, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee} - {0.comment} - {0.comment}'
		return template.format(self)


class TrainingPlan(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Unidade")
	dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Departamentu")
	type = models.ForeignKey(TType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipu")
	contract_date = models.DateField(null=True, verbose_name="Data Kontrato",blank=True)
	start_date = models.DateField(null=True, verbose_name="Data Hahu",blank=True)
	end_date = models.DateField(null=True, verbose_name="Data Remata",blank=True)
	year = models.ForeignKey(TYear, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tinan")
	subject = models.CharField(max_length=300, null=True, blank=True, verbose_name="Materia Formasaun")
	target = models.IntegerField(null=True, blank=True)
	place = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fatin")
	duration = models.IntegerField(null=True, blank=True, verbose_name="Durasaun (loron)")
	file = models.FileField(upload_to=upload_training, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Upload PDF")
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	is_send = models.BooleanField(default=False, null=True, blank=True)
	is_certify = models.BooleanField(default=False, null=True, blank=True)
	is_approve = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.unit} - {0.year}'
		return template.format(self)

class TrainingDep(models.Model):
	plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='trainingdep')
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="trainingdep")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.plan} - {0.department}'
		return template.format(self)


class TrainingPlanGap(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='traininggap')
	plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='traininggap')
	gap = models.ForeignKey(TrainingGap, on_delete=models.CASCADE, null=True, blank=True, related_name="traininggap")
	is_update = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.plan} - {0.gap}'
		return template.format(self)
	

class TrainingEmp(models.Model):
	plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='trainingemp')
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='trainingemp', verbose_name="Pessoal")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name="trainingemp")
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="trainingemp")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="trainingemp")	
	subject = models.FileField(upload_to=upload_training_subject, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Upload Materia")
	diploma = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True, blank=True, related_name="trainingemp")
	is_update = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.plan} - {0.employee}'
		return template.format(self)

class TrainingCriteria(models.Model):
	plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='trainingcriteria')
	training_emp = models.ForeignKey(TrainingEmp, on_delete=models.CASCADE, related_name='trainingcriteria', verbose_name="Pessoal")
	criteria = models.ForeignKey(TCriteria, on_delete=models.CASCADE, related_name='trainingcriteria', verbose_name="Kriteria")
	obs = models.CharField(choices=[('Sim','Sim'),('Lae','Lae')], max_length=6, null=True, blank=False)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.training_emp} - {0.criteria}'
		return template.format(self)




# SCHOLARSHIP
class SType(models.Model):
	name = models.CharField(max_length=50, null=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class SProgress(models.Model):
	name = models.CharField(max_length=50, null=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)


class ScholarshipPlan(models.Model):
	subject = models.CharField(max_length=300, null=True, blank=True, verbose_name="Titlu Bolso Estudo")
	type = models.ForeignKey(SType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipu Bolso Estudo")
	place = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fatin")
	university  = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Universidade")
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
	start_date = models.DateField(null=True, verbose_name="Data Hahu",blank=True)
	end_date = models.DateField(null=True, verbose_name="Data Remata",blank=True)
	year = models.ForeignKey(TYear, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tinan")
	file = models.FileField(upload_to=upload_scholarship, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Upload Pareser")
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.subject} - {0.type}'
		return template.format(self)

class ScholarshipEmp(models.Model):
	scholarship = models.ForeignKey(ScholarshipPlan, on_delete=models.CASCADE, null=True, blank=True, related_name="scholarshipemp")
	emp = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='scholarshipemp', verbose_name="Pessoal")
	thesis = models.CharField(max_length=300, null=True, blank=True, verbose_name="Thesis")
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	is_update = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.scholarship} - {0.emp}'
		return template.format(self)

class ScholarshipEmpProgress(models.Model):
	scholarshipemp = models.ForeignKey(ScholarshipEmp, on_delete=models.CASCADE, null=True, blank=True, related_name="scholarshipempprogress")
	date = models.DateField(null=True, verbose_name="Data",blank=True)
	progress = models.ForeignKey(SProgress, on_delete=models.CASCADE, null=True, blank=True)
	comment = models.TextField(null=True, verbose_name="Remark", blank=True)
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.scholarshipemp} - {0.progress}'
		return template.format(self)
