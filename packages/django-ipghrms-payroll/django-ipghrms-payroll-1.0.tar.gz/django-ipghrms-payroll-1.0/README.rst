
============================
Django IPG HRMS payroll
============================


Quick start
============


1. Add 'payroll' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'payroll'
    ]

2. Include the payroll to project URLS like this::

    path('payroll/', include('payroll.urls')),

3. Run ``python manage.py migrate`` to create payroll model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user