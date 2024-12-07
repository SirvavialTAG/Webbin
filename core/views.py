from django.shortcuts import render
from django.http import HttpResponse

def empty(request):
    return render(request, 'empty.html')