from .models import Estate
from django.shortcuts import render


def index(request):
    estates = Estate.objects.order_by('-created_at')
    return render(request, 'sreality.html', {'estates': estates, 'header': "Sreality"})
