from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import RequestContext, loader

# Create your views here.

def index(request):
    template = loader.get_template('barchart/treemap.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

