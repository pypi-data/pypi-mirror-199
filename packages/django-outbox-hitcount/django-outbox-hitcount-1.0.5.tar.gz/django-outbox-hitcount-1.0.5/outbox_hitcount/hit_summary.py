import calendar
import datetime
import json
import os
import random
import time
from datetime import timedelta

import httpagentparser
import pytz
import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from hitcount.models import Hit

from outbox_hitcount.models import *

# from urllib2 import urlopen

def get_last_day_of_month(year, month):
    return calendar.monthrange(year,month)[1]

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    # day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    day = min(sourcedate.day, get_last_day_of_month(year, month))
    return datetime.datetime(year, month, day)

def get_geolocation_opt3(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
    '''
    res = requests.get('http://ip-api.com/json/' + str_ip_address) # 45 request per minute
    if res:
        res = res.json()
        if res['status'] =='success':
            return (res['country'], res['city'])
    return None

def get_geolocation_opt1(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
        exp: 180.243.14.149
    '''
    result = os.popen("curl https://ipapi.co/"+ str_ip_address +"/json/").read() # 1000 per hari
    if result:
        return (result['country_name'], result['city'])
    return None    

def get_geolocation_opt2(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
    '''        
    res = requests.get('http://ipwho.is/' + str_ip_address) # 10.000 request per minute    
    if res:
        res = res.json()
        if res['success']:
            return (res['country'], res['Seoul'])                    
    return None 

def get_geolocation_opt4(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
    '''        
    result = os.popen("curl http://api.db-ip.com/v2/free/"+ str_ip_address).read() # 1000 per hari
    if result:
        return (result['countryName'], result['city'])
    return None     

# ada version yg belum bagus di split sehingga tersimpan 
# X 10.15.5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15 (Applebot/0.1
def correct_version(version):
    if version.strip():
        tmp = version.replace("(","<-!->")
        tmp = tmp.replace(")","<-!->")
        return tmp.split("<-!->")[0]
    return version

def is_field_exists(model, field):
    # for field in cls._meta.get_fields(include_hidden=True):
    #     if field.name == field:
    #         return True
    # return False
    try:
        field = model._meta.get_field(field)
        return True
    except FieldDoesNotExist:
        return False

# def get_for_object(obj, end_date):
#     ctype = ContentType.objects.get_for_model(obj)    
#     hit_count, created = get_or_create(content_type=ctype, object_pk=obj.pk)
#     return hit_count

def get_or_set_browser(browser):
    name = browser.get('name') if browser else None    
    version = browser.get('version') if browser else None
    
    # jika masih kosong karena tidak ada data maka set not defined
    if not name: name = 'none'
    if not version: version = 'none'
    version = correct_version(version)

    browser, created = HitBrowser.objects.get_or_create(name=name, version=version)
    return browser    

def get_or_set_os(os):
    name = os.get('name') if os else None    
    version = os.get('version') if os else None
    
    # jika masih kosong karena tidak ada data maka set not defined
    if not name: name = 'none'
    if not version: version = 'none'
    version = correct_version(version)

    os, created = HitOS.objects.get_or_create(name=name, version=version)
    return os

def get_or_set_device(device):
    name = device.get('name') if device else None    
    version = device.get('version') if device else None
    
    # jika masih kosong karena tidak ada data maka set not defined
    if not name: name = 'none'
    if not version: version = 'none'
    version = correct_version(version)

    device, created = HitDevice.objects.get_or_create(name=name, version=version)
    return device

def get_or_set_location(ip_address):
    '''
        Location: '192.168.13.29' format string IP ADDRESS
        Khusus location field version tidak ada di ganti ip_address
        kode unik cukup IP address saja
    '''
    # ip_address = location.get('ip_address') if location else None        
    
    # jika masih kosong karena tidak ada data maka set not defined
    if not ip_address: ip_address = 'none'    

    location, created = HitLocation.objects.get_or_create(ip_address=ip_address)
    return location

def hitcount_insert_m2m_field(hit_count, browser, os, platform, ip_address):    # param type dict
    # hit_count = data.get('hit_count')
    # browser = data.get('browser')
    # os = data.get('os')
    # platform = data.get('platform')
    # ip_address = data.get('ip_address')

    obj = get_or_set_browser(browser)
    hit_count.hits_browser.add(obj)
    # hit_count.browser_count += 1

    # get or set os
    obj = get_or_set_os(os)
    hit_count.hits_os.add(obj)
    # hit_count.os_count += 1

    # get or set device
    obj = get_or_set_device(platform)
    hit_count.hits_device.add(obj)
    # hit_count.device_count += 1

    # get or set location
    obj = get_or_set_location(ip_address)
    hit_count.hits_location.add(obj)
    # hit_count.location_count += 1

    # hit_count.save()

def special_condition(object_pk, end_date):
    '''
        Special condition:
        if site_id exists
            but object_pk not found, search on other model
            update hitcount for all model
    '''
    # jika di model yg aktif tidak ada
    model_priority = ['artikel', 'berita', 'galery_video', 'galery_foto', 'halaman_statis', 'link_terkait', 'pengumuman', 'social_media']

    for i in model_priority:
        ct = ContentType.objects.filter(model=i)
        if ct:
            ct_class = ct.get().model_class()
            if is_field_exists(ct_class, 'site'):
                obj = ct_class.objects.filter(id=object_pk) # cari site_id dari model
                site_id = None
                if obj:                    
                    site_id = obj.get().site_id

                    if site_id:
                        site = Site.objects.filter(id=site_id) # cari nama site dari site_id yg di dapat
                        if site:
                            site = site.get()
                            content_type_site = ContentType.objects.get_for_model(site)

                            hit_count, created = HitCount.objects.get_or_create(
                                content_type=content_type_site, 
                                object_pk=site_id,
                                defaults={'end_date': end_date, 'site_id': site_id}
                            )
                            hit_count.count += 1
                            
                            # hit_count.update(count=F(count)+1)

                            data = {
                                'hit_count': hit_count,
                                'browser': browser,
                                'os': os,
                                'platform': platform,
                                'ip_address': ip_address
                            }
                            hitcount_insert_m2m_field(**data)
                            hit_count.save()        
                    

@transaction.atomic
def do_summary(qs, end_date):
    j=0
    count = qs.count()
    for i in qs:
        ip_address = i.ip
        user_agent = i.user_agent
        user_agent_parser = httpagentparser.detect(user_agent)

        platform = user_agent_parser.get('platform')
        os = user_agent_parser.get('os')
        # bot = user_agent_parser.get('bot')
        # dist = user_agent_parser.get('dist')
        browser = user_agent_parser.get('browser')

        # hitcount_id = i.hitcount.id
        object_pk = i.hitcount.object_pk
        print('---')
        # print()

        content_type = i.hitcount.content_type
        content_type_id = content_type.id        
        j+=1
        print(int(j), 'of', int(count), ':object_pk', object_pk, 'model', content_type.model, 'hitcount_id', i.hitcount.id)
        site_id = None

        # dari content type ubah mejadi object
        # dari object, cek apakah ada field site_id
        # jika ada ambil PK dari object ini
        # ct = ContentType.objects.get_for_id(content_type_id)

        # print('content type=', content_type)

        ct_class = content_type.model_class()
        
        # print('ct_class=', ct_class)

        # print('ct=', ct)
        # ct_class = ct.model_class()
        # print('ct_class=', ct_class)

        # Jika ct_class tidak ada berarti model tersebut tidak di temukan di project
        # misal galery_video
        if ct_class:
            print(ct_class._meta.get_fields())

            # obj = ct.get_object_for_this_type(id=object_pk)
            # print('ct_class=', ct_class)
            
            # print('obj=', obj)
            #             
            # cek apakah ada field site ID    
            mfound = False        
            if is_field_exists(ct_class, 'site'):
                obj = ct_class.objects.filter(id=object_pk) # cari site_id dari model
                if obj:                    
                    site_id = obj.get().site_id
                    print('site_id', site_id)
                    mfound = True
                else:
                    print('site_id', object_pk, 'tidak ditemukan!')
            else:
                print('site_id tidak ditemukan di model')

            if not mfound:
                special_condition(object_pk, end_date)

        # 1. jika ada field site_id, maka insert summary baru content_type = site
        if site_id:
            site = Site.objects.filter(id=site_id) # cari nama site dari site_id yg di dapat
            if site:
                site = site.get()
                content_type_site = ContentType.objects.get_for_model(site)

                hit_count, created = HitCount.objects.get_or_create(
                    content_type=content_type_site, 
                    object_pk=site_id,
                    defaults={'end_date': end_date, 'site_id': site_id}
                )
                hit_count.count += 1
                
                # hit_count.update(count=F(count)+1)

                data = {
                    'hit_count': hit_count,
                    'browser': browser,
                    'os': os,
                    'platform': platform,
                    'ip_address': ip_address
                }
                hitcount_insert_m2m_field(**data)
                hit_count.save()                

        # 2. default insert content_type dari apa adanya data di Hit
        # content_type = ContentType.objects.get_for_model(i)
        hit_count, created = HitCount.objects.get_or_create(
            content_type=content_type,  # data sudah ada di paling atas
            object_pk=object_pk,
            defaults={'end_date': end_date, 'site_id': site_id if site_id > 0 else None}
        )
        hit_count.count += 1
        # hit_count.save()
        # hit_count.update(count=F(count)+1)

        data = {
            'hit_count': hit_count,
            'browser': browser,
            'os': os,
            'platform': platform,
            'ip_address': ip_address
        }
        hitcount_insert_m2m_field(**data)
        hit_count.save()

def auto_hit_summary(month_count=-1): # proses jumlah bulan, jika -1 maka semua di proses
    '''
        Should be auto run in midnight
    '''
    time_zone = getattr(settings, 'TIME_ZONE', 'UTC') # get setting timezone
    tz = pytz.timezone(time_zone)    

    grace = getattr(settings, 'HITCOUNT_KEEP_HIT_IN_DATABASE', {'days': 30})
    period = timezone.now() - timedelta(**grace)
    # qs = Hit.objects.filter(created__lt=period)

    # seluruh data yg akan diringkas ada di qs
    # filter lagi per bulan
    # if qs:

    # ambil bulan dan tahun untuk di filter lagi
    # first_data = qs[0]

    # month_count = 1 # looping sejumlah month_count, jika -1 berarti semua data
    mcount = 5 # batasi looping 5 kali jika hasil query set kosong
    # month = period.month
    # year = period.year
    # end_day_of_month = get_last_day_of_month(year, month)    # return hari

    # # dapatkan range tanggal yang benar
    # begin_date = datetime.date(year, month, 1) # pukul 0:0:0
    # end_date = datetime.date(year, month, end_day_of_month, 23, 59, 59)
    tmp = add_months(period, 1) # karena proses awal add_month2 -1 maka di add dulu disini
    begin_date = datetime.datetime(tmp.year, tmp.month, 1)

    # mulai ambil data di database
    while mcount > 0:
        begin_date = add_months(begin_date, -1)
        year = begin_date.year
        month = begin_date.month
        end_day_of_month = get_last_day_of_month(year, month)    # return hari
        end_date = datetime.datetime(year, month, end_day_of_month, 23, 59, 59)
        
        # add time zone
        begin_date = tz.localize(begin_date)
        end_date = tz.localize(end_date)

        qs = Hit.objects.filter(created__gte=begin_date, created__lte=end_date)
        if not qs:
            mcount -= 1
        else:
            do_summary(qs, end_date)
            
            if month_count > 0: month_count -= 1
            if month_count == 0: break
            

@transaction.atomic                            
def auto_get_location(request_per_minute=30, max_data=500):   
    '''
        Batasi hit per ment 30 saja agar tidak di banned oleh situs gratisan
        jalankan menggunakan celery
        batasi max data 500
    '''
    start_time = datetime.datetime.now()
    stop_time = start_time + timedelta(minutes=1)

    hit_location = HitLocation.objects.filter(name='')[:max_data]
    count = 0
    waiting_list = [1, 2, 3, 4, 5, 6, 7]  # random list
    loc = 'loc1'

    for i in hit_location:
        count += 1
        ip_address = i.ip_address
        if count<=request_per_minute:
            location = get_geolocation_opt1(ip_address)
            loc = 'loc1'

            if not location: 
                location = get_geolocation_opt2(ip_address)
                loc = 'loc2'

            if not location: 
                location = get_geolocation_opt3(ip_address)
                loc = 'loc3'

            if not location: 
                location = get_geolocation_opt4(ip_address)
                loc = 'loc4'

            if not location:
                print('Location Not Found', ip_address)
                loc = 'none'
            else:
                i.country = location[0]                    
                i.city = location[1]                    
                print('Update location', ip_address, 'to', location, 'from', loc)
                i.save()     
                time.sleep(random.choice(waiting_list)) # sleep 1 detik agar tidak kentara
        else:
            while datetime.datetime.now() < stop_time:
                print('Waiting for 1 minute')
                time.sleep(random.choice(waiting_list)) # sleep 5 detik

            # reset count
            count = 0
            start_time = datetime.datetime.now()
            stop_time = start_time + timedelta(minutes=1)
            print('Reset variable')

        
