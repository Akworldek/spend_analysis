from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('src.backend.urls')),
    path('auth/', include('src.backend.auth_urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('', include(router.urls)),
    path('summary/', views.spending_summary, name='spending_summary'),
    path('monthly/', views.monthly_spending, name='monthly_spending'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile')
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

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
