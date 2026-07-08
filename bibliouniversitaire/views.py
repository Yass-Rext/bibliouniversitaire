#from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime  
def index(request):
    dateaujour= datetime.today()
    return render(request, "bibliouniversitaire/index.html", context={"date": dateaujour})