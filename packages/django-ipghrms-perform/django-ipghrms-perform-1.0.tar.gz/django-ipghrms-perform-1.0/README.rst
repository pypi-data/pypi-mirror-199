
============================
Django IPG HRMS perform
============================


Quick start
============


1. Add 'perform' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'perform'
    ]

2. Include the perform to project URLS like this::

    path('perform/', include('perform.urls')),

3. Run ``python manage.py migrate`` to create perform model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user