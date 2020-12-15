from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def main(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        return render(request, 'user/main.html')


@login_required
def home(request):
    return render(request, 'user/home.html')
