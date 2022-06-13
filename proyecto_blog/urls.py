"""django_diy_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


# Use include() to add URLS from the blog application  
# Use include() para agregar URL desde la aplicación de blog
from django.urls import include

urlpatterns += [
    path('blog/', include('blog.urls')),
]


# Add URL maps to redirect the base URL to our application  
# Agregue mapas de URL para redirigir la URL base a nuestra aplicación
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
]


#Add Django site authentication urls (for login, logout, password management)  
#Agregue las URL de autenticación del sitio de Django (para iniciar sesión, cerrar sesión, administración de contraseñas)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    
]

# Use static() to add url mapping to serve static files during development (only)   
# Use static() para agregar mapeo de URL para servir archivos estáticos durante el desarrollo (solo)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)