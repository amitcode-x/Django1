from django.shortcuts import render

def home(request):
    return render(request,"index.html")
def index1(request):
    return render(request,"index1.html")


# Create your views here.
