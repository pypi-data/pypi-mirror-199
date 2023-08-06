from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.hrSchoList, name='hr-scho-list'),
    path('raw/data/', views.hrSchoRawData, name='hr-raw-data'),
    path('raw/data/<year>/', views.hrSchoRawDataYear, name='hr-raw-data-year'),
    path('add/', views.hrSchoPlanAdd, name='hr-scho-add'),
    path('update/<str:hashid>/', views.hrSchoPlanUpdate, name='hr-scho-update'),
    path('detail/<str:hashid>/', views.hrSchoDetail, name='hr-scho-detail'),
    path('lock/<str:hashid>/', views.hrSchoPlanLock, name='hr-scho-lock'),
    path('emp/add/<str:hashid>/', views.hrSchoEmpAdd, name='hr-scho-emp-add'),
    path('emp/update/<str:hashid>/<str:hashid2>/', views.hrSchoEmpUpdate, name='hr-scho-emp-update'),
    path('emp/delete/<str:hashid>/<str:hashid2>/', views.hrSchoEmpDelete, name='hr-scho-emp-delete'),
    path('emp/update/att/<str:hashid>/<str:pk>/', views.hrSchoUpdaAtt, name='hr-scho-emp-update-att'),
    path('emp/detail/<str:hashid>/<str:hashid2>/', views.hrSchoEmpDetail, name='hr-scho-emp-detail'),
    path('emp/add/thesis/<str:hashid>/<str:hashid2>/', views.hrSchoEmpThesisAdd, name='hr-scho-emp-add-thesis'),
    path('emp/progress/add/<str:hashid>/<str:hashid2>/', views.hrSchoEmpProgAdd, name='hr-scho-emp-progress-add'),
    path('emp/progress/update/<str:hashid>/<str:hashid2>/<int:pk>/', views.hrSchoEmpProgUpdate, name='hr-scho-emp-progress-update'),
]