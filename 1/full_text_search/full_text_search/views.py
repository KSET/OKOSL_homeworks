# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, 'full_text_search/index.html')
