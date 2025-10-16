from django.shortcuts import render
from django.http import HttpResponse

def course(request):
    return render(request,"course.html")

def subject(request):
    return render(request,"subject.html")

def home(request):
    return HttpResponse ("hello this is home page")

# Create your views here.
