import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from employee.models import CurEmpDivision, Employee
from contract.models import Category, Contract, EmpPosition
from perform.models import ParameterA, ParameterB, Eval, EvalDetA, EvalDetB
from perform.forms import *
from settings_app.utils import getnewid
from log.utils import log_action

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def PerformDetAImport(request, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(Eval, hashed=hashid)
	objects = ParameterA.objects.filter().all()
	for i in objects:
		newid, new_hashid = getnewid(EvalDetA)
		check = EvalDetA.objects.filter(eval=eval, parameter=i).first()
		if not check:
			obj = EvalDetA(id=newid, eval=eval, parameter=i,\
				user=request.user, hashed=new_hashid)
			obj.save()
			messages.success(request, f'Importa sucessu.')
		else:
			messages.warning(request, f'"{check.parameter}" existe ona.')
	return redirect('c-eval-detail', hashid=hashid)


## NEW HERE
@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformDetAUpdate(request, pk, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(Eval, pk=pk)
	objects = get_object_or_404(EvalDetA, hashed=hashid)
	plan = objects.parameter.eval
	if request.method == 'POST':
		form = EvalDetAForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			log_action(request, model='evaluator_evalution_ind_objective', action="Update",field_id=objects.pk)
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=eval.hashed, hashid2=plan.hashed)
	else: form = EvalDetAForm(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Aumenta Valor Avaliasaun',
		'legend': 'Aumenta Valor Avaliasaun',
		'page': 'eval-a', 'plan':plan, 'objects':objects
	}
	return render(request, 'perform2/form_det.html', context)

@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformDetBUpdate(request, pk, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(Eval, pk=pk)
	objects = get_object_or_404(EvalDetB, hashed=hashid)
	plan = objects.parameter.eval
	if request.method == 'POST':
		form = EvalDetBForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			log_action(request, model='evaluator_evalution_prof_behavior', action="Update",field_id=objects.pk)
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=eval.hashed, hashid2=plan.hashed)
	else: form = EvalDetBForm(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Aumenta Valor Avaliasaun',
		'legend': 'Aumenta Valor Avaliasaun',
		'page': 'eval-b', 'plan':plan, 'objects':objects
	}
	return render(request, 'perform2/form_det.html', context)


# work: NEW HERE
@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformEval4Update(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, pk=pk)
	if request.method == 'POST':
		form = EvalForm4(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=objects.hashed, hashid2=plan.hashed)
	else: form = EvalForm4(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Prienche JUSTIFICATION OF OUTSTANDING PERFORMANCE',
		'legend': 'Prienche JUSTIFICATION OF OUTSTANDING PERFORMANCE',
		'objects':objects, 'page':'form-4', 'plan':plan
	}
	return render(request, 'perform2/form_det.html', context)

@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformEval5Update(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, pk=pk)
	if request.method == 'POST':
		form = EvalForm5(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=objects.hashed, hashid2=plan.hashed)
	else: form = EvalForm5(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Prienche Paramenter of individual objectives',
		'legend': 'Prienche Paramenter of individual objectives',
		'objects':objects, 'page':'form-4', 'plan':plan
	}
	return render(request, 'perform2/form_det.html', context)

@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformEval6Update(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, pk=pk)
	if request.method == 'POST':
		form = EvalForm6(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=objects.hashed, hashid2=plan.hashed)
	else: form = EvalForm6(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Prienche Paramenter professional behaviors',
		'legend': 'Prienche Paramenter professional behaviors',
		'objects':objects, 'page':'form-4', 'plan':plan
	}
	return render(request, 'perform2/form_det.html', context)

@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformEval7Update(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, pk=pk)
	if request.method == 'POST':
		form = EvalForm7(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=objects.hashed, hashid2=plan.hashed)
	else: form = EvalForm7(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Prienche PRECOGNITION OF MERIT (OUTSTANDING PERFORMANCE)',
		'legend': 'Prienche PRECOGNITION OF MERIT (OUTSTANDING PERFORMANCE)',
		'objects':objects, 'page':'form-4', 'plan':plan
	}
	return render(request, 'perform2/form_det.html', context)

@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformEval8Update(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, pk=pk)
	if request.method == 'POST':
		form = EvalForm8(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=objects.hashed, hashid2=plan.hashed)
	else: form = EvalForm8(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Prienche JUSTIFICATION OF NON-EVALUATION',
		'legend': 'Prienche JUSTIFICATION OF NON-EVALUATION',
		'objects':objects, 'page':'form-4', 'plan':plan
	}
	return render(request, 'perform2/form_det.html', context)

@login_required
@allowed_users(allowed_roles=['unit','de', 'deputy'])
def PerformEval9Update(request, hashid, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, pk=pk)
	if request.method == 'POST':
		form = EvalForm9(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			
			messages.success(request, f'Aumenta sucessu.')
			return redirect('eval-evaluator-detail', hashid=objects.hashed, hashid2=plan.hashed)
	else: form = EvalForm9(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Prienche EXPECTATIONS, CONDITIONS AND / OR REQUIREMENTS FOR PERSONAL AND PROFESSIONAL DEVELOPMENT',
		'legend': 'Prienche EXPECTATIONS, CONDITIONS AND / OR REQUIREMENTS FOR PERSONAL AND PROFESSIONAL DEVELOPMENT',
		'objects':objects, 'page':'form-4', 'plan':plan
	}
	return render(request, 'perform2/form_det.html', context)






@login_required
@allowed_users(allowed_roles=['unit','hr'])
def PerformDetBImport(request, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(Eval, hashed=hashid)
	objects = ParameterB.objects.filter().all()
	for i in objects:
		newid, new_hashid = getnewid(EvalDetB)
		check = EvalDetB.objects.filter(eval=eval, parameter=i).first()
		if not check:
			obj = EvalDetB(id=newid, eval=eval, parameter=i,\
				user=request.user, hashed=new_hashid)
			obj.save()
			messages.success(request, f'Importa sucessu.')
		else:
			messages.warning(request, f'"{check.parameter}" existe ona.')
	return redirect('c-eval-detail', hashid=hashid)


### SELF
@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformDetAImport(request, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(EvalSelf, hashed=hashid)
	objects = ParameterA.objects.filter().all()
	for i in objects:
		newid, new_hashid = getnewid(EvalSelfDetA)
		check = EvalSelfDetA.objects.filter(eval=eval, parameter=i).first()
		if not check:
			obj = EvalSelfDetA(id=newid, eval=eval, parameter=i,\
				user=request.user, hashed=new_hashid)
			obj.save()
			messages.success(request, f'Importa sucessu.')
		else:
			messages.warning(request, f'"{check.parameter}" existe ona.')
	return redirect('eval-self-detail', hashid=hashid)



#
@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformDetBImport(request, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(EvalSelf, hashed=hashid)
	objects = ParameterB.objects.filter().all()
	for i in objects:
		newid, new_hashid = getnewid(EvalSelfDetB)
		check = EvalSelfDetB.objects.filter(eval=eval, parameter=i).first()
		if not check:
			obj = EvalSelfDetB(id=newid, eval=eval, parameter=i,\
				user=request.user, hashed=new_hashid)
			obj.save()
			messages.success(request, f'Importa sucessu.')
		else:
			messages.warning(request, f'"{check.parameter}" existe ona.')
	return redirect('eval-self-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformDetBUpdateBack(request, pk, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(EvalSelf, pk=pk)
	objects = get_object_or_404(EvalSelfDetB, hashed=hashid)
	if request.method == 'POST':
		form = EvalSelfDetBForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('eval-self-detail', hashid=eval.hashed)
	else: form = EvalSelfDetBForm(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form,
		'title': 'Altera Avaliasaun ba Paramenter B',
		'legend': 'Altera Avaliasaun ba Paramenter B'
	}
	return render(request, 'perform2/form_det.html', context)

