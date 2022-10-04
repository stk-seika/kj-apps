from django.shortcuts import render

def index(request):
    return render(request, 'kj-apps/index.html')