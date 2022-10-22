from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from webapp.models import Messages
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User


  
class MessageReportTest(APITestCase):

    def setUp(self):

        self.title = "Could your school"
        self.start_date='2022-04-20'
        self.end_date='2022-05-27'
        self.post_date='2022-04-27'
        self.no_likes=20
        self.post_id=1
        self.post_category='facebook'
        self.post_thumbnail= "https://www.facebook.com/mygobubble/photos/a.358205154599834/1257648327988841/"
        self.post= "Could your school win the award for being the Happiest in your country? Now open to all schools. More details here bit.ly/GBHappyAward",
        self.username='admin_test'
        self.password='iD5GEy7K4u6j0'

        self.user = User.objects.create_user(username=self.username,password=self.password)
       
        user_data={'username':self.username,'password':self.password}
        response = self.client.post(reverse('auth'),user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['data']['token'])
     

        
    def test_authenticate_end_point(self):
        user_data={'username':self.username,'password':self.password}
        response = self.client.post(reverse('auth'),user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login Successful')

    def test_get_all_message(self):
        response = self.client.get(reverse('messages'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_with_valid_message_id(self):
        response = self.client.get('/api/messages/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_with_invalid_message_id(self):
        response = self.client.get('/api/messages/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_message_with_invalid_start_date_end_date(self):
        response = self.client.get('/api/messages/?start_date={}&end_date={}'.format('20-34-20', '20-04-200'))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_message_with_start_date_end_date(self):
        response = self.client.get('/api/messages/?start_date={}&end_date={}'.format(self.start_date, self.end_date))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
   
    def test_get_message_with_no_of_like_as_string(self):
        response = self.client.get('/api/messages/?no_likes={}'.format('e40'))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_message_with_no_of_like_as_Integer(self):
        response = self.client.get('/api/messages/?no_likes={}'.format(self.no_likes))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_with_post_category(self):
        response = self.client.get('/api/messages/?post_category={}'.format(self.post_category))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



