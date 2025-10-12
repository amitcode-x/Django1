from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def conditional(request):
    
    data = {
        'title': 'if else',
        'dis': ' welcom to if else',
        'fruits' :['mango','apple','graps', 'banana'],
        "numbers": [10,20,30,50,45,55,66,77],
        "num" : []
    }
    return render(request,'index.html',data)


