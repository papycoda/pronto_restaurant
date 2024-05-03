from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def HomePageView (request):
    return render(request, 'index.html')

def MenuView (request):
    return render(request, 'menu.html')

def AboutView(request):
    return render(request, 'about.html')

def BookView(request):
    return render(request, 'book.html')

