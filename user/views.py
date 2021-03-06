from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.views import generic

from .forms import MemoryCreateForm


def main(request):
    return render(request, 'user/main.html')


@login_required
def home(request):
    return render(request, 'user/home.html')


class MemoryCreateView(generic.CreateView):
    form_class = MemoryCreateForm
    template_name = 'user/memory-create.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect('/?next=/home/create')
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Checking fields """
        if not self.request.user.is_anonymous:
            form = self.form_class(request.POST)
            user = self.request.user
            if form.is_valid():
                memory = form.save(commit=False)
                memory.user = user
                memory.save()
                return HttpResponseRedirect(reverse('home'))
            return render(request, self.template_name, {'form': form})
        return HttpResponseNotFound("You are not authorized.")
