from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render, redirect

from cookiecutters.models import CookieCutter
from cookiecutters import tasks


def cookiecutter_detail(request, username, cookie):
    cookie = get_object_or_404(CookieCutter, user__username=username, name=cookie)
    return render(request, 'cookiecutters/detail.html', {'cookie': cookie})


def bake(request, username, cookie):
    cookie = get_object_or_404(CookieCutter, user__username=username, name=cookie)

    if request.method == 'POST':
        form = cookie.form(request.POST)
        if form.is_valid():
            tasks.exec_cookiecutter(cookie, form.cleaned_data, request.user.id, form.use_github)
            #return redirect('/success')
            return render(request, 'cookiecutters/bake_success.html', locals())
    else:
        form = cookie.form()

    return render(request, 'cookiecutters/bake.html', locals())



class CookieGeneratorView(DetailView):
    context_object_name = 'cookie'
    model = CookieCutter
    template_name = 'cookiecutters/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CookieGeneratorView, self).get_context_data(**kwargs)

        context['form'] = GeneratorForm(context['cookie'])

        return context
