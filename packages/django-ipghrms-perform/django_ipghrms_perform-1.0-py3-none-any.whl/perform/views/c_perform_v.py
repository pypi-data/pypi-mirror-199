from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from perform.utils import f_finalscore
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from contract.models import Category, Contract, EmpPosition
from perform.models import *
from settings_app.user_utils import c_unit

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformDash(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	if group == 'unit':
		cats = Category.objects.filter().exclude(Q(pk=1)|Q(pk=2)).order_by('id')
	else:
		cats = Category.objects.filter().all().order_by('id')

	objects = []
	for i in cats:
		a = Contract.objects.filter((Q(employee__curempdivision__department__unit=unit)|Q(employee__curempdivision__unit=unit)),\
			category=i, is_active=True).exclude((Q(employee__curempdivision__department__id=3)|Q(employee__curempposition__position__id=3))).all().count()
		b = Eval.objects.filter((Q(employee__curempdivision__department__unit=unit)|Q(employee__curempdivision__unit=unit)),\
			employee__contract__category=i).exclude((Q(employee__curempdivision__department__id=3)|Q(employee__curempposition__position__id=3)))\
			.all().count()
		c = a - b
		objects.append([i,a,b,c])
	context = {
		'group': group, 'objects': objects,
		'title': 'Painel Avaliasaun', 'legend': 'Painel Avaliasaun'
	}
	return render(request, 'perform2/c_eval_dash.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformList(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	year = EvalYear.objects.filter(is_active=True).first()
	objects = Eval.objects.filter((Q(department__unit=unit)|Q(unit=unit)),\
		year=year).exclude((Q(employee=c_emp)|Q(department__id=3)|Q(category_id=6))).all().order_by('-start_date','id')
	years = Eval.objects.filter().distinct().values('year__year').all()
	context = {
		'group': group, 'unit': unit, 'year': year, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun Tinan {year.year}', 'legend': f'Lista Avaliasaun Tinan {year.year}'
	}
	return render(request, 'perform2/c_eval_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformDetail(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp, unit, dep = "","",""
	c_emp, unit = c_unit(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	zuri = Evaluator.objects.filter(eval=eval).first()
	evaldate = EvalDate.objects.filter(eval=eval).first()
	finalscore = EvalFinalScore.objects.filter(eval=eval).first()
	obj_as = EvalDetA.objects.filter(eval=eval).all()
	obj_bs = EvalDetB.objects.filter(eval=eval).all()
	sum_a = EvalDetA.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	sum_b = EvalDetB.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	context = {
		'group': group, 'c_emp': c_emp, 'unit': unit, 'dep': dep, 'eval': eval, 'zuri': zuri,
		'evaldate': evaldate, 'finalscore': finalscore,
		'obj_as': obj_as, 'obj_bs': obj_bs, 'sum_a': sum_a, 'sum_b': sum_b,
		'title': f'Detalha Avaliasaun', 'legend': f'Detalha Avaliasaun'
	}
	return render(request, 'perform2/c_eval_detail.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformYearList(request, year):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	year = EvalYear.objects.filter(year=year).first()
	objects = Eval.objects.filter((Q(department__unit=unit)|Q(unit=unit)),\
		year=year).exclude((Q(employee=c_emp)|Q(department__id=3)|Q(category_id=6))).all().order_by('id')
	years = Eval.objects.filter().distinct().values('year__year').all()
	context = {
		'group': group, 'unit': unit, 'year': year, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun Tinan {year.year}', 'legend': f'Lista Avaliasaun Tinan {year.year}'
	}
	return render(request, 'perform2/c_eval_year_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def cPerformCatList(request, pk):
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
	return render(request, 'perform2/c_eval_cat_list.html', context)

###