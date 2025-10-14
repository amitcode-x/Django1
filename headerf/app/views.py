from django.shortcuts import render


def home(request):
    return render(request, "Home.html")

# Create your views here.
