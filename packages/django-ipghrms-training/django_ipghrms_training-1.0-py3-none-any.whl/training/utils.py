from .models import TYear, TrainingPlan
from django.db.models import Q

def sumary_check_year(emp):
	years = TYear.objects.exclude(Q(pk=1)|Q(pk=2)|Q(pk=3))
	data = []
	for j in years:
		tr = TrainingPlan.objects.filter(year=j,trainingemp__employee=emp).count()
		data.append(tr)
	return data

def sumary_check_tr_year(emp, year):
    data = []
    tr = TrainingPlan.objects.filter(year=year,trainingemp__employee=emp)
    data.append(tr)
    return data