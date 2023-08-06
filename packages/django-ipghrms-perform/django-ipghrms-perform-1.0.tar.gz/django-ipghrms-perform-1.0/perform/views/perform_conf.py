import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from employee.models import CurEmpDivision, Employee
from contract.models import Category, Contract, EmpPosition
from perform.models import ParameterA, ParameterB, Eval, EvalDetA, EvalDetB, EvalYear, \
EvalPlanning, EvalPlanningA, EvalPlanningB, EvalPreAssessment, EvalPreAssessmentA, EvalSelf, \
EvalSelfDetA, EvalSelfDetB
from perform.forms import *
from settings_app.utils import getnewid

@login_required
def PerformConfDash(request):
	group = request.user.groups.all()[0].name
	paramas = ParameterA.objects.filter().all()
	parambs = ParameterB.objects.filter().all()
	years = EvalYear.objects.filter().all().order_by('year')
	employee = Employee.objects.filter(status_id=1).exclude(curempdivision__de__pk=1)
	ayear = EvalYear.objects.filter(is_active=True).last()
	objects = []
	for emp in employee:
		evalplan = EvalPlanning.objects.filter(employee=emp, year=ayear).last()
		evalpreass = EvalPreAssessment.objects.filter(employee=emp, year=ayear).last()
		check_plan = EvalPlanningA.objects.filter(eval=evalplan).exists()
		evalself = EvalSelf.objects.filter(employee=emp, year=ayear).last()
		eval = Eval.objects.filter(employee=emp, year=ayear).last()
		objects.append([emp,evalplan, evalpreass, check_plan, evalself, eval])


	context = {
		'group': group, 'years': years, 'paramas': paramas, 'parambs': parambs,
		'title': 'Konfigurasaun Avaliasaun', 'legend': 'Konfigurasaun Avaliasaun', \
		'objects': objects, 'ayear':ayear.year
	}
	return render(request, 'perform2_conf/conf_dash.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerformYearActive(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(EvalYear, pk=pk)
	objects2 = EvalYear.objects.filter().exclude(pk=pk).all()
	objects.is_active = True
	objects.save()
	for i in objects2:
		i.is_active = False
		i.save()
	messages.success(request, f'Ativa sucessu.')
	return redirect('eval-conf-dash')
#
@login_required
def ParameterAAdd(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid, _ = getnewid(ParameterA)
		form = ParameterAForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.save()
			messages.success(request, f'Altera sucessu.')
			if group == "unit": return redirect('eval-conf-dash')
	else: form = ParameterAForm()
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Aumenta Parameter', 'legend': 'Aumenta Parameter'
	}
	return render(request, 'perform2_conf/form.html', context)

@login_required
def ParameterAUpdate(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(ParameterA, pk=pk)
	if request.method == 'POST':
		form = ParameterAForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			messages.success(request, f'Altera sucessu.')
			if group == "unit": return redirect('eval-conf-dash')
	else: form = ParameterAForm(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Hadia Parameter', 'legend': 'Hadia Parameter'
	}
	return render(request, 'perform2_conf/form.html', context)
#
@login_required
def ParameterBAdd(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid, _ = getnewid(ParameterB)
		form = ParameterBForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.save()
			messages.success(request, f'Altera sucessu.')
			if group == "unit": return redirect('eval-conf-dash')
	else: form = ParameterBForm()
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Aumenta Parameter', 'legend': 'Aumenta Parameter'
	}
	return render(request, 'perform2_conf/form.html', context)

@login_required
def ParameterBUpdate(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(ParameterB, pk=pk)
	if request.method == 'POST':
		form = ParameterBForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('eval-conf-behavior-list')
	else: form = ParameterBForm(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Hadia Parameter', 'legend': 'Hadia Parameter'
	}
	return render(request, 'perform2_conf/form.html', context)


##BEHAVIORS

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerformConfBehaviorList(request):
	group = request.user.groups.all()[0].name
	objects = ParameterB.objects.filter().all()


	context = {
		'group': group,
		'title': 'Lista Behavior', 'legend': 'Lista Behavior', \
		'objects': objects, 
	}
	return render(request, 'perform2/behavior_list.html', context)

@login_required
def PerformConfBehaviorAdd(request, hashid):
	objects = get_object_or_404(EvalPlanning, hashed=hashid)
	group = request.user.groups.all()[0].name
	parameter = ParameterB.objects.filter().all()
	for par in parameter:
		newid, new_hashid = getnewid(EvalPlanningB)
		obj = EvalPlanningB(
			id=newid,
			eval = objects,
			hashed = new_hashid,
			parameter = par,
			user = request.user
		)
		obj.save()
	messages.success(request, 'Susesu Aumenta')
	if group == 'hr':
		return redirect('eval-conf-plan-detail', hashid)
	else:
		return redirect('staff-perform-plan-detail',hashid)