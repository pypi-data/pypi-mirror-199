
============================
Django IPG HRMS training
============================


Quick start
============


1. Add 'training' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'training'
    ]

2. Include the training to project URLS like this::

    path('training/', include('training.urls')),

3. Run ``python manage.py migrate`` to create training model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user