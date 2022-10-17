from django.db import models

class Brand(models.Model):
    url = models.TextField(primary_key=True)
    brand = models.TextField()
    model_name = models.TextField()
    model_no = models.TextField()
    photo = models.TextField()

    class Meta:
        db_table = 'brand'

    def __str__(self) -> str:
        return f"{self.brand.upper()} ---- {self.model_name.upper()} "

class Hardware(models.Model):
    url = models.TextField(primary_key=True)
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
        return f"{self.os.upper()}---{self.cpu.upper()}---{self.cpu_gen.upper()}---{self.ram.upper()} "

class SiteInfo(models.Model):
    url = models.TextField(primary_key=True)
    product_point = models.TextField()
    price = models.TextField()
    website = models.TextField()

    class Meta:
        db_table = 'site_info'

    def __str__(self) -> str:
        return f"{self.website.upper()}---{self.product_point}---{self.price}"