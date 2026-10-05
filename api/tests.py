from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Import your models (adjust the import path based on your app name)
from .models import Category, Transaction 

User = get_user_model()

class BaseAPITestCase(APITestCase):
    """
    Base test class that sets up a user and authenticates the test client with a JWT.
    """
    def setUp(self):
        # 1. Create a test user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword123',
            role='student'
        )
        
        # 2. Generate JWT tokens for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # 3. Authenticate the test client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


class CategoryCRUDTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = '/api/categories/'

    def test_create_category(self):
        payload = {'name': 'Groceries', 'description': 'Food items'}
        response = self.client.post(self.list_url, payload, format='json')
        # FIX: Changed create_response to response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Failed to create Category: {response.data}")

    def test_read_category_list(self):
        payload = {'name': 'Utilities', 'description': 'Monthly bills'}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Setup failed: {response.data}")
        
        get_response = self.client.get(self.list_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(get_response.data), 1)

    def test_update_category(self):
        payload = {'name': 'Rent', 'description': 'Monthly Rent'}
        create_response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, f"Setup failed: {create_response.data}")
        
        category_id = create_response.data['id'] 
        detail_url = f'{self.list_url}{category_id}/'
        
        response = self.client.put(detail_url, {'name': 'Updated Rent', 'description': 'Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        payload = {'name': 'Entertainment', 'description': 'Fun stuff'}
        create_response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, f"Setup failed: {create_response.data}")
        
        category_id = create_response.data['id']
        detail_url = f'{self.list_url}{category_id}/'
        
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TransactionCRUDTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = '/api/transactions/'
        self.category = Category.objects.create(name="General", description="General Category")

    def test_create_transaction(self):
        payload = {
            'amount': 50.00,
            'description': 'Coffee',
            'category': self.category.pk, 
            'payment_mode':'Cash',
            'type':'Expense',
            'user': self.user.user_id,
            'date': '2026-10-04'
        }
        response = self.client.post(self.list_url, payload, format='json')
        # This will reveal exactly what the serializer doesn't like about the payload
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Failed to create Transaction: {response.data}")

    def test_user_queryset_isolation(self):
        # 1. Create transaction via API
        api_response = self.client.post(self.list_url, {
            'amount': 100.00, 
            'description': 'Test',
            'payment_mode':'Cash',
            'type':'Expense',
            'category': self.category.pk, 
            'user': self.user.user_id,
            'date': '2026-10-04' 
        }, format='json')
        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED, f"Setup failed: {api_response.data}")
        
        # 2. Setup: Create second user
        other_user = User.objects.create_user(email='other@test.com', full_name='Other', password='pass')
        
        # 3. Create transaction via DB for OTHER user (Ensuring date and category are included)
        Transaction.objects.create(
            user=other_user, 
            category=self.category, 
            payment_mode='Cash',
            type='expense',
            amount=500.00, 
            description="Other user's data", 
            date='2026-10-04' 
        )
        
        # Action & Verification
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)