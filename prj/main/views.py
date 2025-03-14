from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def one(request):
    return render(request, 'main/one.html')

def two(request):
    return render(request, 'main/two.html')
