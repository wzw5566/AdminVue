"""AdminVue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url, include
from apps import users
from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from apps.users.views import UserViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view


router = DefaultRouter()
router.register(r'api/users', UserViewset, base_name="users")
schema_view = get_swagger_view(title='ShopVue API文档 ')
# router.register(r'api/user/info', UserViewset, base_name="users")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/login', obtain_jwt_token),
    url(r'^', include(router.urls)),
    path('apidoc/', schema_view),
    path('docs/', include_docs_urls(title='ShopVue 文档')),
    #path('api/user/info/', UserDetail),

]
