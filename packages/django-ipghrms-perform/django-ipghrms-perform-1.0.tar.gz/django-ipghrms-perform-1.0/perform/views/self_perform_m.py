import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from employee.models import CurEmpDivision
from contract.models import Contract, EmpPosition
from perform.models import EvalYear, Eval, Evaluator, EvalFinalScore, EvalSelf, EvalType, EvalSelfDetA, EvalSelfDetB, EvalPlanningA, EvalPlanningB
from perform.forms import *
from settings_app.utils import getnewid
from settings_app.user_utils import c_staff, c_dep, c_unit
from log.utils import log_action


@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformAdd(request, page):
	group = request.user.groups.all()[0].name
	if group == "staff": c_emp = c_staff(request.user)
	elif group == "dep": c_emp, _ = c_dep(request.user)
	elif group == "unit": c_emp, _ = c_unit(request.user)
	elif group == "hr": c_emp, _ = c_unit(request.user)
	year = EvalYear.objects.filter(is_active=True).first()
	contract = Contract.objects.filter(employee=c_emp).first()
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	if request.method == 'POST':
		newid, new_hashid = getnewid(EvalSelf)
		form = EvalSelfForm(request.POST)
		if form.is_valid():
			check = Eval.objects.filter(employee=c_emp, year=year).first()
			if check:
				messages.error(request, f'Dadus iha ona.')
				return redirect('eval-self-list')
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = c_emp
			instance.year = year
			instance.category = contract.category
			instance.position = contract.position
			if empdiv.department: instance.department = empdiv.department
			elif empdiv.unit: instance.unit = empdiv.unit
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('eval-self-detail', hashid=new_hashid)
	else: form = EvalSelfForm()
	context = {
		'group': group, 'form': form, 'page': 'list',
		'title': 'Prenche Avaliasaun', 'legend': 'Prenche Avaliasaun'
	}
	return render(request, 'perform2_self/form.html', context)

@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(EvalSelf, hashed=hashid)
	if request.method == 'POST':
		form = EvalSelfForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('eval-self-detail', hashid=hashid)
	else: form = EvalSelfForm(instance=objects)
	context = {
		'group': group, 'eval': objects, 'form': form, 'page': 'det',
		'title': 'Prenche Avaliasaun', 'legend': 'Prenche Avaliasaun'
	}
	return render(request, 'perform2_self/form.html', context)

@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformComUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(EvalSelf, hashed=hashid)
	if request.method == 'POST':
		form = EvalSelfForm2(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('eval-self-detail', hashid=hashid)
	else: form = EvalSelfForm2(instance=objects)
	context = {
		'group': group, 'eval': objects, 'form': form, 'page': 'det',
		'title': 'Hadia Komentariu', 'legend': 'Hadia Komentariu'
	}
	return render(request, 'perform2_self/form.html', context)

@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformRemove(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(EvalSelf, hashed=hashid)
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('eval-self-list')

@login_required
def selfPerformLock(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(EvalSelf, hashed=hashid)
	if objects.ind_date != None and objects.beh_date != None:
		objects.is_lock = True
		objects.save()
		messages.success(request, f'Susesu Chave')
		if group == 'hr':
			return redirect('hr-eval-self-detail', hashid=hashid)
		else:
			return redirect('staff-perform-self-detail', hashid=hashid)
	else:
		messages.error(request, f'Data Seidauk Prienche')
		if group == 'hr':
			return redirect('hr-eval-self-detail', hashid=hashid)
		else:
			return redirect('staff-perform-self-detail', hashid=hashid)


@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformUnlock(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(EvalSelf, hashed=hashid)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Loke.')
	return redirect('eval-self-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformFinish(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(EvalSelf, hashed=hashid)
	objects.is_finish = True
	objects.save()
	messages.success(request, f'Termina.')
	return redirect('eval-self-detail', hashid=hashid)
### NEW

@login_required
def PerfomConfAddSelfEval(request, hashid, year):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	pyear = get_object_or_404(EvalYear, year=year)
	ptype = get_object_or_404(EvalType, pk=3)
	contract = Contract.objects.filter(employee=employee, is_active=True).last()
	empdiv = CurEmpDivision.objects.filter(employee=employee).last()
	newid, new_hashid = getnewid(EvalSelf)
	obj = EvalSelf(
		id = newid,
		hashed= new_hashid,
		year = pyear,
		type = ptype,
		employee = employee,
		category = contract.category,
		position = contract.position,
		department = empdiv.department,
		unit = empdiv.unit
	)
	obj.save()
	objects = EvalPlanningA.objects.filter(eval__employee=employee, eval__year__year=year).all()
	objects2 = EvalPlanningB.objects.filter(eval__employee=employee, eval__year__year=year).all()
	
	
	for i in objects:
		newid2, new_hashid2 = getnewid(EvalSelfDetA)
		obj2 = EvalSelfDetA(id=newid2, eval=obj, parameter=i,\
			user=request.user, hashed=new_hashid2)
		obj2.save()
	for j in objects2:
		newid3, new_hashid3 = getnewid(EvalSelfDetB)
		obj3 = EvalSelfDetB(id=newid3, eval=obj, parameter=j,\
			user=request.user, hashed=new_hashid3)
		obj3.save()
	messages.success(request, 'Susesu Kria Self Evaluation Sheet')
	if group == 'hr':
		return redirect('eval-conf-dash')
	else:
		return redirect('staff-perform-list')


@login_required
def selfPerformDetAUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(EvalSelfDetA, hashed=hashid)
	if request.method == 'POST':
		form = EvalSelfDetAForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			log_action(request, model='self_evaluation_ind_objective', action="Update",field_id=objects.pk)
			messages.success(request, f'Altera sucessu.')
			if group == 'hr':
				return redirect('hr-eval-self-detail', hashid=objects.eval.hashed)
			else:
				return redirect('staff-perform-self-detail', hashid=objects.eval.hashed)

	else: form = EvalSelfDetAForm(instance=objects)
	context = {
		'group': group,  'form': form, 
		'objects':objects, 'page': 'self-a',
		'title': 'Aumenta Self Evaluation Individual Objectives',
		'legend': 'Aumenta Self Evaluation Individual Objectives'
	}
	return render(request, 'perform2/form_det.html', context)

@login_required
def selfPerformDetBUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(EvalSelfDetB, hashed=hashid)
	if request.method == 'POST':
		form = EvalSelfDetBForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.save()
			log_action(request, model='self_evaluation_prof_behavior', action="Update",field_id=objects.pk)
			messages.success(request, f'Altera sucessu.')
			if group == 'hr':
				return redirect('hr-eval-self-detail', hashid=objects.eval.hashed)
			else:
				return redirect('staff-perform-self-detail', hashid=objects.eval.hashed)
	else: form = EvalSelfDetBForm(instance=objects)
	context = {
		'group': group,  'form': form, 
		'objects':objects, 'page': 'self-b',
		'title': 'Aumenta Self Evaluation Professional Objective',
		'legend': 'Aumenta Self Evaluation Professional Objective'
	}
	return render(request, 'perform2/form_det.html', context)


@login_required
def SelfEvalAddObjDate(request, hashid):
	objects = get_object_or_404(EvalSelf,hashed=hashid)
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
			form = SelfDateForm(request.POST, instance=objects)

			if form.is_valid():
				form.save()
			messages.success(request, f'Aumeta Sucessu')
			if group == 'hr':
				return redirect('hr-eval-self-detail', objects.hashed)
			else:
				return redirect('staff-perform-self-detail', objects.hashed)

	else: form = SelfDateForm(instance=objects)
	context = {
		'group': group, 'form': form, 'page': 'unit', 
		'objects':objects, 'page2': 'self',
		'title': 'Aumenta Data', 'legend': 'Aumenta Data'
	}
	return render(request, 'perform2/form.html', context)

@login_required
def SelfEvalAddBehDate(request, hashid):
	objects = get_object_or_404(EvalSelf,hashed=hashid)
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
			form = SelfDate2Form(request.POST, instance=objects)

			if form.is_valid():
				form.save()
			messages.success(request, f'Aumeta Sucessu')
			if group == 'hr':
				return redirect('hr-eval-self-detail', objects.hashed)
			else:
				return redirect('staff-perform-self-detail', objects.hashed)
	else: form = SelfDate2Form(instance=objects)
	context = {
		'group': group, 'form': form, 'page': 'unit',
		'objects':objects,  'page2': 'self',
		'title': 'Aumenta Data', 'legend': 'Aumenta Data'
	}
	return render(request, 'perform2/form.html', context)

@login_required
def SelfEvalAddComment(request, hashid):
	objects = get_object_or_404(EvalSelf,hashed=hashid)
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
			form = SelfCommentForm(request.POST, instance=objects)

			if form.is_valid():
				form.save()
			messages.success(request, f'Aumeta Sucessu')
			if group == 'hr':
					return redirect('hr-eval-self-detail', objects.hashed)
			else:
				return redirect('staff-perform-self-detail', objects.hashed)
	else: form = SelfCommentForm(instance=objects)
	context = {
		'group': group, 'form': form, 'page': 'unit', 'objects':objects, 
		'title': 'Aumenta Komentario', 'legend': 'Aumenta Komentario', 'page2': 'self',
	}
	return render(request, 'perform2/form.html', context)