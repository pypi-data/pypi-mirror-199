import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import AttendanceTotal
from contract.models import Contract, EmpSalary
from employee.models import ContactInfo, CurEmpDivision, Employee
from payslip.forms import PaySlipDaysForm, PaySlipDetailForm, PaySlipForm
from settings_app.decorators import allowed_users
from django.contrib import messages
from payslip.models import PaySlip, PaySlipDetail, PaySlipTo
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipAdd(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	empdiv = CurEmpDivision.objects.filter(employee=emp).first()
	cont = Contract.objects.filter(employee=emp, is_active=True).first()
	contact = ContactInfo.objects.filter(employee=emp).first()
	if request.method == 'POST':
		newid, new_hashid = getnewid(PaySlip)
		form = PaySlipForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.category = cont.category
			instance.email = contact.email
			if empdiv.unit: instance.unit = empdiv.unit
			elif empdiv.department: instance.dep = empdiv.department
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('payslip-list', hashid=hashid)
	else: form = PaySlipForm()
	context = {
		'form': form, 'cont': cont, 'emp': emp, 'page': 'list',
		'title': 'Aumenta PaySlip', 'legend': 'Aumenta PaySlip'
	}
	return render(request, 'payslip/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipUpdate(request, pk, hashid):
	emp = get_object_or_404(Employee, pk=pk)
	objects = get_object_or_404(PaySlip, hashed=hashid)
	cont = Contract.objects.filter(employee=emp, is_active=True).first()
	if request.method == 'POST':
		form = PaySlipForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('payslip-list', hashid=emp.hashed)
	else: form = PaySlipForm(instance=objects)
	context = {
		'form': form, 'emp': emp, 'cont': cont, 'page': 'list',
		'title': 'Altera PaySlip', 'legend': 'Altera PaySlip'
	}
	return render(request, 'payslip/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipDetailAdd(request, hashid):
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(PaySlipDetail)
		form = PaySlipDetailForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.payslip = payslip
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('payslip-detail', hashid=hashid)
	else: form = PaySlipDetailForm()
	context = {
		'form': form, 'payslip': payslip, 'page': 'det',
		'title': 'Aumenta Desrisaun', 'legend': 'Aumenta Desrisaun'
	}
	return render(request, 'payslip/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipDetailUpdate(request, hashid, pk):
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	objects = get_object_or_404(PaySlipDetail, pk=pk)
	if request.method == 'POST':
		form = PaySlipDetailForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('payslip-detail', hashid=hashid)
	else: form = PaySlipDetailForm(instance=objects)
	context = {
		'form': form, 'payslip': payslip, 'page': 'det',
		'title': 'Aumenta Desrisaun', 'legend': 'Aumenta Desrisaun'
	}
	return render(request, 'payslip/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipDetailRef1(request, hashid, pk):
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	emp = payslip.employee
	cont = Contract.objects.filter(employee=emp, is_active=True).first()
	empsal = EmpSalary.objects.filter(contract=cont).first()
	objects = get_object_or_404(PaySlipDetail, pk=pk)
	objects.month_sallary = empsal.amount
	objects.tax = empsal.amount
	if payslip.category_id == 3: 
		objects.tax_min = float(empsal.amount)*0.1
		objects.net = float(empsal.amount) - float(empsal.amount)
	elif payslip.category_id == 4: 
		objects.tax_min = (float(empsal.amount)-float(500))*0.1
		objects.net = float(empsal.amount) - (float(empsal.amount)-float(500))*0.1
	
	objects.save()
	messages.success(request, f'Altera sucessu.')
	return redirect('payslip-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipDetailRef2(request, hashid, pk):
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	emp = payslip.employee
	cont = Contract.objects.filter(employee=emp, is_active=True).first()
	empsal = EmpSalary.objects.filter(contract=cont).first()
	objects = get_object_or_404(PaySlipDetail, pk=pk)
	objects.month_sallary = 24
	objects.tax = 0
	objects.tax_min = 0
	objects.net = 24
	objects.save()
	messages.success(request, f'Altera sucessu.')
	return redirect('payslip-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipDaysAdd(request, hashid):
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	if request.method == 'POST':
		form = PaySlipDaysForm(request.POST, instance=payslip)
		if form.is_valid():
			form.save()
			messages.success(request, f'Ajusta sucessu.')
			return redirect('payslip-detail', hashid=hashid)
	else: form = PaySlipDaysForm(instance=payslip)
	context = {
		'form': form, 'payslip': payslip, 'page': 'det',
		'title': 'Ajusta Absensia', 'legend': 'Ajusta Absensia'
	}
	return render(request, 'payslip/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipAdjust(request, hashid):
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	emp = payslip.employee
	first = PaySlipDetail.objects.filter(payslip=payslip).first()
	last = PaySlipDetail.objects.filter(payslip=payslip).last()
	total = first.net - last.net
	tot_falta = AttendanceTotal.objects.filter(employee=emp, year__year=payslip.inv_date.year, month__code=payslip.inv_date.month).first()
	tot = float(total) / float(payslip.days)
	tot = tot * tot_falta.total
	payslip.net = float(total)-float(tot)
	payslip.save()
	messages.success(request, f'Altera sucessu.')
	return redirect('payslip-detail', hashid=hashid)
##
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PaySlipLock(request, hashid):
	payslip = get_object_or_404(PaySlip, hashed=hashid)
	payslip.is_lock = True
	payslip.save()
	messages.success(request, f'Taka.')
	return redirect('payslip-detail', hashid=hashid)