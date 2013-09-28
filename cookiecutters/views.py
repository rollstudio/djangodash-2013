from django.views.generic import DetailView

from .models import CookieCutter
from .forms import GeneratorForm


class CookieGeneratorView(DetailView):
    context_object_name = 'cookie'
    model = CookieCutter
    template_name = 'cookiecutters/generator.html'

    def get_context_data(self, **kwargs):
        context = super(CookieGeneratorView, self).get_context_data(**kwargs)

        context['form'] = GeneratorForm(context['cookie'])

        return context
