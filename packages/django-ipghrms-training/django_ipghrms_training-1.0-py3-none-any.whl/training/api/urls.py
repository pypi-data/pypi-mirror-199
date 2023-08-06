from django.urls import path
from . import views

urlpatterns = [
	path('year/', views.APITrainYear.as_view()),
	path('dep/', views.APITrainDep.as_view()),
	path('unit/', views.APITrainUnit.as_view()),
]