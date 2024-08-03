from django.contrib import admin
from django.urls import path, include
from forum import views as forum_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', forum_views.TopicListView.as_view(), name='home'),
    path('forum/', include('forum.urls')),
]
