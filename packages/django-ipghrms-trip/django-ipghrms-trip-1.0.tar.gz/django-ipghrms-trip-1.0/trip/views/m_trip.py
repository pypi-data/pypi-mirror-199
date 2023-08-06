from django.shortcuts import redirect, render, get_object_or_404
from trip.models import Trip, TripType, TripEmp
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settings_app.utils import getnewid
from settings_app.decorators import allowed_users
from trip.forms import TripForm,TripEmpForm
from employee.models import Employee
import datetime
import pandas as pd
from datetime import datetime as dt
from attendance.models import Attendance, AttendanceStatus, Year, Month


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def mTripAdd(request):
	if request.method == 'POST':
		newid, new_hashid = getnewid(Trip)
		form = TripForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Susesu Aumenta')
			return redirect('m-t-detail', instance.hashed)
	else: form = TripForm()
	context = {
		'form': form, 
		'title': 'Adisiona Trip', 'legend': 'Adisiona Trip'
	}
	return render(request, 'trip/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def mTripUpdate(request, hashid):
    objects = get_object_or_404(Trip, hashed=hashid)
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES, instance=objects)
        if form.is_valid():
            form.save()
            messages.success(request, f'Susesu Altera')
            return redirect('m-t-detail', hashid)
    else: form = TripForm(instance=objects)
    context = {
        'form': form, 
        'title': 'Altera Informasaun Trip', 'legend': 'Altera Informasaun Trip'
    }
    return render(request, 'trip/form.html', context)




@login_required
@allowed_users(allowed_roles=['admin','hr'])
def mTripLock(request, hashid):
    objects = get_object_or_404(Trip, hashed=hashid)
    objects.is_lock = True
    objects.save()
    messages.success(request, f'Susesu Chave')
    return redirect('m-t-detail', hashid)



@login_required
@allowed_users(allowed_roles=['admin','hr'])
def mTripEmpAdd(request, hashid):
    objects = get_object_or_404(Trip, hashed=hashid)
    if request.method == 'POST':
        newid, new_hashid = getnewid(TripEmp)
        form = TripEmpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.trip = objects
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Susesu Aumenta')
            return redirect('m-t-detail', hashid)
    else: form = TripEmpForm()
    context = {
        'form': form, 
        'title': 'Adisiona Funsionario', 'legend': 'Adisiona Funsionario'
    }
    return render(request, 'trip/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def mTripEmpUpdate(request, hashid):
    objects = get_object_or_404(TripEmp, hashed=hashid)
    if request.method == 'POST':
        form = TripEmpForm(request.POST, instance=objects)
        if form.is_valid():
            form.save()
            messages.success(request, f'Susesu Altera')
            return redirect('m-t-detail', hashid=objects.trip.hashed)
    else: form = TripEmpForm(instance=objects)
    context = {
        'form': form, 
        'title': 'Altera Funsionario', 'legend': 'Altera Funsionario'
    }
    return render(request, 'trip/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def mTripEmpDelete(request, hashid):
    objects = get_object_or_404(TripEmp, hashed=hashid)
    objects.delete()
    messages.success(request, f'Susesu Delete')
    return redirect('t-list')


@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTripUpdateAtt(request, hashid, pk):
    group = request.user.groups.all()[0].name
    trip = get_object_or_404(Trip, hashed=hashid)
    emp = get_object_or_404(TripEmp, pk=pk)
    per = pd.date_range(start=trip.date_out, end=trip.date_in, freq='B')
    if trip.ttype.pk == 1:
        attstatus = get_object_or_404(AttendanceStatus, pk=4)
    elif trip.ttype.pk == 2:
        attstatus = get_object_or_404(AttendanceStatus, pk=13)
    if len(per) > 0:
        for i in per:
            print(i)
            newid, hashedid = getnewid(Attendance)
            y = trip.date_out.year
            m = trip.date_out.month
            year = get_object_or_404(Year, year=y)
            month = get_object_or_404(Month, pk=m)
            created = Attendance.objects.create(
            id = newid,
            unit = emp.employee.curempdivision.unit,
            employee = emp.employee,
            year = year,
            month = month,
            date = i,
            status_am = attstatus,
            status_pm = attstatus,
            datetime=datetime.datetime.now(),
            user=request.user,
            hashed = hashedid)
            emp.is_update = True
            emp.save()
    else:
        print('CALL')


    messages.success(request, 'Susesu Altera')
    return redirect('m-t-detail', hashid)

@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrTripDeleteAtt(request, hashid):
    group = request.user.groups.all()[0].name
    trip = get_object_or_404(Trip, hashed=hashid)
    # emp = get_object_or_404(TripEmp, pk=pk)

    per = pd.date_range(start=trip.date_out, end=trip.date_in, freq='B')
    for i in per:
        date_str = f'{i.year}-{i.month}-{i.day}'
        date_period = dt.strptime(date_str,"%Y-%m-%d").date()
        emp = TripEmp.objects.filter(trip=trip)
        for e in emp:
            print(e.hashed)
            attendance = Attendance.objects.filter(employee=e.employee, date=date_period).last()
            print(attendance)
            if attendance:
                attendance.delete()
    trip.delete()

    messages.success(request, 'Susesu Delete Trip')
    return redirect('t-list')