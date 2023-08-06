
============================
Django IPG HRMS log
============================


Quick start
============


1. Add 'log' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'log'
    ]

2. Include the log to project URLS like this::

    path('log/', include('log.urls')),

3. Run ``python manage.py migrate`` to create log model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user