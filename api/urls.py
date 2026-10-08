from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, UserProfileViewSet, TransactionViewSet, CategoryViewSet,
    BudgetViewSet, SavingsGoalViewSet, ReportViewSet, LearningContentViewSet,
    NotificationViewSet, SupportQueryViewSet, UserRegistrationView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')
# CategoryViewSet still has a queryset attribute, so basename is optional, but good practice
router.register(r'categories', CategoryViewSet, basename='category') 
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'savings-goals', SavingsGoalViewSet, basename='savingsgoal')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'learning-content', LearningContentViewSet, basename='learningcontent')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'support-queries', SupportQueryViewSet, basename='supportquery')

urlpatterns = [

    path('jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/register/', UserRegistrationView.as_view(), name='register'),

    path('', include(router.urls)),
    
]