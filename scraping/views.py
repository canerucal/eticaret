from django.shortcuts import render
# import scraper

# Create your views here.
def index(request):
    deneme_liste = [1,2,3,4,5]
    return render(request, 'index.html', {
        'deneme_liste': deneme_liste
    })