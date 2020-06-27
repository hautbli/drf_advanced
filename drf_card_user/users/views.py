from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwner
from users import serializers
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        print(self.action)
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()

    # 토큰 로그 아웃..
    @action(detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": ugettext_lazy("Successfully logged out.")},
                            status=status.HTTP_200_OK)

        return response

    #  캐시!!
    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
