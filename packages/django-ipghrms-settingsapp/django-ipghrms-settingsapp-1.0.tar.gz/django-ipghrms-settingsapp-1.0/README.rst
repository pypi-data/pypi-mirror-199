
============================
Django IPG HRMS settings_app
============================


Quick start
============


1. Add 'settings_app' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'settings_app'
    ]

2. Include the settings_app to project URLS like this::

    path('settings_app/', include('settings_app.urls')),

3. Run ``python manage.py migrate`` to create settings_app model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user