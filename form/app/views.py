from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    
  
    return render(request, 'contact.html' )
def action(request):
    return HttpResponse('This is action page')
def Userform(request):
    
    
  
    
    result = ""
    try:
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        msg = request.POST.get("message", "")
        result = f" name: {name} email: {email} phone: {phone} message: {msg}"
        print( name, email, phone,msg)
    
       
    except:
        pass
   
    return render(request, 'Userform.html',{'output':result})
