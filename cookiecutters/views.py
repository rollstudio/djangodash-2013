from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from celery.result import AsyncResult

from cookiecutters.models import CookieCutter
from cookiecutters import tasks

from .serializers import CookieCutterSerializer


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        s = CookieCutterSerializer(CookieCutter.objects.all(), many=True)

        context['cookies'] = JSONRenderer().render(s.data)

        return context


class JSONBakeView(generics.RetrieveAPIView):
    model = CookieCutter
    serializer_class = CookieCutterSerializer

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        cookie = self.kwargs.get('cookie', None)

        return get_object_or_404(CookieCutter, user__username=username,
                                 name=cookie)


class CookieListView(generics.ListAPIView):
    model = CookieCutter
    serializer_class = CookieCutterSerializer


class CookieDetailView(generics.RetrieveAPIView):
    model = CookieCutter
    serializer_class = CookieCutterSerializer

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        cookie = self.kwargs.get('cookie', None)

        return get_object_or_404(CookieCutter, user__username=username,
                                 name=cookie)


class BakeCookieView(APIView):
    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        cookie = self.kwargs.get('cookie', None)

        return get_object_or_404(CookieCutter, user__username=username,
                                 name=cookie)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()

        form = obj.form(request.DATA)

        if form.is_valid():
            task = tasks.exec_cookiecutter.delay(
                obj, form.cleaned_data, request.user.id, form.use_github
            )

            return Response({
                'task_id': task.id,
                'url': reverse('task_status', args=(task.id,)),
            }, status.HTTP_201_CREATED)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class BakingStatusView(APIView):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get('task_id')

        res = AsyncResult(task_id)

        return Response({
            'status': res.status,
            'result': res.result,
        }, status.HTTP_200_OK)
