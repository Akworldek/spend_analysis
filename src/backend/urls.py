from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]

# settings.py additions
# Add these to your project's settings.py

INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'corsheaders',  # For handling CORS
    'django_filters',  # For advanced filtering
    'spend_analysis',  # Your app name
]

MIDDLEWARE = [
    # ... existing middleware
    'corsheaders.middleware.CorsMiddleware',  # Add this before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]

# Allow requests from your React frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Development React server
    # Add your production frontend URL when deployed
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}