from django.db import models

class Brand(models.Model):
    product_id = models.TextField(primary_key=True)
    brand = models.TextField()
    model_name = models.TextField()
    model_no = models.TextField()
    photo_1 = models.TextField()
    photo_2 = models.TextField()
    photo_3 = models.TextField()
    photo_4 = models.TextField()
    photo_5 = models.TextField()

    class Meta:
        db_table = 'brand'

    def __str__(self) -> str:
        return f"{self.product_id} {self.brand} {self.model_name} "

class Hardware(models.Model):
    product_id = models.TextField(primary_key=True)
    os = models.TextField()
    cpu = models.TextField()
    cpu_gen = models.TextField()
    ram = models.TextField()
    ssd_size = models.TextField()
    hdd_size = models.TextField()
    screen_size = models.TextField()

    class Meta:
        db_table = 'hardware'

    def __str__(self) -> str:
        return f"{self.product_id} {self.os} {self.cpu} {self.ram} "

class SiteInfo(models.Model):
    product_id = models.TextField(primary_key=True)
    product_point = models.IntegerField()
    price = models.IntegerField()
    website = models.TextField()
    url = models.TextField()

    class Meta:
        db_table = 'site_info'

    def __str__(self) -> str:
        return f"{self.product_id} {self.product_point} {self.price} {self.website} "