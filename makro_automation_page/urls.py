from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from file_processor import views

urlpatterns = [
    # '' should be the base_generic.html
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_file, name='upload'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]