from rest_framework.serializers import ModelSerializer, ReadOnlyField

from cards.models import Card


class CardSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    # user = UserSerializer() -> 무한으로 list가 출력됨..!!!
    class Meta:
        model = Card
        fields = ['id', 'user', 'date', 'content']
