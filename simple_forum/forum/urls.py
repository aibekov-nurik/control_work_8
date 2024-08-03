from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('create_topic/', views.TopicCreateView.as_view(), name='create_topic'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/edit/<int:pk>/', views.TopicUpdateView.as_view(), name='edit_topic'),
    path('topic/delete/<int:pk>/', views.TopicDeleteView.as_view(), name='delete_topic'),
    path('reply/edit/<int:pk>/', views.ReplyUpdateView.as_view(), name='edit_reply'),
    path('reply/delete/<int:pk>/', views.ReplyDeleteView.as_view(), name='delete_reply'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
