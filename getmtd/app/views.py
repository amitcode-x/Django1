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
        name = request.GET.get("name")
        email = request.GET.get("email")
        phone = request.GET.get("phone")
        msg = request.GET.get("message")
        print(name+ email+ phone+msg)
    except:
        pass
    # finalans = 0
    # try:
    #     n1 = int(request.GET['num1'])
    #     n2 = int(request.GET['num2'])
    #     finalans = n1 + n2
       
    
    # except:
    #     pass
    # return render(request, 'Userform.html',{'output':finalans})
    return render(request, 'Userform.html')
