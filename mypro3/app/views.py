from django.shortcuts import render
from django.http import HttpResponse


def  aboutUs(request):
    return HttpResponse('Welcome to about page')
def  Home(request):
    return HttpResponse('Welcome to home page')

def  course(request):
    return HttpResponse(f'Welcome to course page')
def  coursedtl(request,courseid):
    return HttpResponse(f'Welcome to course page{courseid}')


