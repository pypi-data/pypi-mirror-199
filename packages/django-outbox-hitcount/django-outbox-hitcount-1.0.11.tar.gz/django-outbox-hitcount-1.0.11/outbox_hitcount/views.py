import datetime

import pytz
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from hitcount.models import Hit, HitCount

from .common_date import add_months, get_week_date


def get_statistic(site_id, is_cache=False): 
    ''' 
        Tambah fitur cache, jika True maka cache data statistik sesuai dengan data yg tidak berubah lagi untuk 1 hari
        1 Jam = 60 Menit = 3600 Detik
        24 Jam = 24 * 3600 Detik = 86400 Detik
    '''
    time_zone = getattr(settings, 'TIME_ZONE', 'UTC') # get setting timezone
    tz = pytz.timezone(time_zone)   
    context = {}
    # tgl = datetime.datetime.now()
    tgl = timezone.now()
    # Domain = request.get_host()    
    # site_id = get_site_id(request)

    # Update 1 Des 2022
    # Tambah hitcount_id dari tabel Hit agar perhitungan khusus model tertentu saja
    # tahapan untuk mendapatkan hitcount_id adalah :
    # 1. Aktifkan model (get data model)
    # 2. Dapatkan content_type_id
    # 3. Dapatkan hitcount ID
    
    # implementasi :
    # 1. site_id sudah ada (site_id variabel di atas)
    # 2. content_type_id
    content_type_id = ContentType.objects.get(app_label='sites', model='site')
    content_type_id = content_type_id.id if content_type_id else None   # harus ada None
    
    ## CARA LAIN DAPATKAN CONTENT TYPE
    # content_type = ContentType.objects.filter(model='site').first()
    
    # 3. Dapatkan hitcount ID
    hitcount_id = HitCount.objects.filter(content_type_id=content_type_id, object_pk=site_id).first()
    hitcount_id = hitcount_id.id if hitcount_id else None

    # hitcount_id di gunakan di semua kondisi di bawah ini ....
    # kondisi DOMAIN sudah tidak diperlukan lagi
    # Hal ini membuktikan tambahan field Domain di model hit dan hitcount sebenarnya tidak di perlukan 
    # (Update langsung dari hitcount source menjadi mungkin dilakukan)
    # ---------------------------------------------------------

    # start date jika mengabaikan jam
    # maka bagian jam 0:0:0 mulai pukul 0 (benar)
    # Jika mengabaikan jam, seharusnya end data berakhiran 23:59:59 bukan 0:0:0
    # supaya end data tetap dihitung
    # end_date = datetime.date(tgl.year, tgl.month, tgl.day)
    
    # RULE CAHCE :
    # TIDAK DI CACHE (Mulai di CACHE yesterday dst)
    # TIDAK DI CACHE online juga
    # timeout = 86400 # in second = 1 Day
    # Perubahan setelah jam 00:00:00 malam atau setelah pergantian hari
    # buat cache ini expired saat pergantian hari
    # hitung jumlah detik dari waktu sekarang sampai jam 00:00:00 nanti malam
    # Plus 1 menit untuk antisipasi expired sebelum jam 00:00
    # jika expired sebelum jam 00:00 kemidan hit count di update ke cache maka satu hari full data akan salah karena masih mengambil data kemarin
    # tgl = waktu sekarang
    tgl00 = tgl + datetime.timedelta(days=1)
    jam00 = datetime.datetime(tgl00.year, tgl00.month, tgl00.day, 0, 1, 0, tzinfo=tz) # 60 adalah tambahan waktu 1 menit untuk antisipasi kesalahan refresh data ke cache
    # jam00 = tz.localize(jam00)
    timeout = (jam00-tgl00).seconds
    selisih = 0 # untuk pengujung tambahan yg terhitung mulai jam 00:00

    # PERUBAHAN RULE, khusus unutk minggu ini dan bulan ini
    # Gunakan cara, update manual tanpa membaca database lagi
    # Misal data pengunjung hari ini sudah disimpan 5
    # kemudian 1 jam berikutnya menjadi 8
    # berarti ada penambahan 3, maka
    # tambah juga data 3 ini ke pengunjung minggu ini dan bulan ini
    # HIT_TODAY digunakan untuk menyimpan pengunjung update jam 00:00
    # cari selisih dnegan pengunjung hari ini, hasilnya
    # tambahkan ke pengujung minggu ini dan bulan ini


    # a, b = divmod(timeout, 3600)
    # print('expired in next', str(a), str(b//60))
    tmp = 'hit_today'
    tmp_cache = cache.get(tmp, version=site_id)

    if not (is_cache and tmp_cache is not None): # karena kondisi tmp_cache = 0 maka tetap masuk kondisi load from DB
        print('load from DB (' + tmp + ')')

        # Abaikan jam, ambil hari ini saja
        hit_today = Hit.objects.filter(hitcount_id=hitcount_id, created__year=tgl.year, created__month=tgl.month, created__day=tgl.day)
        
        # error expected string or bytes-like object!!! jika menggunakan cara di bawah ini
        # hit_today = Hit.objects.filter(hitcount_id=hitcount_id, created__date=tgl.date())
        # print('hit_today',hit_today)

        tmp_cache = hit_today.count() if hit_today else 1
        
        # save to cache for next time
        cache.set(tmp, tmp_cache, timeout, version=site_id)

        # return to context (Ini di update jam 00:00)
        context[tmp] = tmp_cache
    else: 
        # Ini di UPDATE tiap pengujung datang

        # Abaikan jam, ambil hari ini saja
        hit_today = Hit.objects.filter(hitcount_id=hitcount_id, created__year=tgl.year, created__month=tgl.month, created__day=tgl.day)
        # hit_today = Hit.objects.filter(hitcount_id=hitcount_id, created__date=tgl.date)
        # print('hit_today',hit_today)
        context[tmp] = hit_today.count() if hit_today else 1

        selisih = context[tmp] - tmp_cache
        print('selisih = ', selisih)
    # if hit_today:        
    #     context['hit_today'] = hit_today.count()
    # else:
    #     context['hit_today'] = 1    # paling tidak ada 1 yg berkunjung hari ini (diri anda sendiri)

    # ref : https://docs.djangoproject.com/en/4.1/topics/cache/
    # 1. kemarin
    # ----------------------------------------------------------------------
    tmp = 'hit_yesterday'
    tmp_cache = cache.get(tmp, version=site_id)
    # tmp_cache = 0 if tmp_cache is None else tmp_cache
    
    # print('cache=',tmp_cache)

    if not (is_cache and tmp_cache is not None): # karena kondisi tmp_cache = 0 maka tetap masuk kondisi load from DB
        print('load from DB (' + tmp + ')')
        # context[tmp] = tmp_cache
        # else:    
        # abaikan jam juga, ambil hari kemarin
        start_date = tgl + datetime.timedelta(days=-1)
        # start_date = datetime.date(start_date.year, start_date.month, start_date.day)   # abaikan jam
        # end_date = datetime.date(tgl.year, tgl.month, tgl.day)
        tmp_cache = Hit.objects.filter(hitcount_id=hitcount_id, \
            created__year=start_date.year, created__month=start_date.month, created__day=start_date.day).count()
        # tmp_cache = Hit.objects.filter(hitcount_id=hitcount_id, \
        #     created__date=start_date.date).count()

        # save to cache for next time
        cache.set(tmp, tmp_cache, timeout, version=site_id)
    
    # Return to context        
    context[tmp] = tmp_cache

    # 2. Minggu INI (Tidak di cache, karena selalu berubah, jika pengunjung hari ini bertambah
    # Data minggu ini juga bertambah)
    # Rule berubah khusus minggu ini dan bulan ini
    # ----------------------------------------------------------------------
    tmp = 'hit_this_week'
    tmp_cache = cache.get(tmp, version=site_id)

    if not (is_cache and tmp_cache is not None): # karena kondisi tmp_cache = 0 maka tetap masuk kondisi load from DB
        print('load from DB (' + tmp + ')')
        # abaikan jam, ambil data dalam 1 minggu
        start_date, end_date = get_week_date(tgl.year, tgl.month, tgl.day)
        start_date = tz.localize(start_date)
        end_date = tz.localize(end_date)
        # print(start_date, end_date)

        # start_date = tgl + datetime.timedelta(days=-7)
        # start_date = datetime.date(start_date.year, start_date.month, start_date.day) # abaikan jam        
        # end_date = datetime.datetime(tgl.year, tgl.month, tgl.day, 23, 59, 59)

        tmp_cache = Hit.objects.filter(hitcount_id=hitcount_id, \
            created__range=(start_date, end_date)).count()
        # save to cache for next time
        cache.set(tmp, tmp_cache, timeout, version=site_id)

    tmp_cache += selisih # Tambahan ini saja
    context[tmp] = tmp_cache


    # 3. Minggu LALU
    # ----------------------------------------------------------------------
    tmp = 'hit_last_week'
    tmp_cache = cache.get(tmp, version=site_id)

    if not (is_cache and tmp_cache is not None): # karena kondisi tmp_cache = 0 maka tetap masuk kondisi load from DB
        print('load from DB (' + tmp + ')')
        # abaikan jam, ambil data 1 minggu yg lalu
        # start_date = tgl + datetime.timedelta(days=-14)
        # start_date = datetime.date(start_date.year, start_date.month, start_date.day) # abaikan jam
        # end_date = tgl + datetime.timedelta(days=-7)
        # end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59) # abaikan jam
        start_date, end_date = get_week_date(tgl.year, tgl.month, tgl.day)
        start_date = start_date + datetime.timedelta(days=-7)
        end_date = end_date + datetime.timedelta(days=-7)
        start_date = tz.localize(start_date)
        end_date = tz.localize(end_date)
        
        # print('=', start_date, end_date)

        tmp_cache = Hit.objects.filter(hitcount_id=hitcount_id, \
            created__range=(start_date, end_date)).count()
        # save cache
        cache.set(tmp, tmp_cache, timeout, version=site_id)

    context[tmp] = tmp_cache


    # 4. BULAN INI
    # ----------------------------------------------------------------------
    tmp = 'hit_this_month'
    tmp_cache = cache.get(tmp, version=site_id)

    if not (is_cache and tmp_cache is not None): # karena kondisi tmp_cache = 0 maka tetap masuk kondisi load from DB
        print('load from DB (' + tmp + ')')

        # abaikan jam, ambil data bulan ini () (Bukan tgl sekarang sampai 1 bulan ke belakang, karena berbeda jumlah hari dalam 1 bulan)
        tmp_cache = Hit.objects.filter(hitcount_id=hitcount_id, \
            created__year=tgl.year, created__month=tgl.month).count()

        # save cache
        cache.set(tmp, tmp_cache, timeout, version=site_id)

    tmp_cache += selisih
    context[tmp] = tmp_cache


    # 5. BULAN LALU
    # ----------------------------------------------------------------------
    tmp = 'hit_last_month'
    tmp_cache = cache.get(tmp, version=site_id)

    if not (is_cache and tmp_cache is not None): # karena kondisi tmp_cache = 0 maka tetap masuk kondisi load from DB
        print('load from DB (' + tmp + ')')

        # abaikan jam, ambil dari bulan lalu
        start_date = add_months(tgl,-1)
        tmp_cache = Hit.objects.filter(hitcount_id=hitcount_id, \
            created__year=start_date.year, created__month=start_date.month).count()
        # save cache
        cache.set(tmp, tmp_cache, timeout, version=site_id)

    context[tmp] = tmp_cache

    # abikan menit dan detik
    # ambil 3 jam terakhir untuk penanda user online (ubah dari 1 jam menjadi 3 jam (agar tampak lebih banyak))
    

    # Update 1 Des 2022, 
    # Ambil 5 jam terakhir dan ip unique
    start_date = tgl + datetime.timedelta(hours=-5) # abaikan menit dan detik
    start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, start_date.hour, 0, 0, tzinfo=tz) # abaikan menit dan detik
    # end_date = tgl
    end_date = datetime.datetime(tgl.year, tgl.month, tgl.day, tgl.hour, 59, 59, tzinfo=tz) # abaikan menit dan detik
    hit_online = Hit.objects.filter(hitcount_id=hitcount_id, \
        created__range=(start_date, end_date)).values('user_agent').order_by('user_agent').distinct()

    # IP masih sama, ganti menjadi user_agent

    # Ambil data 3 jam terakhir, dengan ip unique, itu dianggap jumlah user yg sedang online
    context['hit_online'] = hit_online.count() if hit_online else 1

    # if hit_online:        
    #     context['hit_online'] = hit_online.count() 
    # else: # tetap perlu 1, karena pengunjung yg sama tidak di hitung lagi sampai hari berikutnya
    #     context['hit_online'] = 1 # paling tidak ada 1 yg online

    # context['hit_all'] = Hit.objects.filter(domain=Domain).count()
    # hit terbaru di ambil dari ringkasan, karena mencakup seluruh pengunjung dari awal website online
    # data ada di hit_count bukan di hit (karena tabel ini akan di hapus dalam waktu 2 bulan, secara manual di hapus)

    # Update di OPD (pending)

    ## CARA LAIN DAPATKAN CONTENT TYPE
    # content_type = ContentType.objects.filter(model='site').first()
    tmp = 'hit_all'
    tmp_cache = cache.get(tmp, version=site_id)

    if not (is_cache and tmp_cache is not None): # karena kondisi tmp_cache = 0 maka tetap masuk kondisi load from DB
        print('load from DB (' + tmp + ')')


        hit_count = HitCount.objects.filter(object_pk = site_id, content_type_id = content_type_id) #, domain=Domain)
        tmp_cache = hit_count[0].hits if hit_count else 1
        # if hit_count:
        #     context['hit_all'] = hit_count[0].hits
        # else:   
        #     context['hit_all'] = 1 # mengikuti jumlah site Online dan hitcount 1 hari 
        cache.set(tmp, tmp_cache, timeout, version=site_id)

    tmp_cache += selisih
    context[tmp] = tmp_cache

    # RETURN
    return context
