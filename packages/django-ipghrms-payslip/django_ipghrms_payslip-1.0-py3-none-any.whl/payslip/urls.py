from django.urls import path
from . import views

urlpatterns = [
	path('emp/list/', views.PayslipEmpList, name="payslip-emp-list"),
	path('list/<str:hashid>/', views.PayslipList, name="payslip-list"),
	path('detail/<str:hashid>/', views.PayslipDet, name="payslip-detail"),
	#
	path('add/<str:hashid>/', views.PaySlipAdd, name="payslip-add"),
	path('update/<str:pk>/<str:hashid>/', views.PaySlipUpdate, name="payslip-update"),
	path('days/add/<str:hashid>/', views.PaySlipDaysAdd, name="payslip-days-add"),
	path('adjust/<str:hashid>/', views.PaySlipAdjust, name="payslip-adjust"),
	path('lock/<str:hashid>/', views.PaySlipLock, name="payslip-lock"),
	#
	path('det/add/<str:hashid>/', views.PaySlipDetailAdd, name="payslip-det-add"),
	path('det/update/<str:hashid>/<str:pk>/', views.PaySlipDetailUpdate, name="payslip-det-update"),
	path('det/ref1/<str:hashid>/<str:pk>/', views.PaySlipDetailRef1, name="payslip-det-ref1"),
	path('det/ref2/<str:hashid>/<str:pk>/', views.PaySlipDetailRef2, name="payslip-det-ref2"),
]