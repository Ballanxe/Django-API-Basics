from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse

from posting.models import BlogPost
User = get_user_model()

# automated
# new / blank db

class BlogPostAPITestCase(APITestCase):

	def setUp(self):
		user_obj = User(username="testcfeuser", email='email@deprueba.com')
		user_obj.set_password('somerandompassword')
		user_obj.save()
		blog_post = BlogPost.objects.create(
			user=user_obj,
			title='New title',
			content='some_random_content'
			)

	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_post(self):
		post_count = BlogPost.objects.count()
		self.assertEqual(post_count, 1)

	def test_get_list(self):
		data = {}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.get(url,data,format='json')
		self.assertEqual(response.status_code,  status.HTTP_200_OK)
		# print(response.data)


	def test_post_item(self):

		data = {"title":"Some randem title","content":"some randome content"}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.post(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


	def test_get_item(self):
		blog_post = BlogPost.objects.first()
		data = {}
		url = blog_post.get_api_url()
		response = self.client.get(url,data,format='json')
		self.assertEqual(response.status_code,  status.HTTP_200_OK)
		# print(response.data)


	def test_update_item(self):

		blog_post = BlogPost.objects.first()
		url = blog_post.get_api_url()
		data = {"title":"Some randem title","content":"some randome content"}
		response = self.client.post(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
		response = self.client.put(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


		# self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_update_item_with_user(self):

		blog_post = BlogPost.objects.first()
		print(blog_post.content)
		url = blog_post.get_api_url()
		data = {"title":"Some randem title","content":"some randome content"}
		user_obj = User.objects.first()
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION="JWT" + token_rsp)

		response = self.client.put(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print(response.data)

	def test_post_item_with_user(self):

		user_obj = User.objects.first()
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION="JWT" + token_rsp)
		data = {"title":"Some randem title","content":"some randome content"}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.post(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_user_ownership(self):

		owner = User.objects.create(username="tstuser2222")
		blog_post = BlogPost.objects.create(
				user=owner,
				title='New title',
				content='new content'
			)
		user_obj = User.objects.first()
		self.assertNotEqual(user_obj.username,owner.username)
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION="JWT" + token_rsp)

		url = blog_post.get_api_url()
		data = {"title":"Some randem title","content":"some randome content"}
		response = self.client.put(url,data,format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_user_login_and_update(self):
		data = {
			'username':'testcfeuser',
			'password':'somerandompassword'
		}
		url = api_reverse("api-login")
		response = self.client.post(url,data)
		print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		token = response.data.get("token")

		if token is not None:

			blog_post = BlogPost.objects.first()
			url = blog_post.get_api_url()
			data = {"title":"Some randem title","content":"some randome content"}
			self.client.credentials(HTTP_AUTHORIZATION="JWT" + token)

			response = self.client.put(url,data,format='json')
			self.assertEqual(response.status_code, status.HTTP_200_OK)
			print(response.data)
