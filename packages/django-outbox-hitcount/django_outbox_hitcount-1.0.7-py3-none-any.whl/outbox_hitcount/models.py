from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

class HitLocation(models.Model):
    '''
        Table Master
        Cek location unique, do not duplicate value in name
        192.168.13.29
    '''
    country = models.CharField(max_length=50, default=None, null=True)
    city = models.CharField(max_length=50, default=None, null=True)
    ip_address = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HitDevice(models.Model):
    '''
        Table Master
        Cek device unique, do not duplicate value in name
        example:
        Tab, Hp, Desktop/Laptop
    '''
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HitOS(models.Model):
    '''
        Table Master
        Cek Operating System unique, do not duplicate value in name
        Linux, mac os, Windows, android
    '''
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HitBrowser(models.Model):
    '''
        Table Master
        Cek Browser unique, do not duplicate value in name
        Firefox, chrome, 
    '''
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HitCount(models.Model):
    """
    Table Transaksi (jumlah hit)

    Base class for hitcount models.

    Model that stores the hit totals for any content object.

    """
    # count = models.PositiveIntegerField(default=0)
    count = models.PositiveBigIntegerField(default=0)
    end_date = models.DateTimeField()  # last date in month (ringkasan dari tanggal 1, simpan sebagai tanggal akhir dari tiap bulan)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

    # count di atas, misal berjumlah 10
    # maka hit browser misal chrome, firefox, dll, jumlahnya harus 10
    # hit os, misal andorid, linux, windows, jumlahnya harus 10 juga

    hits_browser = models.ManyToManyField(HitBrowser) #, through="HitCountBrowser")
    # field ini pindahan dari tabel intemediate, lebih tepat di letakkan di tabel ini
    # browser_count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width

    hits_os = models.ManyToManyField(HitOS) #, through="HitCountOS")
    # os_count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width

    hits_device = models.ManyToManyField(HitDevice) #, through="HitCountDevice")
    # device_count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width

    hits_location = models.ManyToManyField(HitLocation) #, through="HitCountLocation")
    # location_count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width

    # link ke object, bisa berita, sita, artikel, dll
    # , related_name="content_type_set_for_%(class)s"
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_pk')


# class HitCountBrowser(models.Model):
#     '''
#         # Tabel pertengahan di relasi many2many dengan tambahan field
#         Many to many relationship with additional fields
#     '''
#     hit_count = models.ForeignKey(HitCount, on_delete=models.CASCADE)
#     hit_browser = models.ForeignKey(HitBrowser, on_delete=models.CASCADE)

#     # count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width
#     # Fitur cropping mengikuti data ini
#     # image_width = models.SmallIntegerField()    # ukuran gambar width
#     # image_height = models.SmallIntegerField()   # ukuran gambar height

# class HitCountOS(models.Model):
#     '''
#         # Tabel pertengahan di relasi many2many dengan tambahan field
#         Many to many relationship with additional fields
#     '''
#     hit_count = models.ForeignKey(HitCount, on_delete=models.CASCADE)
#     hit_os = models.ForeignKey(HitOS, on_delete=models.CASCADE)

#     # count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width

# class HitCountDevice(models.Model):
#     '''
#         # Tabel pertengahan di relasi many2many dengan tambahan field
#         Many to many relationship with additional fields
#     '''
#     hit_count = models.ForeignKey(HitCount, on_delete=models.CASCADE)
#     hit_device = models.ForeignKey(HitDevice, on_delete=models.CASCADE)

#     # count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width

# class HitCountLocation(models.Model):
#     '''
#         # Tabel pertengahan di relasi many2many dengan tambahan field
#         Many to many relationship with additional fields
#     '''
#     hit_count = models.ForeignKey(HitCount, on_delete=models.CASCADE)
#     hit_location = models.ForeignKey(HitLocation, on_delete=models.CASCADE)

#     # count = models.PositiveBigIntegerField(default=0)    # ukuran gambar width
