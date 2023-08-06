import calendar
import datetime
# 
# from datetime import timedelta

def get_last_day_of_month(year, month):
    return calendar.monthrange(year,month)[1]

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    # day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    day = min(sourcedate.day, get_last_day_of_month(year, month))
    return datetime.datetime(year, month, day)

def get_week_date(year, month, day):
    '''
        Ambil tanggal awal dan akhir 

        misal : calendar (2022,12)
        tgl skrg = 3
        maka ambil tanggal awal = 28/11 
        tanggal akhir = 4/12 

        [0, 0, 0, 1, 2, 3, 4]
        [5, 6, 7, 8, 9, 10, 11]
        [12, 13, 14, 15, 16, 17, 18]
        [19, 20, 21, 22, 23, 24, 25]
        [26, 27, 28, 29, 30, 31, 0]
        
    '''
    cal = calendar.Calendar()
    cal = cal.monthdatescalendar(year, month)
    mfound = False
    i = 0 # init

    for i in range(0, len(cal)-1):
        for j in cal[i]:
            if j.day == day:
                mfound = True
                break

        if mfound: break

    # index ada di i
    week_begin = cal[i][0]
    week_begin = datetime.datetime(week_begin.year, week_begin.month, week_begin.day, 0, 0, 0)
    week_end = cal[i][6]
    week_end = datetime.datetime(week_end.year, week_end.month, week_end.day, 23, 59, 59)

    # untuk last week tinggal dikurangi 7 hari week_begin dan week_end
    return (week_begin, week_end) # return tuple
