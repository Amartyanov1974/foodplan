from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'index.html',)

def login(request):
    context = {}
    return render(request, 'index.html', )
