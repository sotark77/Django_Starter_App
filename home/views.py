from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')

def blog_list(request):
    return render(request, 'home/blogs.html')

def blog_view(request):
    return render(request, 'home/blog_view.html')
