from django.shortcuts import get_object_or_404, render

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from celery.result import AsyncResult

from cookiecutters.models import CookieCutter
from cookiecutters import tasks

from .serializers import CookieCutterSerializer


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

        form = obj.form(request.POST)

        if form.is_valid():
            task = tasks.exec_cookiecutter.delay(obj, form.cleaned_data, request.user.id, form.use_github)

            print task.status

            return Response({
                'task_id': task.id
            }, status.HTTP_201_CREATED)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class BakingStatusView(APIView):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get('task_id')

        res = AsyncResult(task_id)

        return Response({
            'status': res.status
        }, status.HTTP_200_OK)

