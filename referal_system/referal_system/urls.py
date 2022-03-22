'''referal_system URL Configuration'''

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

"""
URLs
- admin/ - get admin page
- schema/ - get file 'schema.yaml'
- doc/ - get project documentation with all endpoints
- / - include URLs from person application
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/', SpectacularSwaggerView.as_view(
         template_name='swagger-ui.html', url_name='schema'),
         name='swagger-ui',
         ),
    path('', include('person.urls')),
]
