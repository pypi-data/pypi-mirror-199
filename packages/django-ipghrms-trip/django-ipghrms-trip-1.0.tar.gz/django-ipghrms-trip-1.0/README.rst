
============================
Django IPG HRMS trip
============================


Quick start
============


1. Add 'trip' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'trip'
    ]

2. Include the trip to project URLS like this::

    path('trip/', include('trip.urls')),

3. Run ``python manage.py migrate`` to create trip model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user