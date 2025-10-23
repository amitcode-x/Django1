from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')
def Userform(request):
    try:
        name = request.GET("name")
        email = request.GET("email")
        phone = request.GET("phone")
        msg = request.GET("message")
        print(name+ email+ phone+msg)
    except:
        pass
    
    # try:
    #     n1 = request.GET['num1']
    #     n2 = request.GET['num2']
    #     print(n1+n2)
    
    # except:
    #     pass
    return render(request, 'Userform.html')
