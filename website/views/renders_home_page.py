from django.shortcuts import render

def get_home_page(request):
    if request.method == 'GET':
        return render(request , 'website/home.html')