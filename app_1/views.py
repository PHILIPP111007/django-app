from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

  
def index(request):
	return render(request, 'index.html')

def text(request):
	return render(request, 'text.html')