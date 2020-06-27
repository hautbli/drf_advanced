from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from cards import serializers
from cards.models import Card
from cards.permissions import IsOwner


class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = serializers.CardSerializer

    # token은 request 데이터..?!
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()
