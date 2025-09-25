from django.shortcuts import render
from django.http import HttpResponse

def Home(request):
    return HttpResponse("<b style='color:blue; background-color:yellow;'>Hello, World!</b>")
def About(request):
    return HttpResponse("<b style='color:blue; background-color:yellow;'>   About us!</b>")
# Create your views here.
def Contact(request):
    return HttpResponse("<b style='color:blue; background-color:yellow;'>   Contact us!</b>")

def Services(request):
    return HttpResponse("<b style='color:blue; background-color:yellow;'>   Services!</b>")
def Products(request):
    return HttpResponse("<b style='color:blue; background-color:yellow;'>   Products!</b>")
def CoursesDetails(request,corseid=0):
    return HttpResponse(f"<b style='color:blue; background-color:yellow;'>   Courses Details : {corseid}!</b>")
def Courses(request):
    return HttpResponse("<b style='color:blue; background-color:yellow;'>   Courses!</b>")