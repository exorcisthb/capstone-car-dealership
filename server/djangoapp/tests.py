"""
Minimal tests to verify the API endpoints work end-to-end.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from djangoapp.models import Dealer, CarMake, Review
from djangoapp.sentiment import analyze_sentiment


class SentimentTestCase(TestCase):
    def test_positive(self):
        sentiment, _ = analyze_sentiment("Fantastic services and great staff")
        self.assertEqual(sentiment, 'positive')

    def test_negative(self):
        sentiment, _ = analyze_sentiment("Terrible rude horrible service")
        self.assertEqual(sentiment, 'negative')

    def test_neutral(self):
        sentiment, _ = analyze_sentiment("The car is blue and has four wheels")
        self.assertEqual(sentiment, 'neutral')


class DealerAPITestCase(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(
            full_name='Test Dealer', city='Testville', state='KS',
            address='1 Test St', zip_code='12345',
        )

    def test_get_dealers(self):
        resp = self.client.get('/djangoapp/dealers')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['dealers']), 1)

    def test_get_dealer_by_id(self):
        resp = self.client.get(f'/djangoapp/dealer/{self.dealer.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['dealer']['full_name'], 'Test Dealer')

    def test_get_dealers_by_state(self):
        resp = self.client.get('/djangoapp/dealers/state/KS')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['dealers']), 1)


class AuthAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', 'a@a.com', 'Pass1234')

    def test_login(self):
        c = Client()
        resp = c.post('/djangoapp/login',
                      data={'userName': 'alice', 'password': 'Pass1234'},
                      content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['status'])

    def test_login_wrong_password(self):
        c = Client()
        resp = c.post('/djangoapp/login',
                      data={'userName': 'alice', 'password': 'wrong'},
                      content_type='application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(resp.json()['status'])

    def test_logout(self):
        c = Client()
        c.post('/djangoapp/login',
               data={'userName': 'alice', 'password': 'Pass1234'},
               content_type='application/json')
        resp = c.post('/djangoapp/logout')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['status'])


class ReviewAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('bob', 'b@b.com', 'Pass1234')
        self.dealer = Dealer.objects.create(
            full_name='Bobs Cars', city='KC', state='KS',
            address='1 St', zip_code='12345',
        )

    def test_get_dealer_reviews(self):
        Review.objects.create(dealer=self.dealer, name='x', review_text='Great!', sentiment='positive')
        resp = self.client.get(f'/djangoapp/reviews/dealer/{self.dealer.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['reviews']), 1)

    def test_analyze_endpoint(self):
        resp = self.client.get('/djangoapp/analyze?text=Fantastic services')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['sentiment'], 'positive')

    def test_add_review_requires_login(self):
        # Without login: @login_required returns 302 (redirect to login)
        resp = self.client.post('/djangoapp/reviews/add',
                                data={'dealer_id': self.dealer.id, 'review': 'nice'},
                                content_type='application/json')
        self.assertIn(resp.status_code, (302, 403))
