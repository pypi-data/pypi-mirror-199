from django.shortcuts import redirect, render, get_object_or_404
from trip.models import Trip, TripType, TripEmp
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settings_app.utils import getnewid
from settings_app.decorators import allowed_users
from employee.models import Employee
from django.contrib.auth.models import User

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def vTripDash(request):
    context = {
        'title': 'Painel Trip', 'legend': 'Painel Trip',
    }
    return render(request, 'trip/dash.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de'])
def vTripSummary(request):
    employees = Employee.objects.filter(status_id=1)
    objects = []
    for emp in employees:
        localT = TripEmp.objects.filter(employee=emp, trip__ttype__pk=1)
        localTCount = localT.count()
        overSeasT = TripEmp.objects.filter(employee=emp, trip__ttype__pk=2)
        overSeasTCount = overSeasT.count()
        totallT = localTCount + overSeasTCount
        objects.append([emp, localTCount, overSeasTCount, totallT])
    totallTrip = TripEmp.objects.filter(trip__ttype__pk=1).count()
    totaloTrip = TripEmp.objects.filter(trip__ttype__pk=2).count()
    totalgen = totallTrip + totaloTrip

    context = {
        'title': 'Summary Trip', 'legend': 'Summary all staff out of Office for Official Trip', 'objects': objects, \
        'totallTrip':totallTrip, 'totaloTrip':totaloTrip, 'totalgen':totalgen
    }
    return render(request, 'trip/sumary.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de'])
def vTripList(request):
    objects = Trip.objects.select_related('country','ttype', 'municipality')
    context = {
        'title': 'Lista Trip', 'legend': 'Lista Trip',
        'objects': objects, 
    }
    return render(request, 'trip/list.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr', 'de'])
def mTripDetail(request, hashid):
    group = request.user.groups.all()[0].name
    objects = get_object_or_404(Trip.objects.select_related('ttype', 'country', 'municipality' ), hashed=hashid)
    tripemp = TripEmp.objects.filter(trip=objects).select_related('employee', 'employee__curempposition', 'employee__curempdivision')
    context = {
        'objects': objects, 'tripemp':tripemp,
        'title': 'Detalha Trip', 'legend': 'Detalha Trip','group': group
    }
    return render(request, 'trip/detail.html', context)
