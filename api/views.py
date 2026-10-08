from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import (
    User, UserProfile, Transaction, Category, Budget, 
    SavingsGoal, Report, LearningContent, Notification, SupportQuery
)
from .serializers import (
    UserSerializer, UserProfileSerializer, TransactionSerializer, 
    CategorySerializer, BudgetSerializer, SavingsGoalSerializer, 
    ReportSerializer, LearningContentSerializer, NotificationSerializer, 
    SupportQuerySerializer, UserRegistrationSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    # This is crucial: it bypasses the JWT requirement so new users can sign up
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # The user model itself is filtered by its primary key
        return User.objects.filter(pk=self.request.user.pk)

class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserProfileSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    # Category is excluded from the user restriction
    authentication_classes = [JWTAuthentication]
    queryset = Category.objects.all() #[cite: 3]
    serializer_class = CategorySerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        category = serializer.validated_data.get('category')
        user = self.request.user
        
        print("--- DATABASE EXISTENCE CHECK ---")
        # Check if the Category strictly exists in the DB
        cat_exists = category.__class__.objects.filter(pk=category.pk).exists()
        print(f"Category {category.pk} exists in DB: {cat_exists}")
        
        # Check if the User strictly exists in the DB
        user_exists = User.objects.filter(pk=user.pk).exists()
        print(f"User {user.pk} exists in DB: {user_exists}")
        
        serializer.save(user=user)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = BudgetSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class SavingsGoalViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = SavingsGoalSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

class ReportViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = ReportSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

class LearningContentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = LearningContentSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningContent.objects.filter(user=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = NotificationSerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class SupportQueryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = SupportQuerySerializer #[cite: 3]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SupportQuery.objects.filter(user=self.request.user)