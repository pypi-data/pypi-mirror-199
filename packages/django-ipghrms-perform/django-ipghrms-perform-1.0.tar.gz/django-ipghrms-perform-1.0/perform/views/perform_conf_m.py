import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from employee.models import CurEmpDivision, Employee
from contract.models import Category, Contract, EmpPosition
from perform.models import ParameterA, ParameterB, Eval, EvalDetA, EvalDetB, EvalYear, \
EvalPlanning, EvalPlanningA, EvalPlanningB, EvalType
from perform.forms import *
from settings_app.utils import getnewid



@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerfomConfAddPlan(request, hashid, year):
    employee = get_object_or_404(Employee, hashed=hashid)
    pyear = get_object_or_404(EvalYear, year=year)
    ptype = get_object_or_404(EvalType, pk=1)
    contract = Contract.objects.filter(employee=employee, is_active=True).last()
    empdiv = CurEmpDivision.objects.filter(employee=employee).last()
    newid, new_hashid = getnewid(EvalPlanning)
    obj = EvalPlanning(
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
    messages.success(request, 'Susesu Kria Planning and Monitoring Sheet')
    return redirect('eval-conf-dash')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PerfomConfAddPlanAll(request, year):
    pyear = get_object_or_404(EvalYear, year=year)
    ptype = get_object_or_404(EvalType, pk=1)
    employees = Employee.objects.filter(status_id=1).exclude(curempdivision__de__pk=1)
    for emp in employees:
        check_emp_plan = EvalPlanning.objects.filter(employee=emp, year=pyear).last()
        if not check_emp_plan:
            contract = Contract.objects.filter(employee=emp, is_active=True).last()
            empdiv = CurEmpDivision.objects.filter(employee=emp).last()
            newid, new_hashid = getnewid(EvalPlanning)
            obj = EvalPlanning(
                id = newid,
                hashed= new_hashid,
                year = pyear,
                type = ptype,
                employee = emp,
                category = contract.category,
                position = contract.position,
                department = empdiv.department,
                unit = empdiv.unit
            )
            obj.save()
    messages.success(request, 'Susesu Kria Planning and Monitoring Sheet')
    return redirect('eval-conf-dash')

