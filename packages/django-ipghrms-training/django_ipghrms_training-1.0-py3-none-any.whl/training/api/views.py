from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from custom.models import Department, Unit
from training.models import TrainingPlan, TrainingDep
from settings_app.user_utils import c_unit, c_dep

class APITrainYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		years = TrainingPlan.objects.filter().distinct().values('year__year').all()
		obj,label = list(),list()
		for i in years:
			objects = []
			if group == 'unit':
				_, unit = c_unit(request.user)
				objects = TrainingPlan.objects.filter((Q(unit=unit)|Q(dep__unit=unit))).all().count()
			else:
				objects = TrainingPlan.objects.filter().all().count()
			label.append(i['year__year'])
			# obj.append(objects)
			obj.append(objects)
		data = { 'legend': 'DISTRIBUISAUN FUNSIONARIO TUIR TREINAMENTO KADA TINAN', 'obj': obj,  'label':label}
		return Response(data)

class APITrainDep(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label= list()
		obj = list()
		legend = 'DISTRIBUISAUN FUNSIONARIO TUIR TREINAMENTO KADA EKIPA'
		if group == 'unit':
			_, unit = c_unit(request.user)
			deps = Department.objects.filter(unit=unit).all()
		else:
			deps = Department.objects.filter().all()
		for i in deps:
			objects = TrainingDep.objects.filter(department=i).all().count()
			label.append(i.name)
			obj.append(objects)
		data = { 'legend':legend, 'label': label, 'obj': obj, }
		return Response(data)

class APITrainUnit(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		units = Unit.objects.filter().all()
		obj,label = [],[]
		for i in units:
			objects = TrainingPlan.objects.filter(unit=i).all().count()
			label.append(i.name)
			obj.append(objects)
		data = { 'label': label, 'obj': obj, }
		return Response(data)
