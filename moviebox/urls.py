"""moviebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.first, name='first'),
    path('index',views.index, name='index'),
    path('reg/',views.reg, name='reg'),
    path('reg/addreg',views.addreg, name='addreg'),
    path('login/',views.login, name='login'),
    path('login/addlogin',views.addlogin, name='addlogin'),
    path('logout/',views.logout, name='logout'),
    path('viewuser/',views.viewuser, name='viewuser'),
    path('movie_revenue_prediction/', views.movie_revenue_prediction, name='movie_revenue_prediction'),
    path('view_revenue_prediction/', views.view_revenue_prediction, name='view_revenue_prediction'),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

