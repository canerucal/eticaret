from django.shortcuts import render
from scraping.models import Brand
import pandas as pd

def getData():
    global brands, brand_db, os_type, cpu, cpu_gen, ram, screen_size, website
    brands = Brand.objects.values_list('brand', flat=True).order_by('brand').distinct()
    brand_db = Brand.objects.values()
    os_type = Brand.objects.values_list('os', flat=True).order_by('os').distinct()
    Brand.objects.filter(os="FREE DOS").update(os="FREEDOS")
    cpu = Brand.objects.values_list('cpu', flat=True).order_by('cpu').distinct()
    cpu_gen = Brand.objects.values_list('cpu_gen', flat=True).order_by('cpu_gen').distinct()
    ram = Brand.objects.values_list('ram', flat=True).distinct()
    screen_size = Brand.objects.values_list('screen_size', flat=True).distinct()
    website = Brand.objects.values_list('website', flat=True).order_by('website').distinct()

def index(request):
    getData()
    return render(request, 'index.html', {
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })

def lowPrice(request):
    getData()
    brand_db = Brand.objects.values().order_by("price")
    return render(request, 'low_price.html', {
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })

def highPrice(request):
    getData()
    brand_db = Brand.objects.values().order_by("-price")
    return render(request, 'high_price.html', {
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })

def hplp(request):
    getData()
    brand_db = Brand.objects.values().order_by("-product_point").order_by("price")
    return render(request, 'hplp.html', {
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })