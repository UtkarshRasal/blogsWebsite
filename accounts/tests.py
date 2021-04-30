# from rest_framework.test import APITestCase
# from django.urls import reverse
    
# class TestViews(TestSetUp):

#     def test_user_cannot_register_with_no_data(self):
#         response = self.client.post(self.register_url)
#         self.assertEqual(response.status_code, 400)
    
#     def test_user_can_register_correctly(self):
#         user_data = {
#             'first_name': 'utkarsh',
#             'last_name':'Rasal',
#             'email': 'email@gmail.com',
#             'password': 'email@email'
#         }
#         import pdb;pdb.set_trace()
#         response = self.client.post(self.register_url, data = user_data, format='json')
#         data = response.json()

#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(data['data']['email'], 'email@gmail.com')

