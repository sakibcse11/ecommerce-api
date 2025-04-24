from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet, CustomerRegistrationView, AdminRegistrationView, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'', UserViewSet,basename='user')

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/customer/', CustomerRegistrationView.as_view(), name='customer_register'),
    path('auth/register/admin/', AdminRegistrationView.as_view(), name='admin_register'),

    # User management endpoints
    path('', include(router.urls)),
]