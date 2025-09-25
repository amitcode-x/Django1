from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def Home(request):
    return render(request, "Home.html")
def loop(request):
    data={
        'numbers': range(1,11)
    }
    return render(request, "loop.html", data)
def data(request):
    data={
        'data':[1,2,3,4,5,6,7,8,9,10]
        }
    return render(request, "data.html",data )

