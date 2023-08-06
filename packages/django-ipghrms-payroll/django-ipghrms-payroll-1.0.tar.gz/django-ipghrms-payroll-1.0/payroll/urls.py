from django.urls import path
from . import views

urlpatterns = [
	path('dash/', views.PayrollDash, name="payroll-dash"),
	path('salary/list/', views.SalaryList, name="payroll-sal-list"),
	path('salary/cat/list/<str:pk>/', views.SalaryCatList, name="payroll-sal-cat-list"),
	path('salary/pos/list/<str:pk>/', views.SalaryPosList, name="payroll-sal-pos-list"),
	path('salary/add/<str:hashid>/', views.SalaryAdd, name="payroll-sal-add"),
	path('salary/update/<str:hashid>/', views.SalaryUpdate, name="payroll-sal-update"),
	path('salary/lock/<str:hashid>/', views.SalaryLock, name="payroll-sal-lock"),
	path('salary/unlock/<str:hashid>/', views.SalaryUnLock, name="payroll-sal-unlock"),
	path('salary/confirm/<str:hashid>/', views.SalaryConfirm, name="payroll-sal-confirm"),
	path('salary/rem/<str:hashid>/', views.SalaryRem, name="payroll-sal-rem"),
]