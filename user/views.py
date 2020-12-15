from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, 'user/main.html')


@login_required
def home(request):
    return render(request, 'user/home.html')
