from django.db import models

class Scrape(models.Model):
    op_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50, null=True)
    model_name = models.CharField(max_length=50)
    model_no = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    cpu = models.CharField(max_length=50)
    cpu_type = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    disk_size = models.CharField(max_length=50)
    disk_type = models.CharField(max_length=50)
    point = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    site_name = models.CharField(max_length=50)
    site_url = models.CharField(max_length=250, null=True)

    class Meta:
        db_table = 'scrape'

    def __str__(self) -> str:
        return f"{self.op_id} {self.model_name} {self.site_name} {self.price}₺ "
