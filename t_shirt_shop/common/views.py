from django.shortcuts import render

# Create your views here.


def homepage_view(request):
    return render(request, template_name='common/homepage.html')

