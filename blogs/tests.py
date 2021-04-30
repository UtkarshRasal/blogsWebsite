from rest_framework.test import APITestCase, force_authenticate, APIClient
from django.urls import reverse
from accounts.models import User
from blogs.models import Blogs

class BlogsTesting(APITestCase):
    fixtures = ['configuration.json']

    def test_list(self):
        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = client.get('/blogs/', format='json')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 4)
    
    def test_create(self):

        data = {
	        "title": "testBlog",
	        "content": "Hey this a test comment",
	        "tags": [{
		                "name": "test"
	                }, {
		                "name": "blog"
	                }]
        }

        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION= 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = client.post('/blogs/',data=data, format='json')
        _data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(_data['status'], True)
        self.assertEqual(_data['data']['title'], 'testBlog')
    
    def test_update(self):
        data = {
	        "title": "testBlog hey",
	        "content": "Hey this a test comment",
	        "tags": [{
		                "name": "test"
	                }, {
		                "name": "blog"
	                }]
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION= 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = self.client.put('/blogs/cb9aafb5-87be-4a28-951d-bc1aeed0e00b/',data=data, format='json')
        _data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(_data['status'], True)
        self.assertEqual(_data['data']['title'], 'testBlog hey')
    
    def test_partial_update(self):
        data = {
            "title":"sampleBlog"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION= 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = client.patch('/blogs/cb9aafb5-87be-4a28-951d-bc1aeed0e00b/', data=data, format='json')
        _data = response.json()

        self.assertEqual(response.status_code, 201)
    
    def test_delete(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION= 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = client.delete('/blogs/cb9aafb5-87be-4a28-951d-bc1aeed0e00b/', format='json') 
        data = response.json()

        self.assertEqual(response.status_code, 200)

    def test_leaderboard(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION= 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = client.get('/blogs/leaderboard/', format='json')
        _data = response.json()

        self.assertEqual(response.status_code, 200)
        
    def test_post_comment(self):

        data = {
            "comment":"Hey this is a test comment"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION= 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = self.client.post('/blogs/cb9aafb5-87be-4a28-951d-bc1aeed0e00b/post_comment/', data=data, format='json')
        _data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(_data['status'], True)
    
    def test_comment_list(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION= 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMjE5NTkwLCJqdGkiOiI2MmRhZGVlY2JmNTA0YTVhOThkNTM1ZGM0Y2NmNTRiNiIsInVzZXJfaWQiOiIxZjNhNTJmOC0zOTY2LTQ5N2QtYTk0OC00N2I2Y2MyZTQxYzEifQ.Y11FDfQQhyPopOfOTMuBQGyvFyX_5vc1dM_cCxieQcs')
        response = client.get('/blogs/cb9aafb5-87be-4a28-951d-bc1aeed0e00b/comment/', format='json')
        _data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(_data['status'], True)

class TagsTesting(APITestCase):

    def test_list(self):

        response = self.client.get('/tags/', format='json')
        data = response.json()

        self.assertEqual(response.status_code, 200)