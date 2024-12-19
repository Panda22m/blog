from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # 삭제 URL 추가
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # 로그아웃 URL 추가
    path('login/', auth_views.LoginView.as_view(), name='login'),  # 로그인 URL 추가
    path('register/', views.register, name='register'),  # 회원가입 URL 추가
]