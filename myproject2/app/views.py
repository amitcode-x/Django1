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
        'data':[1,2,3,4,5,6,7,8,9,10],
        'name':"Amit chauhan",
        'place':"India",
        'fruits':["mango","banana","orange","grapes"]
        }
    return render(request, "data.html",data )

def table(request):
    data = {
        'numbers': range(1, 7),
        'squares': [i**2 for i in range(1, 7)],
        'cubes': [i**3 for i in range(1, 7)],
        'fourths': [i**4 for i in range(1, 7)],
        'fifths': [i**5 for i in range(1, 7)],
        'sixths': [i**6 for i in range(1, 7)],
    }
    return render(request, "table.html", data)

