from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from django.http import HttpResponse

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    




def home(request):
    return HttpResponse("<h2>Welcome to Django Backend 👋</h2><p>Go to /api/products/ to see products.</p>")

