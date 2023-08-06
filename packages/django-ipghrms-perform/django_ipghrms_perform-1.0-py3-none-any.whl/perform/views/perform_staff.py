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
EvalSelfDetA, EvalSelfDetB, EvalFinalScore
from perform.forms import *
from settings_app.utils import getnewid
from settings_app.user_utils import c_unit, c_staff


@login_required
def StaffListPerfom(request):
    group = request.user.groups.all()[0].name
    cats = Category.objects.filter().all().order_by('id')
    employee = c_staff(request.user)
    eval_year = EvalYear.objects.filter(is_active=True).last()
    
    planning = EvalPlanning.objects.filter(employee=employee, year=eval_year).last()
    preass = EvalPreAssessment.objects.filter(employee=employee, year=eval_year).last()
    selfeval = EvalSelf.objects.filter(employee=employee, year=eval_year).last()
    eval = Eval.objects.filter(employee=employee, year=eval_year).last()
    check_plan = EvalPlanningA.objects.filter(eval=planning).exists()
    context = {
        'group': group, 
        'planning': planning,  'preass': preass, 'selfeval': selfeval, 'eval':eval,        
        'employee':employee, 'check_plan':check_plan, 'ayear':eval_year.year,
        'title': 'Lista Avaliasaun', 'legend': f'Lista Avaliasaun iha Tinan {eval_year.year}'
    }
    return render(request, 'perform_staff/list.html', context)

@login_required
def StaffPerfomPlanDetail(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    user = c_staff(request.user)
    check_emp = True if user == objects.employee else False
    individual = EvalPlanningA.objects.filter(eval=objects)
    behavior = EvalPlanningB.objects.filter(eval=objects)
    context = {
        'title': 'Detail Planning and Monitoring', 'legend': 'Planning and Monitoring Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior
    }
    return render(request,'perform_staff/plan_detail.html', context)

@login_required
def StaffPerfomPreAssDetail(request, hashid):
    objects = get_object_or_404(EvalPreAssessment,hashed=hashid)
    user = c_staff(request.user)
    check_emp = True if user == objects.employee else False
    individual = EvalPreAssessmentA.objects.filter(eval=objects)
    behavior = EvalPreAssessmentB.objects.filter(eval=objects)
    context = {
        'title': 'Detail Pre-Assessment', 'legend': 'Pre-Assessment Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior
    }
    return render(request,'perform_staff/preass_detail.html', context)

@login_required
def StaffPerformSelfDetail(request, hashid):
    objects = get_object_or_404(EvalSelf,hashed=hashid)
    user = c_staff(request.user)
    check_emp = True if user == objects.employee else False
    individual = EvalSelfDetA.objects.filter(eval=objects)
    behavior = EvalSelfDetB.objects.filter(eval=objects)
    context = {
        'title': 'Detail Self Evaluation', 'legend': 'Self Evaluation Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior
    }
    return render(request,'perform_staff/self_detail.html', context)

@login_required
def StaffEvalDetail(request, hashid, hashid2):
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
    return render(request,'perform_staff/eval_detail.html', context)
