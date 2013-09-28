from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render, redirect

from .models import CookieCutter
from .forms import GeneratorForm


def cookiecutter_detail(request, username, cookie):
    cookie = get_object_or_404(CookieCutter, user__username=username, name=cookie)
    return render(request, 'cookiecutters/detail.html', {'cookie': cookie})


def bake(request, username, cookie):
    cookie = get_object_or_404(CookieCutter, user__username=username, name=cookie)
    if request.method == 'POST':
        options = dict(request.POST)
        tasks.exec_cookiecutter(cookie, request.user.id, options)
        return redirect('/success')

    return render(request, 'cookiecutters/bake.html', {'cookie': cookie})



class CookieGeneratorView(DetailView):
    context_object_name = 'cookie'
    model = CookieCutter
    template_name = 'cookiecutters/generator.html'

    def get_context_data(self, **kwargs):
        context = super(CookieGeneratorView, self).get_context_data(**kwargs)

        context['form'] = GeneratorForm(context['cookie'])

        return context
