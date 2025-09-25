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

