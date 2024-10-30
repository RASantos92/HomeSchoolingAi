from django.contrib import admin
from django.urls import path
from .views import LessonListCreateView, LessonRetrieveUpdateDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
]