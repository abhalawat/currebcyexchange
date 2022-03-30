from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class WalletTest(APITestCase):
    # success Test cases
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        self.token = Token.objects.create(user=self.user)

    def testcase1(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/wallet/view/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def testcase2(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/wallet/deposit/', data={"amount": 1000},
                                    HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def testcase3(self):
        self.client.force_login(user=self.user)
        self.client.post('/wallet/deposit/', data={"amount": 1000},
                         HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.post('/wallet/withdraw/', data={"amount": 10},
                                    HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def testcase4(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/wallet/crypto_trans/',
                                    data={"fromAdd": 'alice', "toAdd": "bob", "tokenId": 1, "quantity": "10"},
                                    HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    # Negative Test Cases
    # def testcase5(self):
    #     self.client.logout()
    #     # self.client.force_login(user=self.user)
    #     response = self.client.get('/wallet/view/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
    #     print(response.data)
    #     self.assertEqual(response.status_code, 401)

    def testcase6(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/wallet/deposit/', data={"amount": -1000},
                                    HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, 404)

    def testcase7(self):
        self.client.force_login(user=self.user)
        self.client.post('/wallet/deposit/', data={"amount": 1000},
                         HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.post('/wallet/withdraw/', data={"amount": -10},
                                    HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, 404)

    def testcase8(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/wallet/withdraw/', data={"amount": 10},
                                    HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        # Log out
        # self.client.logout()
        # Check response code
        response = self.client.get('/demo/')
        self.assertEquals(response.status_code, 404)
