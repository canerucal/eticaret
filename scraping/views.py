from django.shortcuts import render
# import scraper

# Create your views here.
def index(request):
    return render(request, 'index.html')