from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from pyparsing import null_debug_action
from contract.models import Contract
from employee.models import Employee
from custom.models import Unit, Department, Position

class Salary(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name='salary')
	contract = models.OneToOneField(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name='salary')
	gross = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Gross Salary")
	tax = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	social = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Social Security")
	net = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	is_active = models.BooleanField(default=True, blank=True)
	is_lock = models.BooleanField(default=False, null=True)
	is_confirm = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.employee}: {0.net}'
		return template.format(self)
