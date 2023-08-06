from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from perform.utils import f_finalscore
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from contract.models import Category, Contract, EmpPosition
from perform.models import *
from settings_app.user_utils import c_staff, c_dep, c_unit

@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformList(request):
	group = request.user.groups.all()[0].name
	if group == "staff": c_emp = c_staff(request.user)
	elif group == "dep": c_emp, _ = c_dep(request.user)
	elif group == "unit": c_emp, _ = c_unit(request.user)
	elif group == "hr": c_emp, _ = c_unit(request.user)
	objects = EvalSelf.objects.filter(employee=c_emp).all().order_by('-start_date')
	context = {
		'group': group, 'c_emp': c_emp, 'objects': objects, 'page': 'list',
		'title': f'Lista Avaliasaun', 'legend': f'Lista Avaliasaun'
	}
	return render(request, 'perform2_self/eval_list.html', context)

@login_required
@allowed_users(allowed_roles=['staff','dep','unit','hr'])
def selfPerformDetail(request, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(EvalSelf, hashed=hashid)
	obj_as = EvalSelfDetA.objects.filter(eval=eval).all()
	obj_bs = EvalSelfDetB.objects.filter(eval=eval).all()
	context = {
		'group': group, 'eval': eval, 'obj_as': obj_as, 'obj_bs': obj_bs,
		'title': f'Detalha Avaliasaun', 'legend': f'Detalha Avaliasaun'
	}
	return render(request, 'perform2_self/eval_detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def selfPerformAllList(request):
	group = request.user.groups.all()[0].name
	objects = EvalSelf.objects.filter().all().order_by('-start_date')
	years = EvalSelf.objects.filter().distinct().values('year__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun Pessoal', 'legend': f'Lista Avaliasaun Pessoal'
	}
	return render(request, 'perform2_self/all_eval_list.html', context)

@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def selfPerformYearList(request, year):
	group = request.user.groups.all()[0].name
	objects, years = [],[]
	objects = EvalSelf.objects.filter(year__year=year).all().order_by('-start_date')
	years = EvalSelf.objects.filter().distinct().values('year__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun Pessoal', 'legend': f'Lista Avaliasaun Pessoal'
	}
	return render(request, 'perform2_self/all_eval_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def selfPerformUnitList(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = EvalSelf.objects.filter((Q(employee__curempdivision__department__unit=unit)\
		|Q(employee__curempdivision__unit=unit))).all().order_by('-start_date')
	years = EvalSelf.objects.filter((Q(employee__curempdivision__department__unit=unit)\
		|Q(employee__curempdivision__unit=unit))).distinct().values('year__year').all()
	context = {
		'group': group, 'unit': unit, 'objects': objects, 'years': years, 'page': 'list',
		'title': f'Lista Avaliasaun Pessoal', 'legend': f'Lista Avaliasaun Pessoal'
	}
	return render(request, 'perform2_self/eval_unit_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr'])
def selfPerformUnitYearList(request, year):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects, years = [],[]
	objects = EvalSelf.objects.filter((Q(employee__curempdivision__department__unit=unit)\
		|Q(employee__curempdivision__unit=unit)), year__year=year).all().order_by('-start_date')
	years = EvalSelf.objects.filter((Q(employee__curempdivision__department__unit=unit)\
		|Q(employee__curempdivision__unit=unit))).distinct().values('year__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun Pessoal', 'legend': f'Lista Avaliasaun Pessoal'
	}
	return render(request, 'perform2_self/eval_unit_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr','de','deputy'])
def selfPerformAllDetail(request, hashid):
	group = request.user.groups.all()[0].name
	eval = get_object_or_404(EvalSelf, hashed=hashid)
	obj_as = EvalSelfDetA.objects.filter(eval=eval).all()
	obj_bs = EvalSelfDetB.objects.filter(eval=eval).all()
	context = {
		'group': group, 'eval': eval, 'obj_as': obj_as, 'obj_bs': obj_bs,
		'title': f'Detalha Avaliasaun', 'legend': f'Detalha Avaliasaun'
	}
	return render(request, 'perform2_self/all_eval_detail.html', context)


#### NEW

@login_required
def PerfomConfSelfDetail(request, hashid):
    objects = get_object_or_404(EvalSelf,hashed=hashid)
    user = c_staff(request.user)
    check_emp = True if user == objects.employee else False
    individual = EvalSelfDetA.objects.filter(eval=objects)
    behavior = EvalSelfDetB.objects.filter(eval=objects)
    context = {
        'title': 'Detail Self Evaluation', 'legend': 'Self Evaluation Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior
    }
    return render(request,'perform2/self_detail.html', context)


@login_required
def PerfomEvaluatorSelfDetail(request, hashid):
    objects = get_object_or_404(EvalSelf,hashed=hashid)
    user = c_staff(request.user)
    check_emp = True if user == objects.employee else False
    individual = EvalSelfDetA.objects.filter(eval=objects)
    behavior = EvalSelfDetB.objects.filter(eval=objects)
    context = {
        'title': 'Detail Self Evaluation', 'legend': 'Self Evaluation Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior
    }
    return render(request,'perform2/evaluator_self_detail.html', context)