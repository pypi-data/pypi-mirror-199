import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from trip.models import Trip, TripEmp, TripType
from custom.models import Position
from settings_app.user_utils import c_unit, c_dep
from employee.models import Employee
from datetime import datetime as dt
import calendar

class APIContEmpTrip(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        emp = Employee.objects.filter(status__pk=1)
        categories = list()
        ltrip = list()
        otrip = list()
        month = calendar.month_name[dt.now().month] 
        year = dt.now().year

        for obj in emp:
            local_trip = TripEmp.objects.filter(employee=obj, trip__ttype__pk=1).count()
            overseas_trip = TripEmp.objects.filter(employee=obj, trip__ttype__pk=2).count()
            categories.append(obj.first_name + ' ' + obj.last_name )
            ltrip.append(local_trip)
            otrip.append(overseas_trip)
        data = { 'categories': categories, 'lt': ltrip, 'ot': otrip, 'legend': f'Summary of Official Trips per employees until {month} {year}'}
        return Response(data)
    
class APITripTotal(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        label = list()
        obj = list()
        trip_type = TripType.objects.all()
        for i in trip_type:
            annual_leave = TripEmp.objects.filter(trip__ttype=i).count()
            obj.append({
                'name': i.name,
                'y': annual_leave
            })
        data = { 'label': 'All Staff Official Trips', 
        'obj': obj,  'label2':label}
        return Response(data)


