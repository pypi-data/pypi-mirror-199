from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q, Sum
from custom.models import Unit, Department, Position
from contract.models import Contract, ContractType, EmpPosition, EmpSalary, EmpPlacement, Category
from employee.models import Employee, CurEmpDivision, CurEmpPosition, FIDNumber, Photo
from contract.models import Contract, EmpPosition
from payroll.models import Salary

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PayrollDash(request):
	group = request.user.groups.all()[0].name
	cats = Category.objects.all()
	poss = Position.objects.all()
	obj_cats,obj_poss = [],[]
	for i in cats:
		i_a = Contract.objects.filter(category=i, is_active=True).count()
		i_b = Salary.objects.filter(contract__category=i, contract__is_active=True).aggregate(Sum('net')).get('net__sum', 0.00)
		obj_cats.append([i,i_a,i_b])
	for j in poss:
		j_a = Contract.objects.filter(position=j, is_active=True).count()
		j_b = Salary.objects.filter(contract__position=j, contract__is_active=True)\
			.aggregate(Sum('net')).get('net__sum', 0.00)
		obj_poss.append([j,j_a,j_b])
	context = {
		'group': group, 'obj_cats': obj_cats, 'obj_poss': obj_poss,
		'title': 'Painel Payroll', 'legend': 'Painel Payroll'
	}
	return render(request, 'payroll/dash.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryList(request):
	group = request.user.groups.all()[0].name
	objects = Contract.objects.filter(is_active=True).all()
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Salariu', 'legend': 'Lista Salariu'
	}
	return render(request, 'payroll/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryCatList(request, pk):
	group = request.user.groups.all()[0].name
	cat = get_object_or_404(Category, pk=pk)
	objects = Contract.objects.filter(is_active=True, category=cat).prefetch_related('salary').all()
	context = {
		'group': group, 'cat': cat, 'objects': objects,
		'title': 'Lista Salariu', 'legend': 'Lista Salariu'
	}
	return render(request, 'payroll/cat_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryPosList(request, pk):
	group = request.user.groups.all()[0].name
	pos = get_object_or_404(Position, pk=pk)
	objects = Contract.objects.filter(is_active=True, position=pos).prefetch_related('salary').all()
	context = {
		'group': group, 'pos': pos, 'objects': objects,
		'title': 'Lista Salariu', 'legend': 'Lista Salariu'
	}
	return render(request, 'payroll/pos_list.html', context)
