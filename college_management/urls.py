from django.contrib import admin
from django.urls import path, include

# Correctly import views from the core app
# from . import views  # Remove this line if it exists
from core import views  # Import views from the core app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Include URLs from the core app
]
