from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Employee, Photo
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from payslip.models import PaySlip, PaySlipDetail, PaySlipTo
from contract.models import Contract
from attendance.models import AttendanceTotal

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PayslipEmpList(request):
	group = request.user.groups.all()[0].name
	objects = Contract.objects.filter((Q(category_id=3)|Q(category_id=4)), is_active=True).all().order_by('employee__first_name')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Assesor', 'legend': 'Lista Assesor'
	}
	return render(request, 'payslip/emp_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PayslipList(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	img = Photo.objects.get(employee=emp)
	objects = PaySlip.objects.filter(employee=emp).all().order_by('-id')
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'img': img, 'page': 'list',
		'title': 'Lista Payslip', 'legend': 'Lista Payslip'
	}
	return render(request, 'payslip/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PayslipDet(request, hashid):
	group = request.user.groups.all()[0].name
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	emp = payslip.employee
	img = Photo.objects.get(employee=emp)
	objects = PaySlipDetail.objects.filter(payslip=payslip).all()
	first = PaySlipDetail.objects.filter(payslip=payslip).first()
	print(first)
	last = PaySlipDetail.objects.filter(payslip=payslip).last()
	print(last)
	count = int(objects.count())
	total = 0
	if first:
		if first.net:
			if last.net:
				total = first.net - last.net
	p_year = payslip.inv_date.strftime('%Y')
	p_month = payslip.inv_date.strftime('%m')
	tot_attend = AttendanceTotal.objects.filter(employee=emp, year__year=p_year, month__code=p_month).first()
	context = {
		'group': group, 'payslip': payslip, 'emp': emp, 'img': img, 'objects': objects, 'count': count, 
		'total': total, 'tot_attend': tot_attend.total, 'page': 'det',
		'title': 'Detalha Payslip', 'legend': 'Detalha Payslip'
	}
	return render(request, 'payslip/detail.html', context)
