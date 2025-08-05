from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    # CRUD API endpoints
    path('api/users/', views.get_all_users, name='get_all_users'),
    path('api/users/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
    path('api/users/<str:email>/update/', views.update_user, name='update_user'),
    path('api/users/<str:email>/delete/', views.delete_user, name='delete_user'),
]