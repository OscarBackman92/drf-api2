from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase

class PostTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test')
    
    def test_can_list_posts(self):
        test = User.objects.get(username='test')
        Post.objects.create(owner=test, title="a title")
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))
        
    def test_logged_in_user_can_create_post(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class PostDetailTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='adam')
        Brian = User.objects.create_user(username='Brian', password='Brian')
        Post.objects.create(owner=adam, title="a title")
        Post.objects.create(owner=Brian, title="another title")
        
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'a title')
    
    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_can_update_post_using_valid_id(self):
        self.client.login(username='adam', password='adam')
        response = self.client.put('/posts/1/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'new title')
    
    def test_cannot_update_post_using_invalid_id(self):
        self.client.login(username='adam', password='adam')
        response = self.client.put('/posts/3/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_cannot_update_post_if_not_owner(self):
        self.client.login(username='adam', password='adam')
        response = self.client.put('/posts/2/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)