import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from employee.models import CurEmpDivision
from contract.models import Contract, EmpPosition
from perform.models import EvalYear, Eval, Evaluator, EvalFinalScore, EvalType, EvalPlanning
from perform.forms import *
from settings_app.utils import getnewid
from settings_app.user_utils import c_unit, c_staff

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformAdd(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	year = EvalYear.objects.filter(is_active=True).first()
	de = EmpPosition.objects.filter(position_id=1).first()
	deputy = EmpPosition.objects.filter(position_id=2).first()
	if request.method == 'POST':
		newid, new_hashid = getnewid(Eval)
		form = EvalForm(c_emp, unit, request.POST)
		if form.is_valid():
			emp = form.cleaned_data.get('employee')
			contract = Contract.objects.filter(employee=emp).first()
			empdiv = CurEmpDivision.objects.get(employee=emp)
			check = Eval.objects.filter(employee=emp, year=year).first()
			if check:
				messages.error(request, f'Dadus iha ona.')
				return redirect('c-eval-list')
			instance = form.save(commit=False)
			instance.id = newid
			instance.year = year
			instance.category = contract.category
			instance.position = contract.position
			if contract.category_id == 5: instance.is_dep = True
			if empdiv.department: instance.department = empdiv.department
			elif empdiv.unit: instance.unit = empdiv.unit
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			obj = Evaluator(id=newid, eval_id=newid, employee=c_emp, unit=unit,\
				position=c_emp.curempposition.position)
			obj.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('c-eval-detail', hashid=new_hashid)
	else: form = EvalForm(c_emp, unit)
	context = {
		'group': group, 'form': form, 'page': 'unit',
		'title': 'Prenche Avaliasaun', 'legend': 'Prenche Avaliasaun'
	}
	return render(request, 'perform2/form_eval.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(Eval, hashed=hashid)
	if request.method == 'POST':
		form = EvalForm2(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('c-eval-detail', hashid=hashid)
	else: form = EvalForm2(instance=objects)
	context = {
		'group': group, 'form': form, 'page': 'unit',
		'title': 'Prenche Avaliasaun', 'legend': 'Prenche Avaliasaun'
	}
	return render(request, 'perform2/form_eval.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformRemove(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(Eval, hashed=hashid)
	objects.delete()
	messages.success(request, f'Hapaga sucessu.')
	return redirect('c-eval-list')



@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformUnlock(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(Eval, hashed=hashid)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Loke.')
	return redirect('c-eval-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformFinish(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(Eval, hashed=hashid)
	objects.is_finish = True
	objects.save()
	messages.success(request, f'Termina.')
	return redirect('c-eval-detail', hashid=hashid)
#
@login_required
def cPerformRefresh(request, hashid, hashid2):
	eval = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, hashed=hashid2)
	sum_a = EvalDetA.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	sum_b = EvalDetB.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	total_a, total_b, total = 0,0,0
	if sum_a: total_a = sum_a
	if sum_b: total_b = sum_b
	total = float(total_a) + float(total_b)
	eval.score_a = total_a
	eval.score_b = total_b
	eval.total = total
	eval.save()
	final = EvalFinalScore.objects.filter(eval=eval).last()
	print(final)
	total = int(total)
	print(total)
	if total >= 80: 
		final.a = total
		final.b, final.c, final.d, final.e = None,None,None,None
	elif total >= 60: 
		final.b = total
		final.a, final.c, final.d, final.e = None,None,None,None
	elif total >= 40: 
		final.c = total
		final.a, final.b, final.d, final.e = None,None,None,None
	elif total >= 20: 
		final.d = total
		final.a, final.b, final.c, final.e, = None,None,None,None
	elif total >= 0: 
		final.e = total
		final.a, final.b, final.c, final.d = None,None,None,None
	final.save()
	messages.success(request, f'Altera sucessu.')
	return redirect('eval-evaluator-detail', hashid=hashid, hashid2=plan.hashed)
###
@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformDate1Update(request, pk):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	evaldate = get_object_or_404(EvalDate, pk=pk)
	eval = evaldate.eval
	if request.method == 'POST':
		form = EvalDateForm1(request.POST, instance=evaldate)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('c-eval-detail', hashid=eval.hashed)
	else: form = EvalDateForm1(instance=evaldate)
	context = {
		'group': group, 'form': form, 'page': 'unit',
		'title': 'Hadia Data', 'legend': 'Hadia Data'
	}
	return render(request, 'perform2/form_eval.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformDate2Update(request, pk):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	evaldate = get_object_or_404(EvalDate, pk=pk)
	eval = evaldate.eval
	if request.method == 'POST':
		form = EvalDateForm2(request.POST, instance=evaldate)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('c-eval-detail', hashid=eval.hashed)
	else: form = EvalDateForm2(instance=evaldate)
	context = {
		'group': group, 'form': form, 'page': 'unit',
		'title': 'Hadia Data', 'legend': 'Hadia Data'
	}
	return render(request, 'perform2/form_eval.html', context)


### NEW
@login_required
def PerfomConfAddEval(request, hashid, year):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	pyear = get_object_or_404(EvalYear, year=year)
	ptype = get_object_or_404(EvalType, pk=4)
	contract = Contract.objects.filter(employee=employee, is_active=True).last()
	empdiv = CurEmpDivision.objects.filter(employee=employee).last()
	newid, new_hashid = getnewid(Eval)
	obj = Eval(
		id = newid,
		hashed= new_hashid,
		year = pyear,
		type = ptype,
		employee = employee,
		is_lock = True,
		category = contract.category,
		position = contract.position,
		department = empdiv.department,
		unit = empdiv.unit
	)
	obj.save()
	plan = EvalPlanning.objects.filter(employee=employee, year__year=year).last()
	objects = EvalPlanningA.objects.filter(eval__employee=employee, eval__year__year=year).all()
	objects2 = EvalPlanningB.objects.filter(eval__employee=employee, eval__year__year=year).all()
	
	
	for i in objects:
		newid2, new_hashid2 = getnewid(EvalDetA)
		obj2 = EvalDetA(id=newid2, eval=obj, parameter=i,\
			user=request.user, hashed=new_hashid2)
		obj2.save()
	for j in objects2:
		newid3, new_hashid3 = getnewid(EvalDetB)
		obj3 = EvalDetB(id=newid3, eval=obj, parameter=j,\
			user=request.user, hashed=new_hashid3)
		obj3.save()
	messages.success(request, 'Susesu Kria Self Evaluation Sheet')
	if group == 'hr':
		return redirect('eval-detail-eval', hashid=obj.hashed, hashid2=plan.hashed)
	else:
		return redirect('staff-eval-detail', hashid=obj.hashed, hashid2=plan.hashed)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerfomEvalDetail(request, hashid, hashid2):
    objects = get_object_or_404(Eval,hashed=hashid)
    user = c_staff(request.user)
    plan = get_object_or_404(EvalPlanning,hashed=hashid2)
    check_emp = True if user == objects.employee else False
    individual = EvalDetA.objects.filter(eval=objects)
    behavior = EvalDetB.objects.filter(eval=objects)
    finalscore = EvalFinalScore.objects.filter(eval=objects).last()
    context = {
        'title': 'Detail Evaluation', 'legend': 'Evaluation Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior, \
		'plan':plan, 'finalscore':finalscore
    }
    return render(request,'perform2/eval_detail.html', context)



##EVALUATOR

@login_required
def PerfomEvalEvaluatorAdd(request, hashid, hashid2):
    emp, unit = c_unit(request.user)
    eval = get_object_or_404(Eval,hashed=hashid)
    contract = Contract.objects.filter(employee=emp, is_active=True).last()
    empdiv = CurEmpDivision.objects.filter(employee=emp).last()
    plan = get_object_or_404(EvalPlanning,hashed=hashid2)
    eval.employeeeval = emp
    eval.positioneval = contract.position
    eval.uniteval = empdiv.unit
    eval.save()
    messages.success(request, f'Chave Sucessu')
    return redirect('eval-evaluator-detail', hashid=eval.hashed,  hashid2=plan.hashed )

@login_required
def PerfomEvalEvaluatorDetail(request, hashid, hashid2):
    objects = get_object_or_404(Eval,hashed=hashid)
    user = c_staff(request.user)
    plan = get_object_or_404(EvalPlanning,hashed=hashid2)
    check_emp = True if user == objects.employee else False
    individual = EvalDetA.objects.filter(eval=objects)
    behavior = EvalDetB.objects.filter(eval=objects)
    finalscore = EvalFinalScore.objects.filter(eval=objects).last()
    context = {
        'title': 'Detail Evaluation', 'legend': 'Evaluation Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior, \
		'plan':plan, 'finalscore':finalscore
    }
    return render(request,'perform2/evaluator_eval_detail.html', context)


@login_required
def cPerformLock(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = get_object_or_404(Eval, hashed=hashid)
	plan = get_object_or_404(EvalPlanning, hashed=hashid2)
	objects.is_finish = True
	objects.save()
	messages.success(request, f'Susesu Chave')
	return redirect('eval-evaluator-detail', hashid=hashid, hashid2=plan.hashed)