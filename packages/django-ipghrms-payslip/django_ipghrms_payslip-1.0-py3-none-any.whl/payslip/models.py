from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from pyparsing import null_debug_action
from contract.models import Category
from employee.models import Employee
from custom.models import Unit, Department, Position

class PaySlip(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="payslip")
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="payslip")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="payslip")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Unidade")
	dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Departamentu")
	inv_no = models.CharField(max_length=50, null=True, blank=False, verbose_name="Nu. Fatura")
	inv_date = models.DateField(null=True, blank=False)
	email = models.CharField(max_length=70, null=True, blank=True)
	net = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	tot_falta = models.IntegerField(default=False, null=True, blank=True)
	days = models.IntegerField(default=False, null=True, blank=False, verbose_name="Total Loron")
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee}'
		return template.format(self)

class PaySlipDetail(models.Model):
	payslip = models.ForeignKey(PaySlip, on_delete=models.CASCADE, null=True, blank=True, related_name="payslipdetail")
	desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
	unit = models.CharField(choices=[('Fulan','Fulan')], max_length=6, null=True, blank=False, verbose_name="Unidade")
	qty = models.IntegerField(null=True, blank=True, verbose_name="Qty")
	month_sallary = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	tax = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	tax_min = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	net = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	is_sallary = models.BooleanField(null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.payslip} - {0.desc}'
		return template.format(self)

class PaySlipTo(models.Model):
	payslip = models.ForeignKey(PaySlip, on_delete=models.CASCADE, null=True, blank=True, related_name="payslipto")
	to = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="payslipto")
	address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Enderesu")
	subject = models.CharField(max_length=200, null=True, blank=True, verbose_name="Sujeitu")
	inv_date = models.DateField(null=True, blank=True)
	email = models.CharField(max_length=70, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.payslip} - {0.subject}'
		return template.format(self)