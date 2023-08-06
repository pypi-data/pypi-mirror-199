# DJANGO OUTBOX HITCOUNT

Project to make hitcount information more complex. Base on https://github.com/thornomad/django-hitcount, we build advance version that make device, OS, Browser, IP Geolocation, available in your website.

All you need to do is:   

## In your django Environment

### Install package to your environment
    > pip install django-outbox-hitcount

### Add to INSTALLED_APPS
    INSTALLED_APPS = [        
        'django.contrib.sites', 
        'outbox_hitcount',
    ]

### Add SITE_ID in user settings.py
    SITE_ID = 1
    
    # This setting just like django-hitcount library
    HITCOUNT_KEEP_HIT_ACTIVE = { 'hours': 1 }
    # HITCOUNT_HITS_PER_IP_LIMIT = 0  # unlimited
    # HITCOUNT_EXCLUDE_USER_GROUP = ()  # not used
    HITCOUNT_KEEP_HIT_IN_DATABASE = { 'days': 90 } 

### Install requirements
    Activate your environment using
    > mkvirtualenv env_hitcount

### Migrate to create table to your database
    > python manage.py migrate

### Run project
    > python manage.py runserver
    on you browser :
    127.0.0.1:8000
