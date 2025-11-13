from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def calculator(request):
    if request.method =='POST':
        num1 = request.POST.get('num1')
        num2 = request.POST.get('num2')
        operation = request.POST.get('operation')
        result = None

        if num1 and num2:
            num1 = float(num1)
            num2 = float(num2)

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 != 0:
                    result = num1 / num2
                else:
                    result = 'Error: Division by zero'

    return render(request, 'calculator.html', {'result': result})


def Homepage(request):
    return HttpResponse("Welcome calculator app")