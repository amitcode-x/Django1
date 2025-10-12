from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def forl(request):
    
    data = {
        'title': 'for loop',
        'dis': ' welcom to for loop',
        'fruits' :['mango','apple','graps', 'banana'],
        'students' :[
            {'name': 'amit', "mobile" : 123}
        ]
    }
    return render(request,'index.html',data)


