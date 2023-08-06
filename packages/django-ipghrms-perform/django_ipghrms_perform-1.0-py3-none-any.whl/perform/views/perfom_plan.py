import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from employee.models import CurEmpDivision, Employee
from contract.models import Category, Contract, EmpPosition
from perform.models import ParameterA, ParameterB, Eval, EvalDetA, EvalDetB, EvalYear, \
EvalPlanning, EvalPlanningB, EvalType
from perform.forms import *
from settings_app.utils import getnewid
from settings_app.user_utils import c_staff, c_unit
from log.utils import log_action

@login_required
@allowed_users(allowed_roles=['admin','hr', 'staff', 'dep', 'unit', 'deputy'])
def PerfomPlanAddObjective(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningObjectiveForm(request.POST, instance=objects)
            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            if group == 'hr':
                return redirect('eval-conf-plan-detail', hashid)
            else:
                return redirect('staff-perform-plan-detail', hashid)
    else: form = PlanningObjectiveForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit', 
        'objects': objects,
        'title': 'Aumenta Objectives', 'legend': 'Aumenta Objectives'
    }
    return render(request, 'perform2/form.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerfomPlanDetail(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    user = c_staff(request.user)
    check_emp = True if user == objects.employee else False
    individual = EvalPlanningA.objects.filter(eval=objects)
    behavior = EvalPlanningB.objects.filter(eval=objects)
    context = {
        'title': 'Detail Planning and Monitoring', 'legend': 'Planning and Monitoring Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior
    }
    return render(request,'perform2/plan_detail.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr', 'staff', 'dep', 'unit', 'deputy' ])
def PerfomPlanAddA(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            newid, new_hashid = getnewid(EvalPlanningA)
            form = PlanningAForm(request.POST)

            if form.is_valid():
                 instance = form.save(commit=False)
                 instance.id = newid
                 instance.hashed = new_hashid
                 instance.eval = objects
                 instance.enter_date = datetime.date.today()
                 instance.user = request.user
                 instance.save()
            messages.success(request, f'Aumeta Sucessu')
            if group == 'hr':
                return redirect('eval-conf-plan-detail', hashid)
            else:
                return redirect('staff-perform-plan-detail', hashid)
    else: form = PlanningAForm()
    context = {
        'group': group, 'form': form, 'page': 'unit','objects': objects,
        'title': 'Aumenta Individual Activities', 'legend': 'Aumenta Individual Activities'
    }
    return render(request, 'perform2/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'staff', 'dep', 'unit', 'deputy' ])
def PerfomPlanUdpateA(request, hashid):
    objects = get_object_or_404(EvalPlanningA,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningAForm(request.POST, instance=objects)

            if form.is_valid():
                 instance = form.save(commit=False)
                 instance.eval_date = datetime.date.today()
                 instance.user = request.user
                 instance.save()
                 log_action(request, model='individual_activity', action="Update",field_id=objects.pk)
            messages.success(request, f'Altera Sucessu')
            if group == 'hr':
                return redirect('eval-conf-plan-detail', hashid)
            else:
                return redirect('staff-perform-plan-detail', hashid=objects.eval.hashed)
    else: form = PlanningAForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit', 'objects': objects.eval,
        'title': 'Altera Individual Activities', 'legend': 'Altera Individual Activities'
    }
    return render(request, 'perform2/form.html', context)

@login_required
def PerfomPlanDeleteA(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    objects = get_object_or_404(EvalPlanningA,hashed=hashid)
    plan = get_object_or_404(EvalPlanning,hashed=hashid2)
    log_action(request, model='individual_activity', action="Delete",field_id=objects.pk)
    objects.delete()
    messages.success(request, f'Delete Sucessu')
    if group == 'hr':
        return redirect('eval-conf-plan-detail', hashid)
    else:
        return redirect('staff-perform-plan-detail', hashid=objects.eval.hashed)


@login_required
def PerfomPlanDeleteB(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    objects = get_object_or_404(EvalPlanningB,hashed=hashid)
    plan = get_object_or_404(EvalPlanning,hashed=hashid2)
    objects.delete()
    messages.success(request, f'Delete Sucessu')
    if group == 'hr':
        return redirect('eval-conf-plan-detail', plan.hashed)
    else:
        return redirect('staff-perform-plan-detail',plan.hashed)



@login_required
def PerfomPlanLock(request, hashid):
    group = request.user.groups.all()[0].name
    plan = get_object_or_404(EvalPlanning,hashed=hashid)
    if plan.ind_date != None and plan.obj_date != None:
        plan.is_lock = True
        plan.save()
        messages.success(request, f'Chave Sucessu')
        if group == 'hr':
            return redirect('eval-conf-plan-detail', plan.hashed)
        else:
            return redirect('staff-perform-plan-detail',plan.hashed)
    else:
        messages.error(request, f'Data Seidauk Prienche')
        if group == 'hr':
            return redirect('eval-conf-plan-detail', plan.hashed)
        else:
            return redirect('staff-perform-plan-detail',plan.hashed)
         




# EVALUATOR PLAN
@login_required
@allowed_users(allowed_roles=['de', 'unit'])
def PerfomPlanEvaluatorAdd(request, hashid):
    emp, unit = c_unit(request.user)
    plan = get_object_or_404(EvalPlanning,hashed=hashid)
    contract = Contract.objects.filter(employee=emp, is_active=True).last()
    empdiv = CurEmpDivision.objects.filter(employee=emp).last()
    plan.employeeeval = emp
    plan.positioneval = contract.position
    plan.uniteval = empdiv.unit
    plan.save()
    messages.success(request, f'Chave Sucessu')
    return redirect('eval-conf-plan-evaluator-detail', plan.hashed)

@login_required
@allowed_users(allowed_roles=['de', 'unit'])
def PerfomPlanEvaluatorDetail(request, hashid):
    group = request.user.groups.all()[0].name
    plan = get_object_or_404(EvalPlanning,hashed=hashid)
    individual = EvalPlanningA.objects.filter(eval=plan)
    behavior = EvalPlanningB.objects.filter(eval=plan)
    check_ind = EvalPlanningA.objects.filter(eval=plan).exists()
    check_beh = EvalPlanningB.objects.filter(eval=plan).exists()
    context = {
         'title': 'Detail Planning and Monitoring', 'legend':'Detail Planning and Monitoring', 
         'group': group,  'objects': plan, 'page':'pr-detail', 'individual':individual, 'behavior':behavior,
         'check_ind':check_ind, 'check_beh':check_beh
    }
    return render(request,'perform2/evaluator_plan_detail.html', context)

@login_required
@allowed_users(allowed_roles=['de', 'unit'])
def PerfomPlanEvaluatorLock(request, hashid):
    group = request.user.groups.all()[0].name
    plan = get_object_or_404(EvalPlanning,hashed=hashid)
    if plan.eval_date_obj != None and plan.eval_date_ind != None:
        plan.is_finish = True
        plan.save()
        messages.success(request, 'Susesu Chave')
        return redirect('eval-conf-plan-evaluator-detail', hashid)
    else:
        messages.error(request, 'Data seidauk prienche')
        return redirect('eval-conf-plan-evaluator-detail', hashid)
         


### INDIVIDUAL 
@login_required
def PerfomPlanIndividualAdd(request, hashid):
    objects = get_object_or_404(EvalPlanningA,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningIndividualForm(request.POST, instance=objects)
            if form.is_valid():
                 instance = form.save(commit=False)
                 instance.eval_date = datetime.date.today()
                 instance.usereval = request.user
                 instance.save()
                 log_action(request, model='evaluator_individual_activity', action="Update",field_id=objects.pk)
            messages.success(request, f'Aumenta Sucessu')
            return redirect('eval-conf-plan-evaluator-detail', objects.eval.hashed)
    else: form = PlanningIndividualForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'ind-add', 'objects':objects,
        'title': 'Aumenta Individual  Objectives', 'legend': 'Aumenta Individual  Objectives'
    }
    return render(request, 'perform2/form.html', context)

@login_required
def PerfomPlanBehaviorAdd(request, hashid):
    objects = get_object_or_404(EvalPlanningB,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningBehaviorForm(request.POST, instance=objects)
            if form.is_valid():
                 instance = form.save(commit=False)
                 instance.eval_date = datetime.date.today()
                 instance.usereval = request.user
                 instance.save()
                 log_action(request, model='evaluator_prof_behavior', action="Update",field_id=objects.pk)
            messages.success(request, f'Aumenta Sucessu')
            return redirect('eval-conf-plan-evaluator-detail', objects.eval.hashed)
    else: form = PlanningBehaviorForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'beh-add', 'objects':objects,
        'title': 'Aumenta Professional Behavior', 'legend': 'Aumenta Professional Behavior'
    }
    return render(request, 'perform2/form.html', context)


@login_required
def PerfomPlanAddObjDate(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningDate2Form(request.POST, instance=objects)

            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            if group == 'hr':
                return redirect('eval-conf-plan-detail', hashid)
            else:
                return redirect('staff-perform-plan-detail',hashid)
    else: form = PlanningDate2Form(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit', 'objects':objects,
        'title': 'Aumenta Data', 'legend': 'Aumenta Data'
    }
    return render(request, 'perform2/form.html', context)
@login_required
def PerfomPlanAddBehDate(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningDateForm(request.POST, instance=objects)

            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            if group == 'hr':
                return redirect('eval-conf-plan-detail', hashid)
            else:
                return redirect('staff-perform-plan-detail',hashid)
    else: form = PlanningDateForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit', 'objects':objects,
        'title': 'Aumenta Data', 'legend': 'Aumenta Data'
    }
    return render(request, 'perform2/form.html', context)


@login_required
def PerfomPlanEvalAddObjDate(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningEvaluatorDate2Form(request.POST, instance=objects)

            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            return redirect('eval-conf-plan-evaluator-detail', objects.hashed)
    else: form = PlanningEvaluatorDate2Form(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit',
        'title': 'Aumenta Data', 'legend': 'Aumenta Data'
    }
    return render(request, 'perform2/form.html', context)
@login_required
def PerfomPlanEvalAddBehDate(request, hashid):
    objects = get_object_or_404(EvalPlanning,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PlanningEvaluatorDateForm(request.POST, instance=objects)

            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            return redirect('eval-conf-plan-evaluator-detail', objects.hashed)
    else: form = PlanningEvaluatorDateForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit',
        'title': 'Aumenta Data', 'legend': 'Aumenta Data'
    }
    return render(request, 'perform2/form.html', context)