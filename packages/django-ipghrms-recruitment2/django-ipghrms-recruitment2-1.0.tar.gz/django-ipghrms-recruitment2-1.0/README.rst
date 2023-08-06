
============================
Django IPG HRMS recruitment2
============================


Quick start
============


1. Add 'recruitment2' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'recruitment2'
    ]

2. Include the recruitment2 to project URLS like this::

    path('recruitment2/', include('recruitment2.urls')),

3. Run ``python manage.py migrate`` to create recruitment2 model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user