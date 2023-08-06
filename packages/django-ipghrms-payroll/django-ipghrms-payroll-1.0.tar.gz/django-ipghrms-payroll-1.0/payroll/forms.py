from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import User
from payroll.models import Salary
from custom.models import Position

class DateInput(forms.DateInput):
	input_type = 'date'

class SalaryForm(forms.ModelForm):
	class Meta:
		model = Salary
		fields = ['gross']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['gross'].required = True
		self.helper.layout = Layout(
			Row(
				Column('gross', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)