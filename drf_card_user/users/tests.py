from django.contrib.auth.models import User
from django.test import TestCase
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from model_bakery import baker


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        # self.user = User.objects.create() 이렇게 하나하나 넣기 힘ㄷ름..
        #  for !!! unique!!!!!

        self.users = baker.make('auth.User', _quantity=3)
        baker.make('cards.Card', user=self.users[0])

    def test_should_list(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get('/api/users')

        print(response.data['results'])
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for user_response, user in zip(response.data['results'], self.users[::-1]):
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)

    def test_should_create(self):
        data = {'username': 'abc'}
        response = self.client.post('/api/users', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = response.data

        self.assertTrue(user_response['id'])
        self.assertEqual(user_response['username'], data['username'])

    def test_should_get(self):
        user = self.users[0]
        self.client.force_authenticate(user=user)

        response = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, user.username)

    def test_should_update(self):
        user = self.users[0]
        prev_username = user.username

        data = {'username': 'newname'}
        self.client.force_authenticate(user=user)

        response = self.client.put(f'/api/users/{user.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertNotEqual(user_response.username, prev_username)
        self.assertEqual(user_response.username, data['username'])

    def test_should_delete(self):
        user = self.users[0]
        self.client.force_authenticate(user=user)

        response = self.client.delete(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(pk=user.id).count(), 0)
        self.assertFalse(User.objects.filter(id=user.id).exists())


    def test(self):
        self.client.force_authenticate(user=self.users[0])
        self.client.get('/api/users/logout')

        # self.fail()
    def test_should_logout(self):
        user = self.users[0]
        self.client.force_authenticate(user=self.users[0])

        respnse = self.client.get('/api/users/logout')
        token = Token.objects.filter(pk=user.id).exists()

        self.assertEqual(respnse.status_code, status.HTTP_200_OK)
        self.assertFalse(token)

