from django.shortcuts import render,redirect


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    
    # ye hai redirect k liye logic doubt ho to ja kr video no 27 dekh lena wscubetech ka
    # if request.method == "GET":
    #     output = request.GET.get('output', '')
    # return render(request, 'contact.html',{'output':output}  )
    return render(request, 'contact.html' )
def Userform(request):
    
    
    # <!-- this is for save the data in input section after submit the form -->
    
    # data = {}
    
    result = ""
    try:
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        msg = request.POST.get("message", "")
        result = f" name: {name} email: {email} phone: {phone} message: {msg}"
        
       
        
        
        print( name, email, phone,msg)
        # <!-- this is for save the data in input section after submit the form -->
        # data = {
        #     'name': name,
        #     'email': email,
        #     'phone': phone,
        #     'message': msg,
        #         'result': result
        #  }
        # url ="contact?output={}".format(result)
        return redirect("contact")
    except:
        pass
    # finalans = 0
    # try:
    #     n1 = int(request.POST.get['num1'])
    #     n2 = int(request.POST.get['num2'])
    #     finalans = n1 + n2
          
       
    
    # except:
    #     pass
    # return render(request, 'Userform.html',{'output':finalans})
    
    # this is for save the data in input section after submit the form 
    # return render(request, 'Userform.html',data)
    return render(request, 'Userform.html',{'output':result})
