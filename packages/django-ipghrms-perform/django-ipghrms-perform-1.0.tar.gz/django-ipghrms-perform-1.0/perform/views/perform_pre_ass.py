import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from employee.models import CurEmpDivision, Employee
from contract.models import Category, Contract, EmpPosition
from perform.models import ParameterA, ParameterB, Eval, EvalDetA, EvalDetB, EvalYear, \
EvalPlanning, EvalPlanningB, EvalType, EvalPreAssessment, EvalPreAssessmentA, EvalPreAssessmentB
from perform.forms import *
from settings_app.utils import getnewid
from settings_app.user_utils import c_staff, c_unit
from log.utils import log_action


@login_required
def PerfomConfAddPreAss(request, hashid, year):
    group = request.user.groups.all()[0].name
    employee = get_object_or_404(Employee, hashed=hashid)
    pyear = get_object_or_404(EvalYear, year=year)
    ptype = get_object_or_404(EvalType, pk=2)
    contract = Contract.objects.filter(employee=employee, is_active=True).last()
    empdiv = CurEmpDivision.objects.filter(employee=employee).last()
    newid, new_hashid = getnewid(EvalPreAssessment)
    obj = EvalPreAssessment(
        id = newid,
        hashed= new_hashid,
        year = pyear,
        type = ptype,
        is_lock = True,
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
        newid, new_hashid = getnewid(EvalPreAssessmentA)
        obj2 = EvalPreAssessmentA(id=newid, eval=obj, plan_objective=i,\
            user=request.user, hashed=new_hashid)
        obj2.save()
    for j in objects2:
        newid2, new_hashid2 = getnewid(EvalPreAssessmentB)
        obj3 = EvalPreAssessmentB(id=newid2, eval=obj, parameter=j,\
            user=request.user, hashed=new_hashid2)
        obj3.save()
    messages.success(request, 'Susesu Kria Pre-Assessment Sheet')
    if group == 'hr':
        return redirect('eval-conf-dash')
    else:
        return redirect('staff-perform-list')
# @login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def PerfomConfAddPreAssAll(request, year):
#     pyear = get_object_or_404(EvalYear, year=year)
#     ptype = get_object_or_404(EvalType, pk=1)
#     employees = Employee.objects.filter(status_id=1).exclude(curempdivision__de__pk=1)
#     for emp in employees:
#         check_emp_plan = EvalPlanning.objects.filter(employee=emp, year=pyear).last()
#         if not check_emp_plan:
#             contract = Contract.objects.filter(employee=emp, is_active=True).last()
#             empdiv = CurEmpDivision.objects.filter(employee=emp).last()
#             newid, new_hashid = getnewid(EvalPlanning)
#             obj = EvalPlanning(
#                 id = newid,
#                 hashed= new_hashid,
#                 year = pyear,
#                 type = ptype,
#                 employee = emp,
#                 category = contract.category,
#                 position = contract.position,
#                 department = empdiv.department,
#                 unit = empdiv.unit
#             )
#             obj.save()
#     messages.success(request, 'Susesu Kria Planning and Monitoring Sheet')
#     return redirect('eval-conf-dash')



# @login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def PerfomPreAssAddObjective(request, hashid):
#     objects = get_object_or_404(EvalPlanning,hashed=hashid)
#     plan = EvalPlanningA.objects.filter(eval=objects)
#     group = request.user.groups.all()[0].name
#     if request.method == 'POST':
#             form = PlanningObjectiveForm(request.POST, instance=objects)
#             if form.is_valid():
#                  form.save()
#             messages.success(request, f'Aumeta Sucessu')
#             return redirect('eval-conf-plan-detail', hashid)
#     else: form = PlanningObjectiveForm(instance=objects)
#     context = {
#         'group': group, 'form': form, 'page': 'unit',
#         'title': 'Aumenta Objectives', 'legend': 'Aumenta Objectives'
#     }
#     return render(request, 'perform2/form.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerfomConfPreAssDetail(request, hashid):
    objects = get_object_or_404(EvalPreAssessment,hashed=hashid)
    user = c_staff(request.user)
    check_emp = True if user == objects.employee else False
    individual = EvalPreAssessmentA.objects.filter(eval=objects)
    behavior = EvalPreAssessmentB.objects.filter(eval=objects)
    context = {
        'title': 'Detail Pre-Assessment', 'legend': 'Pre-Assessment Sheet', \
        'objects': objects, 'check_emp':check_emp, 'individual':individual, 'behavior':behavior
    }
    return render(request,'perform2/pre_ass_detail.html', context)

@login_required
@allowed_users(allowed_roles=['unit','hr', 'staff', 'dep', 'unit'])
def PerfomConfPreAssAddA(request, hashid):
    group = request.user.groups.all()[0].name
    eval = get_object_or_404(EvalPreAssessment, hashed=hashid)
    objects = EvalPlanningA.objects.filter(eval__employee=eval.employee, eval__year=eval.year).all()
    for i in objects:
        newid, new_hashid = getnewid(EvalPreAssessmentA)
        obj = EvalPreAssessmentA(id=newid, eval=eval, plan_objective=i,\
            user=request.user, hashed=new_hashid)
        obj.save()
        messages.success(request, f'Importa sucessu.')
    if group == 'hr':
        return redirect('eval-conf-pre-ass-detail', hashid=hashid)
    else:
        return redirect('staff-perform-preass-detail', hashid=hashid)
         

@login_required
@allowed_users(allowed_roles=['unit','hr', 'staff', 'dep', 'unit'])
def PerfomConfPreAssAddB(request, hashid):
    group = request.user.groups.all()[0].name
    eval = get_object_or_404(EvalPreAssessment, hashed=hashid)
    objects = EvalPlanningB.objects.filter(eval__employee=eval.employee, eval__year=eval.year).all()
    for i in objects:
        newid, new_hashid = getnewid(EvalPreAssessmentB)
        obj = EvalPreAssessmentB(id=newid, eval=eval, parameter=i,\
            user=request.user, hashed=new_hashid)
        obj.save()
        messages.success(request, f'Importa sucessu.')
    if group == 'hr':
        return redirect('eval-conf-pre-ass-detail', hashid=hashid)
    else:
        return redirect('staff-perform-preass-detail', hashid=hashid)


# @login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def PerfomConfPreAssAddA(request, hashid):
#     objects = get_object_or_404(EvalPreAssessmentA,hashed=hashid)
#     group = request.user.groups.all()[0].name
#     if request.method == 'POST':
#             newid, new_hashid = getnewid(EvalPreAssessmentA)
#             form = PlanningAForm(request.POST)

#             if form.is_valid():
#                  instance = form.save(commit=False)
#                  instance.id = newid
#                  instance.hashed = new_hashid
#                  instance.eval = objects
#                  instance.enter_date = datetime.date.today()
#                  instance.user = request.user
#                  instance.save()
#             messages.success(request, f'Aumeta Sucessu')
#             return redirect('eval-conf-plan-detail', hashid)
#     else: form = PlanningAForm()
#     context = {
#         'group': group, 'form': form, 'page': 'unit',
#         'title': 'Aumenta Individual Activities', 'legend': 'Aumenta Individual Activities'
#     }
#     return render(request, 'perform2/form.html', context)

# @login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def PerfomPlanUdpateA(request, hashid):
#     objects = get_object_or_404(EvalPlanningA,hashed=hashid)
#     group = request.user.groups.all()[0].name
#     if request.method == 'POST':
#             form = PlanningAForm(request.POST, instance=objects)

#             if form.is_valid():
#                  instance = form.save(commit=False)
#                  instance.eval_date = datetime.date.today()
#                  instance.user = request.user
#                  instance.save()
#             messages.success(request, f'Altera Sucessu')
#             return redirect('eval-conf-plan-detail', objects.eval.hashed)
#     else: form = PlanningAForm(instance=objects)
#     context = {
#         'group': group, 'form': form, 'page': 'unit',
#         'title': 'Altera Individual Activities', 'legend': 'Altera Individual Activities'
#     }
#     return render(request, 'perform2/form.html', context)

# @login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def PerfomPlanDeleteA(request, hashid, hashid2):
#     objects = get_object_or_404(EvalPlanningA,hashed=hashid)
#     plan = get_object_or_404(EvalPlanning,hashed=hashid2)
#     objects.delete()
#     messages.success(request, f'Delete Sucessu')
#     return redirect('eval-conf-plan-detail', plan.hashed)


# @login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def PerfomPlanDeleteB(request, hashid, hashid2):
#     objects = get_object_or_404(EvalPlanningB,hashed=hashid)
#     plan = get_object_or_404(EvalPlanning,hashed=hashid2)
#     objects.delete()
#     messages.success(request, f'Delete Sucessu')
#     return redirect('eval-conf-plan-detail', plan.hashed)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerfomPreAssLock(request, hashid):
    plan = get_object_or_404(EvalPreAssessment,hashed=hashid)
    plan.is_lock = True
    plan.save()
    messages.success(request, f'Chave Sucessu')
    return redirect('eval-conf-pre-ass-detail', plan.hashed)




# # EVALUATOR PRE ASS
@login_required
def PerfomEvaluatorAdd(request, hashid):
    emp, unit = c_unit(request.user)
    preass = get_object_or_404(EvalPreAssessment,hashed=hashid)
    contract = Contract.objects.filter(employee=emp, is_active=True).last()
    empdiv = CurEmpDivision.objects.filter(employee=emp).last()
    preass.employeeeval = emp
    preass.positioneval = contract.position
    preass.uniteval = empdiv.unit
    preass.save()
    messages.success(request, f'Chave Sucessu')
    return redirect('eval-pre-ass-evaluator-detail', preass.hashed)

@login_required
def PerfomEvaluatorDetail(request, hashid):
    group = request.user.groups.all()[0].name
    plan = get_object_or_404(EvalPreAssessment,hashed=hashid)
    individual = EvalPreAssessmentA.objects.filter(eval=plan)
    behavior = EvalPreAssessmentB.objects.filter(eval=plan)
    check_ind = EvalPreAssessmentA.objects.filter(eval=plan, scored__isnull=False).exists()
    check_beh = EvalPreAssessmentB.objects.filter(eval=plan, scored__isnull=False).exists()
    context = {
         'title': 'Detail Detail Pre-Assessment', 'legend':'Detail Detail Pre-Assessment', 
         'group': group,  'objects': plan, 'page':'pr-detail', 'individual':individual, 'behavior':behavior,
         'check_ind':check_ind, 'check_beh':check_beh
    }
    return render(request,'perform2/evaluator_preass_detail.html', context)

@login_required
def PerfomEvaluatorLock(request, hashid):
    group = request.user.groups.all()[0].name
    plan = get_object_or_404(EvalPreAssessment,hashed=hashid)
    plan.is_finish = True
    plan.save()
    messages.success(request, 'Susesu Chave')
    return redirect('eval-pre-ass-evaluator-detail', hashid)


# ### INDIVIDUAL 
@login_required
def PerfomEvaluatorIndAdd(request, hashid):
    objects = get_object_or_404(EvalPreAssessmentA,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PreAssIndividuoForm(request.POST, instance=objects)
            if form.is_valid():
                 instance = form.save(commit=False)
                 instance.eval_date = datetime.date.today()
                 instance.usereval = request.user
                 instance.save()
                 log_action(request, model='evaluator_pre_ass_ind_objective', action="Update",field_id=objects.pk)
            messages.success(request, f'Aumenta Sucessu')
            return redirect('eval-pre-ass-evaluator-detail', objects.eval.hashed)
    else: form = PreAssIndividuoForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'ind-add-ps', 'objects':objects,
        'title': 'Aumenta Indikador Individual Objectives', 'legend': 'Aumenta Indikador Individual Objectives'
    }
    return render(request, 'perform2/form.html', context)

@login_required
def PerfomEvaluatorBehAdd(request, hashid):
    objects = get_object_or_404(EvalPreAssessmentB,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PreAssBehaviorForm(request.POST, instance=objects)
            if form.is_valid():
                 instance = form.save(commit=False)
                 instance.eval_date = datetime.date.today()
                 instance.usereval = request.user
                 instance.save()
                 log_action(request, model='evaluator_pre_ass_prof_behavior', action="Update",field_id=objects.pk)
            messages.success(request, f'Aumenta Sucessu')
            return redirect('eval-pre-ass-evaluator-detail', objects.eval.hashed)
    else: form = PreAssBehaviorForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'bhv-add-ps', 'objects':objects,
        'title': 'Aumenta indikador Professional Behavior', 'legend': 'Aumenta indikador Professional Behavior'
    }
    return render(request, 'perform2/form.html', context)



@login_required
def PerfomPreAssEvalAddObjDate(request, hashid):
    objects = get_object_or_404(EvalPreAssessment,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PreAssEvaluatorDateForm(request.POST, instance=objects)

            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            return redirect('eval-pre-ass-evaluator-detail', objects.hashed)
    else: form = PreAssEvaluatorDateForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit',
        'title': 'Aumenta Data', 'legend': 'Aumenta Data'
    }
    return render(request, 'perform2/form.html', context)

@login_required
def PerfomPreAssEvalAddBehDate(request, hashid):
    objects = get_object_or_404(EvalPreAssessment,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PreAssEvaluatorDate2Form(request.POST, instance=objects)

            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            return redirect('eval-pre-ass-evaluator-detail', objects.hashed)
    else: form = PreAssEvaluatorDate2Form(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit',
        'title': 'Aumenta Data', 'legend': 'Aumenta Data'
    }
    return render(request, 'perform2/form.html', context)

@login_required
def PerfomPreAssEvalAddComment(request, hashid):
    objects = get_object_or_404(EvalPreAssessment,hashed=hashid)
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
            form = PreAssEvaluatorCommentForm(request.POST, instance=objects)

            if form.is_valid():
                 form.save()
            messages.success(request, f'Aumeta Sucessu')
            return redirect('eval-pre-ass-evaluator-detail', objects.hashed)
    else: form = PreAssEvaluatorCommentForm(instance=objects)
    context = {
        'group': group, 'form': form, 'page': 'unit',
        'title': 'Aumenta Komentario', 'legend': 'Aumenta Komentario'
    }
    return render(request, 'perform2/form.html', context)