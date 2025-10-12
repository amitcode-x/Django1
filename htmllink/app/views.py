from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return render(request,"index.html")

def datapass(request):
    
    data = {
        
        "title": "data pass",
        'discription': ' this is datapass concepts'
    }
    
    return render(request,"index1.html",data)
    
    

    
# Create your views here.
