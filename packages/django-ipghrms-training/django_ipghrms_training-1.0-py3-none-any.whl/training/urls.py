from django.urls import path
from . import views

urlpatterns = [
	path('c/dash/', views.cTDash, name="train-c-dash"),
	path('c/plan/list/', views.cTPlanList, name="train-c-plan-list"),
	path('c/plan/add/', views.cTPlanAdd, name="train-c-plan-add"),
	path('c/plan/update/<str:hashid>/', views.cTPlanUpdate, name="train-c-plan-update"),
	path('c/plan/detail/<str:hashid>/', views.cTPlanDetail, name="train-c-plan-detail"),
	#
	path('c/raw/data/', views.cTRawData, name="train-c-raw-data"),
	path('raw/data/', views.TRawData, name="train-raw-data"),
	#
	path('c/plan/lock/<str:pk>/', views.cTPlanLock, name="train-c-plan-lock"),
	path('c/plan/unlock/<str:pk>/', views.cTPlanUnLock, name="train-c-plan-unlock"),
	path('c/plan/send/<str:pk>/', views.cTPlanSend, name="train-c-plan-send"),
	path('hr/plan/certify/<str:pk>/', views.cTPlanCertify, name="train-hr-plan-certify"),
	path('de/plan/approve/<str:pk>/', views.deTPlanApprove, name="train-de-plan-approve"),
	#
	path('c/temp/add/<str:hashid>/', views.cTEmpAdd, name="train-c-temp-add"),
	path('c/temp/delete/<str:hashid>/<str:pk>/', views.cTEmpDelete, name="train-c-temp-delete"),
	#
	path('c/crit/list/<str:hashid>/<str:pk>/', views.cTCritList, name="train-c-crit-list"),
	path('c/crit/add/<str:hashid>/<str:pk>/', views.cTCritAdd, name="train-c-crit-add"),
	path('c/crit/update/<str:hashid>/<str:pk>/<str:pk2>/', views.cTCritUpdate, name="train-c-crit-update"),
	path('c/crit/delete/<str:hashid>/<str:pk>/<str:pk2>/', views.cTCritDelete, name="train-c-crit-delete"),
	#
	path('hr/dash/', views.hrTDash, name="train-hr-dash"),
	path('hr/plan/list/', views.hrTPlanList, name="train-hr-plan-list"),
	path('hr/summary/list/', views.hrTSumaryList, name="train-hr-plan-summary"),
	path('hr/summary/year/list/<int:year>/', views.hrTSumaryYearList, name="train-hr-summary-year"),
	path('hr/plan/detail/<str:hashid>/', views.hrTPlanDetail, name="train-hr-plan-detail"),
	path('hr/add/subject/<int:pk>/', views.hrTAddSubject, name="train-hr-add-subject"),
	path('hr/crit/list/<str:hashid>/<str:pk>/', views.hrTCritList, name="train-hr-crit-list"),
	path('hr/update/status/<str:hashid>/<str:pk>/', views.hrTUpdaStatus, name="train-hr-update-status"),
	path('hr/crit/add/<str:hashid>/<str:pk>/', views.hrTCritAdd, name="train-hr-crit-add"),
	path('hr/crit/update/<str:hashid>/<str:pk>/<str:pk2>/', views.hrTCritUpdate, name="train-hr-crit-update"),
	path('hr/crit/delete/<str:hashid>/<str:pk>/<str:pk2>/', views.hrTCritDelete, name="train-hr-crit-delete"),
	###
	path('pr/dash/', views.deTDash, name="train-de-dash"),
	path('pr/plan/list/', views.deTPlanList, name="train-de-plan-list"),
	path('pr/plan/detail/<str:hashid>/', views.deTPlanDetail, name="train-de-plan-detail"),
	path('hr/view/subject/<int:pk>/', views.TrainEmpSubjectFile, name="train-hr-view-subject"),
	path('hr/view/subject/<str:hashid>/', views.TrainEmpPareserFile, name="train-view-pareser"),


	### GAP
	path('unit/gap/<str:pk>/', views.TrainingGapEmpList, name="train-unit-gap-list"),
	path('unit/emp-gap/<str:hashid>/<int:pk>/', views.TrainingGapList, name="train-unit-gap-emp-list"),
	path('unit/emp-gap/add/<str:hashid>/<int:pk>/<str:hashid2>/', views.TrainingGapAdd, name="train-unit-gap-emp-add"),
	path('unit/emp-gap/update/<str:hashid>/<int:pk>/<str:hashid2>/', views.TrainingGapUpdate, name="train-unit-gap-emp-update"),
	path('unit/emp-gap/delete/<str:hashid>/<int:pk>/<str:hashid2>/', views.TrainingGapDelete, name="train-unit-gap-emp-delete"),
	path('unit/emp-gap/lock/<str:hashid>/<int:pk>/', views.TrainingGapLock, name="train-unit-gap-emp-lock"),
    

	### TEAM

	path('c/dep/add/<str:hashid>/', views.cTDepAdd, name="train-team-add"),
	path('c/dep/update/<str:hashid>/<str:pk>/', views.cTDepUpdate, name="train-team-update"),
	path('c/dep/delete/<str:hashid>/<str:pk>/', views.cTDepDelete, name="train-team-delete"),


	### TRAININNG WITH GAP
	path('c/tra-gap/add/<str:hashid>/', views.cTEmpGapAdd, name="train-gap-add"),
	path('c/tra-gap/update/<str:hashid>/<int:pk>/', views.cTEmpGapUpdate, name="train-gap-update"),
	path('c/tra-gap/add/<str:hashid>/<int:pk>/', views.cTEmpGapDelete, name="train-gap-delete"),



]