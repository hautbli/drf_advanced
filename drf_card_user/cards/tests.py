from datetime import datetime
from pprint import pprint

from django.test import TestCase
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from cards.models import Card


class CardTestCase(APITestCase):
    def setUp(self) -> None:
        u1 = baker.make('auth.User')
        u2 = baker.make('auth.User')
        u3 = baker.make('auth.User')
        self.users = [u1, u2, u3]
        self.cards = baker.make('cards.Card', _quantity=4, user=u1)
        self.cards += baker.make('cards.Card', _quantity=4, user=u2)
        self.cards += baker.make('cards.Card', _quantity=4, user=u3)

    def test_should_list(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get('/api/cards')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for card_response, card in zip(response.data['results'], self.cards[::-1]):
            self.assertEqual(card_response['id'], card.id)
            self.assertEqual(card_response['content'], card.content)

        # self.fail()

    def test_should_create(self):
        data = {'content': 'test', 'date':'2019-09-09'}
        self.client.force_authenticate(user=self.users[0])

        response = self.client.post('/api/cards', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        card_response = response.data
        print(card_response)
        self.assertTrue(card_response['id'])
        self.assertEqual(card_response['content'], data['content'])

    def test_should_get(self):
        card = self.cards[0]
        self.client.force_authenticate(user=self.users[0])

        response = self.client.get(f'/api/cards/{card.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        card_response = Munch(response.data)
        self.assertTrue(card_response.id)
        self.assertEqual(card_response.content, card.content)

    def test_should_update(self):
        card = Card.objects.filter(user_id=self.users[0].id).first()
        prev_content = card.content
        data = {'content': 'new_contents!', 'date':'2019-09-09'}

        print(card.user.id, self.users[0].id)
        self.client.force_authenticate(user=self.users[0])

        response = self.client.put(f'/api/cards/{card.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        card_response = Munch(response.data)
        print(card_response)

        self.assertNotEqual(card_response.content, prev_content)
        self.assertEqual(card_response.content, data['content'])

    def test_should_delete(self):
        card = self.cards[0]
        self.client.force_authenticate(user=self.users[0])

        response = self.client.delete(f'/api/cards/{card.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Card.objects.filter(id=card.id).exists())

    # def test(self):
    #     self.client.force_authenticate(card=self.cards[0])
    #     self.client.get('/api/cards/fastcampus')
