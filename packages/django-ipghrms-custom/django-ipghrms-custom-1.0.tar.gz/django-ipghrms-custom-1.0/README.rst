
============================
Django IPG HRMS custom
============================


Quick start
============


1. Add 'custom' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'custom'
    ]

2. Include the custom to project URLS like this::

    path('custom/', include('custom.urls')),

3. Run ``python manage.py migrate`` to create custom model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user