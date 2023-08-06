from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from payslip.models import PaySlip, PaySlipDetail, PaySlipTo

class DateInput(forms.DateInput):
	input_type = 'date'

class PaySlipForm(forms.ModelForm):
	inv_date = forms.DateField(label='Data', widget=DateInput(), required=True)
	class Meta:
		model = PaySlip
		fields = ['inv_no','inv_date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('inv_no', css_class='form-group col-md-6 mb-0'),
                Column('inv_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PaySlipDetailForm(forms.ModelForm):
	class Meta:
		model = PaySlipDetail
		fields = ['desc','unit','qty','is_sallary']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('desc', css_class='form-group col-md-5 mb-0'),
				Column('unit', css_class='form-group col-md-3 mb-0'),
				Column('qty', css_class='form-group col-md-2 mb-0'),
				Column('is_sallary', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PaySlipDaysForm(forms.ModelForm):
	class Meta:
		model = PaySlip
		fields = ['days']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('days', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
