from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from perform.utils import f_finalscore
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from contract.models import Category, Contract
from perform.models import *
from settings_app.user_utils import c_unit, c_staff
from custom.models import Unit

@login_required
@allowed_users(allowed_roles=['hr','de','deputy', 'unit'])
def allPerformDash(request):
	group = request.user.groups.all()[0].name
	unit = Unit.objects.all()
	emp, unit_g = c_unit(request.user)
	employee = []
	if group == 'de':
		emp = Employee.objects.filter(
			(Q(curempdivision__department__unit=unit_g)|Q(curempdivision__unit=unit_g))| \
			(Q(empposition__is_manager=True, empposition__is_active=True, empposition__unit__isnull=False))|\
			(Q(empposition__is_active=True, empposition__position__id=2))
			).select_related('curempdivision').exclude((Q(id=emp.id))).distinct()
	else:
		emp = Employee.objects.filter(
				(Q(curempdivision__department__unit=unit_g)|Q(curempdivision__unit=unit_g))
			).select_related('curempdivision').exclude((Q(id=emp.id))).distinct()

	for i in emp:
		planning = EvalPlanning.objects.filter(employee=i, year__is_active=True).last()
		preass = EvalPreAssessment.objects.filter(employee=i, year__is_active=True).last()
		selfass = EvalSelf.objects.filter(employee=i, year__is_active=True).last()
		eval = Eval.objects.filter(employee=i, year__is_active=True).last()
		employee.append([i, planning, preass, selfass, eval])
	objects = []
	for i in unit:
		objects.append(i)
	context = {
		'group': group, 'objects': objects, 'employee':employee,
		'title': 'Painel Avaliasaun', 'legend': 'Painel Avaliasaun'
	}
	return render(request, 'perform2/all_eval_dash.html', context)

@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def allPerformList(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	year = EvalYear.objects.filter(is_active=True).first()
	objects = Eval.objects.filter(year=year).exclude().all().order_by('-start_date','id')
	years = Eval.objects.filter().distinct().values('year__year').all()
	context = {
		'group': group, 'unit': unit, 'year': year, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun Tinan {year.year}', 'legend': f'Lista Avaliasaun Tinan {year.year}'
	}
	return render(request, 'perform2/all_eval_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def allPerformDetail(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit, dep = "","",""
	c_emp, unit = c_unit(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	zuri = Evaluator.objects.filter(eval=eval).first()
	evaldate = EvalDate.objects.filter(eval=eval).first()
	obj_as = EvalDetA.objects.filter(eval=eval).all()
	obj_bs = EvalDetB.objects.filter(eval=eval).all()
	sum_a = EvalDetA.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	sum_b = EvalDetB.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	context = {
		'group': group, 'c_emp': c_emp, 'unit': unit, 'dep': dep, 'eval': eval, 'zuri': zuri,
		'evaldate': evaldate,
		'obj_as': obj_as, 'obj_bs': obj_bs, 'sum_a': sum_a, 'sum_b': sum_b,
		'title': f'Detalha Avaliasaun', 'legend': f'Detalha Avaliasaun'
	}
	return render(request, 'perform2/all_eval_detail.html', context)

@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def allPerformYearList(request, year):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	year = EvalYear.objects.filter(year=year).first()
	objects = Eval.objects.filter((Q(department__unit=unit)|Q(unit=unit)),\
		year=year).exclude((Q(employee=c_emp)|Q(department__id=3)|Q(category_id=6))).all().order_by('-start_date','id')
	years = Eval.objects.filter().distinct().values('year__year').all()
	context = {
		'group': group, 'unit': unit, 'year': year, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun Tinan {year.year}', 'legend': f'Lista Avaliasaun Tinan {year.year}'
	}
	return render(request, 'perform2/all_eval_year_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def allPerformCatList(request, pk):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	cat = get_object_or_404(Category, pk=pk)
	year = EvalYear.objects.filter(is_active=True).first()
	objects = Eval.objects.filter((Q(department__unit=unit)|Q(unit=unit)),\
		category=cat,year=year).exclude((Q(employee=c_emp)|Q(department__id=3)|Q(category_id=6))).all().order_by('-start_date','id')
	context = {
		'group': group, 'unit': unit, 'year': year, 'cat': cat, 'objects': objects,
		'title': f'Lista Avaliasaun Tinan {year.year}', 'legend': f'Lista Avaliasaun Tinan {year.year}'
	}
	return render(request, 'perform2/all_eval_cat_list.html', context)



@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def allPerformCatEvalList(request, pk):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	cat = get_object_or_404(Category, pk=pk)
	year = EvalYear.objects.filter(is_active=True).first()
	objects2 = Eval.objects.filter((Q(department__unit=unit)|Q(unit=unit)),\
		category=cat,year=year).exclude((Q(employee=c_emp)|Q(department__id=3)|Q(category_id=6))).all().order_by('-start_date','id')
	objects = Eval.objects.filter(employee__contract__category=cat).exclude().all()
	context = {
		'group': group, 'unit': unit, 'year': year, 'cat': cat, 'objects': objects,
		'title': f'Lista Funsionario nebe halo Avaliasaun', 'legend': f'Lista Funsionario nebe halo Avaliasaun'
	}
	return render(request, 'perform2/all_eval_cat_list.html', context)


@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def allPerformCatNotList(request, pk):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	cat = get_object_or_404(Category, pk=pk)
	year = EvalYear.objects.filter(is_active=True).first()
	objects2 = Eval.objects.filter((Q(department__unit=unit)|Q(unit=unit)),\
		category=cat,year=year).exclude((Q(employee=c_emp)|Q(department__id=3)|Q(category_id=6))).all().order_by('-start_date','id')
	objects = Contract.objects.filter(category=cat, is_active=True).all()
	context = {
		'group': group, 'unit': unit, 'year': year, 'cat': cat, 'objects': objects,
		'title': f'Lista Funsionario nebe seidauk halo Avaliasaun', 'legend': f'Lista Funsionario nebe seidauk halo Avaliasaun'
	}
	return render(request, 'perform2/all_eval_cat_list.html', context)



###