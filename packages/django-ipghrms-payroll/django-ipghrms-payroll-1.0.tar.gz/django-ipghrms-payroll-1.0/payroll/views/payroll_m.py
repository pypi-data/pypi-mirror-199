import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from contract.models import Contract, Category
from payroll.models import Salary
from payroll.forms import SalaryForm
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryAdd(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(Salary)
		form = SalaryForm(request.POST)
		if form.is_valid():
			check = Salary.objects.filter(contract=cont).first()
			if check:
				messages.warning(request, f'Dadus iha ona.')
				return redirect('payroll-sal-list')
			gross = form.cleaned_data.get('gross')
			tax = 0
			if gross > 500:
				tax = float(gross)-500
				tax = tax*0.1
			social = float(gross)*0.04
			net = float(gross) - tax - social
			instance = form.save(commit=False)
			instance.id = newid
			instance.contract = cont
			instance.employee = cont.employee
			instance.tax = tax
			instance.social = social
			instance.net = net
			instance.user = request.user
			instance.datetime = datetime.datetime.now()
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Salariu aumenta ona.')
			return redirect('payroll-sal-list')
	else: form = SalaryForm()
	context = {
		'cont': cont, 'form': form, 
		'title': 'Aumenta Salariu', 'legend': 'Aumenta Salariu'
	}
	return render(request, 'payroll/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryUpdate(request, hashid):
	objects = get_object_or_404(Salary, hashed=hashid)
	cont = objects.contract
	if request.method == 'POST':
		form = SalaryForm(request.POST, instance=objects)
		if form.is_valid():
			gross = form.cleaned_data.get('gross')
			tax = 0
			if gross > 500:
				tax = float(gross)-500
				tax = tax*0.1
			social = float(gross)*0.04
			net = float(gross) - tax - social
			instance = form.save(commit=False)
			instance.tax = tax
			instance.social = social
			instance.net = net
			instance.save()
			messages.success(request, f'Salariu altera ona.')
			return redirect('payroll-sal-list')
	else: form = SalaryForm(instance=objects)
	context = {
		'cont': cont, 'form': form,
		'title': 'Altera Salariu', 'legend': 'Altera Salariu'
	}
	return render(request, 'payroll/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryLock(request, hashid):
	objects = get_object_or_404(Salary, hashed=hashid)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Lock.')
	return redirect('payroll-sal-list')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryUnLock(request, hashid):
	objects = get_object_or_404(Salary, hashed=hashid)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Unlock.')
	return redirect('payroll-sal-list')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryConfirm(request, hashid):
	objects = get_object_or_404(Salary, hashed=hashid)
	objects.is_confirm = True
	objects.save()
	messages.success(request, f'Konfirmadu.')
	return redirect('payroll-sal-list')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryRem(request, hashid):
	objects = get_object_or_404(Salary, hashed=hashid)
	objects.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('payroll-sal-list')